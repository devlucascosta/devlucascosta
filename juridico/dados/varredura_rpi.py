"""Scan INPI RPI trademark issues (official XML) for two process numbers and AgendAI-like names."""
import subprocess, zipfile, io, json, re, sys, unicodedata, os
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

TARGETS = {"918516579", "942861876", "913138185", "930850211", "931762243", "945549784"}
OUT = "/tmp/claude-0/inpi/scan"


def norm(s):
    s = unicodedata.normalize("NFKD", s or "").encode("ascii", "ignore").decode().lower()
    return s


def similar(name):
    n = norm(name); flat = re.sub(r"[^a-z0-9]", "", n); toks = re.findall(r"[a-z0-9]+", n)
    if any(k in flat for k in ("agendai", "agendaai", "agendaia", "agendia")):
        return True
    if "agenda" in toks and any(t in ("ai", "ia") for t in toks):
        return True
    if "agend" in toks and any(t in ("ai", "ia") for t in toks):
        return True
    return False


def rec(pr):
    m = pr.find("marca")
    return {
        "numero": pr.get("numero"), "deposito": pr.get("data-deposito"), "concessao": pr.get("data-concessao"),
        "vigencia": pr.get("data-vigencia"),
        "despachos": [(d.get("codigo"), d.get("nome"), (d.findtext("texto-complementar") or "")[:300]) for d in pr.iter("despacho")],
        "titulares": [(t.get("nome-razao-social"), t.get("pais"), t.get("uf")) for t in pr.iter("titular")],
        "marca": None if m is None else {"nome": m.findtext("nome"), "apresentacao": m.get("apresentacao"), "natureza": m.get("natureza")},
        "nice": [(c.get("codigo"), (c.findtext("especificacao") or "")[:1500]) for c in pr.iter("classe-nice")],
        "vienna": [c.get("codigo") for c in pr.iter("classe-vienna")],
        "sobrestadores": [s.get("processo") or s.get("marca") for s in pr.iter("sobrestador")],
    }


def scan(n):
    path = f"{OUT}/RM{n}.json"
    if os.path.exists(path):
        return n, "cached"
    r = subprocess.run(["curl", "-sS", "-L", "--max-time", "300", f"https://revistas.inpi.gov.br/txt/RM{n}.zip"], capture_output=True)
    data = r.stdout
    try:
        z = zipfile.ZipFile(io.BytesIO(data))
        root = ET.fromstring(z.read(z.namelist()[0]))
    except Exception as e:
        json.dump({"n": n, "error": str(e)[:200], "size": len(data)}, open(path, "w"))
        return n, "error"
    hits, sims, nums = [], [], []
    date = root.get("data")
    for pr in root.iter("processo"):
        num = pr.get("numero")
        txt = " ".join((d.findtext("texto-complementar") or "") for d in pr.iter("despacho"))
        m = pr.find("marca")
        name = m.findtext("nome") if m is not None else ""
        if num in TARGETS or any(t in txt for t in TARGETS):
            hits.append(rec(pr))
        if name and similar(name):
            sims.append(rec(pr))
        if any(d.get("codigo") == "IPAS009" for d in pr.iter("despacho")):
            nums.append(int(num))
    json.dump({"n": n, "data": date, "hits": hits, "sims": sims,
               "pub_range": [min(nums), max(nums)] if nums else None}, open(path, "w"), ensure_ascii=False)
    return n, f"{date} hits={len(hits)} sims={len(sims)}"


if __name__ == "__main__":
    a, b = int(sys.argv[1]), int(sys.argv[2])
    with ThreadPoolExecutor(4) as ex:
        for n, s in ex.map(scan, range(a, b + 1)):
            print(n, s, flush=True)
