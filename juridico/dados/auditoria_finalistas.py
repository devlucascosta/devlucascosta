"""Varredura ampliada no índice local da RPI para os finalistas (sem reindexar).

Compara cada palavra (e o nome inteiro sem espaços) de todas as marcas com cada candidato por:
  (a) distância de edição <= 2 na grafia;
  (b) distância <= 2 na forma fonética de buscar_nomes.phon;
  (c) distância <= 1 numa chave "frouxa" que iguala pares surdos/sonoros e grafias equivalentes
      (d=t, v=f, b=p, g=c, z=s, ce/ci=se/si, ge/gi=je/ji, vogal final ignorada);
  (d) candidato contido numa palavra (prefixo ou sufixo extra).
Uso: python3 auditoria_finalistas.py saida.json Nome1 Nome2 ...
"""
import json, re, sqlite3, sys
from rapidfuzz.distance import Levenshtein
from buscar_nomes import DB, ascii_, phon, tokens
from classificar_conflitos import status, CORE

ALVO = {"9", "09", "35", "42", "39"}


def frouxa(s):
    s = phon(s)
    s = re.sub(r"c([ei])", r"s\1", s)
    s = re.sub(r"g([ei])", r"j\1", s)
    for a, b in (("d", "t"), ("v", "f"), ("b", "p"), ("g", "c"), ("z", "s"), ("q", "c")):
        s = s.replace(a, b)
    s = re.sub(r"(.)\1+", r"\1", s)
    return re.sub(r"[aeiou]$", "", s)


def main(out, cands):
    C = [(c, ascii_(c), phon(c), frouxa(c)) for c in cands]
    con = sqlite3.connect(DB)
    hits = {c: [] for c in cands}
    for numero, nome, classes in con.execute("SELECT numero, nome, classes FROM marcas WHERE nome IS NOT NULL AND nome != ''"):
        toks = tokens(nome)
        if not toks:
            continue
        pal = set(t for t in toks if len(t) >= 4)
        if len(toks) > 1:
            pal.add("".join(toks))
        for c, ca, cp, cf in C:
            for t in pal:
                if abs(len(t) - len(ca)) > 3:
                    if ca in t and len(t) <= len(ca) + 6:
                        hits[c].append((numero, nome, classes, t, "contém o nome"))
                        break
                    continue
                d = Levenshtein.distance(t, ca, score_cutoff=2)
                dp = Levenshtein.distance(phon(t), cp, score_cutoff=2)
                df = Levenshtein.distance(frouxa(t), cf, score_cutoff=1)
                if d <= 2 or dp <= 2 or df <= 1 or ca in t:
                    why = ("idêntico" if t == ca else "fonética idêntica" if phon(t) == cp else
                           "chave frouxa idêntica" if frouxa(t) == cf else "contém o nome" if ca in t else
                           f"distância {min(d, dp)}" + (" (chave frouxa 1)" if df <= 1 else ""))
                    hits[c].append((numero, nome, classes, t, why))
                    break
    res = {}
    for c, lst in hits.items():
        rows = []
        for numero, nome, classes, t, why in lst:
            ev = [dict(zip(("rpi", "codigo", "despacho"), r)) for r in
                  con.execute("SELECT n, codigo, despacho FROM eventos WHERE numero=? ORDER BY n", (numero,))]
            campos = ("numero", "nome", "apresentacao", "natureza", "classes", "especificacao", "titulares", "deposito",
                      "concessao", "vigencia")
            m = dict(zip(campos, con.execute(f"SELECT {', '.join(campos)} FROM marcas WHERE numero=?", (numero,)).fetchone()))
            m["eventos"] = ev
            st, ativo = status(m)
            cls = set((classes or "").split(",")) - {""}
            rows.append({**{k: m[k] for k in m if k != "eventos"}, "palavra": t, "motivo": why, "situacao": st, "ativo": ativo,
                         "classes_alvo": sorted(cls & ALVO), "ultimo_despacho": ev[-1] if ev else None})
        rows.sort(key=lambda r: (not r["ativo"], not r["classes_alvo"], r["motivo"] != "idêntico", r["nome"]))
        res[c] = {"total": len(rows), "ativos": sum(r["ativo"] for r in rows),
                  "ativos_classes_alvo": sum(r["ativo"] and bool(r["classes_alvo"]) for r in rows), "ocorrencias": rows}
        print(c, res[c]["total"], res[c]["ativos"], res[c]["ativos_classes_alvo"], flush=True)
    json.dump(res, open(out, "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2:])
