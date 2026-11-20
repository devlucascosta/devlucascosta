"""RDAP (Registro.br, Verisign) for .com.br/.app.br/.com and iTunes Search API for the candidate names."""
import json, subprocess, sys, time, urllib.parse
NOMES = ["Orvia","Rotiva","Novera","Vértia","Atempo","Plenna","Avora","Ordina","Pontta","Oryza","Nivora","Movent",
         "Tavora","Elora","Veyra","Solven","Averto","Tavena","Oltara","Caliro","Orrena"]
OUT = "/home/user/devlucascosta/juridico/naming/dados"


def get(url):
    r = subprocess.run(["curl", "-sS", "--max-time", "40", "-w", "\n%{http_code}", url], capture_output=True, text=True)
    body, _, code = r.stdout.rpartition("\n")
    return code.strip(), body, r.stderr.strip()[:200]


def ascii_(s):
    import unicodedata
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()


res = {}
for nome in NOMES:
    base = ascii_(nome)
    d = {}
    for dom, url in ((f"{base}.com.br", f"https://rdap.registro.br/domain/{base}.com.br"),
                     (f"{base}.app.br", f"https://rdap.registro.br/domain/{base}.app.br"),
                     (f"{base}.com", f"https://rdap.verisign.com/com/v1/domain/{base}.com")):
        code, body, err = get(url)
        info = {"http": code, "erro": err}
        if code == "200":
            try:
                j = json.loads(body)
                info["status"] = j.get("status")
                info["eventos"] = {e.get("eventAction"): e.get("eventDate") for e in j.get("events", [])}
                info["nameservers"] = [n.get("ldhName") for n in j.get("nameservers", [])]
                ents = []
                for e in j.get("entities", []):
                    v = e.get("vcardArray", [None, []])[1]
                    fn = next((x[3] for x in v if x and x[0] == "fn"), None)
                    ents.append({"papel": e.get("roles"), "nome": fn, "handle": e.get("handle")})
                info["entidades"] = ents
            except Exception as ex:
                info["parse"] = str(ex)
        d[dom] = info
        time.sleep(0.6)
    q = urllib.parse.quote(nome)
    apps = []
    for country in ("br", "us"):
        code, body, err = get(f"https://itunes.apple.com/search?term={q}&entity=software&country={country}&limit=25")
        try:
            for a in json.loads(body).get("results", []):
                apps.append({"pais": country, "app": a.get("trackName"), "dev": a.get("artistName"),
                             "genero": a.get("primaryGenre"), "url": a.get("trackViewUrl")})
        except Exception:
            apps.append({"pais": country, "erro": f"{code} {err}"})
    res[nome] = {"dominios": d, "app_store": apps}
    print(nome, {k: v["http"] for k, v in d.items()}, len(apps), flush=True)
    json.dump(res, open(f"{OUT}/dominios_appstore.json", "w"), ensure_ascii=False, indent=1)
