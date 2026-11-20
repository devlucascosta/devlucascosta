"""Search the local RPI index (indexar_rpi.py) for names similar to a list of candidates.

Similarity = exact / contained / phonetically normalised / fuzzy (rapidfuzz) on each word of the mark name.
Writes one JSON with, per candidate, every similar mark and its full event timeline.
Usage: python3 buscar_nomes.py saida.json Nome1 Nome2 ...
"""
import json, re, sqlite3, sys, unicodedata
from rapidfuzz import fuzz

DB = "/tmp/claude-0/inpi/rpi_marcas.sqlite"
KEY_CLASSES = {"9", "09", "35", "42", "38", "39", "36", "41"}


def ascii_(s):
    return unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()


def phon(s):
    s = ascii_(s)
    for a, b in (("ph", "f"), ("y", "i"), ("w", "v"), ("k", "c"), ("qu", "c"), ("ç", "s"), ("sh", "x"), ("ch", "x")):
        s = s.replace(a, b)
    s = re.sub(r"(.)\1+", r"\1", s)        # double letters
    s = re.sub(r"^h", "", s)
    return s


def tokens(name):
    return [t for t in re.findall(r"[a-z0-9]+", ascii_(name)) if t]


def score(cand, name):
    c, cp = ascii_(cand), phon(cand)
    flat = "".join(tokens(name))
    best, why = 0, ""
    if c == flat:
        return 100, "idêntico"
    toks = tokens(name)
    if phon(flat) == cp:
        return 96, "fonética idêntica (junto)"
    for t in toks:
        if t == c:
            return 99, "palavra idêntica"
        if phon(t) == cp:
            best, why = max((best, why), (96, "fonética idêntica"))
        if len(c) >= 5 and c in t:
            best, why = max((best, why), (92, "contém o nome"))
        if abs(len(t) - len(c)) <= 2 and len(t) >= 4:
            r = fuzz.ratio(phon(t), cp)
            if r >= 80:
                best, why = max((best, why), (r, f"semelhante ({r:.0f}%)"))
    return best, why


def main(out, cands):
    con = sqlite3.connect(DB)
    rows = con.execute("SELECT numero, nome, apresentacao, natureza, classes, especificacao, titulares, deposito, concessao, vigencia, vienna, primeira_rpi, ultima_rpi FROM marcas WHERE nome IS NOT NULL").fetchall()
    eds = dict(con.execute("SELECT n, data FROM edicoes"))
    res = {c: [] for c in cands}
    # cheap pre-filter: first 2 phonetic letters or containment
    keys = {c: (phon(c)[:2], ascii_(c)) for c in cands}
    for r in rows:
        nm = r[1]; a = ascii_(nm).replace(" ", "")
        ts = tokens(nm)
        tp = {phon(t)[:2] for t in ts}
        for c in cands:
            p2, ca = keys[c]
            if not (any(ca in t for t in ts) or ca == a or (p2 in tp and any(abs(len(t) - len(ca)) <= 2 for t in ts))):
                continue
            s, why = score(c, nm)
            if s >= 80:
                res[c].append({"numero": r[0], "nome": nm, "apresentacao": r[2], "natureza": r[3], "classes": r[4],
                               "especificacao": (r[5] or "")[:700], "titulares": r[6], "deposito": r[7], "concessao": r[8],
                               "vigencia": r[9], "vienna": r[10], "score": round(s), "motivo": why})
    for c in cands:
        for m in res[c]:
            ev = con.execute("SELECT n, codigo, despacho, texto FROM eventos WHERE numero=? ORDER BY n", (m["numero"],)).fetchall()
            m["eventos"] = [{"rpi": n, "data": eds.get(n), "codigo": cod, "despacho": d, "texto": t[:300]} for n, cod, d, t in ev]
            m["ultimo_despacho"] = m["eventos"][-1]["despacho"] if m["eventos"] else None
            m["classe_chave"] = bool(set((m["classes"] or "").split(",")) & KEY_CLASSES)
        res[c].sort(key=lambda m: (-m["score"], not m["classe_chave"]))
    json.dump({"base": f"RPI edições {min(eds)}–{max(eds)} ({len(eds)} edições indexadas)", "resultados": res},
              open(out, "w"), ensure_ascii=False, indent=1)
    for c in cands:
        print(c, len(res[c]), sum(1 for m in res[c] if m["classe_chave"]))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
