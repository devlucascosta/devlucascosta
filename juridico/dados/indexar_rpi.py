"""Build a local SQLite index of INPI trademark publications (RPI, seção Marcas, XML oficial).

Every process and every despacho of every scanned issue goes into the index, so any future name search runs
locally without downloading the RPI again. Raw ZIPs are kept in RAW_DIR for reuse.
Usage: python3 indexar_rpi.py <primeira_edicao> <ultima_edicao>
"""
import io, os, sqlite3, subprocess, sys, zipfile
import xml.etree.ElementTree as ET
from concurrent.futures import ThreadPoolExecutor

BASE = os.environ.get("RPI_DIR", "/tmp/claude-0/inpi")
RAW = f"{BASE}/raw"
DB = f"{BASE}/rpi_marcas.sqlite"
os.makedirs(RAW, exist_ok=True)


def fetch(n):
    path = f"{RAW}/RM{n}.zip"
    for attempt in range(3):
        if os.path.exists(path):
            try:
                zipfile.ZipFile(path).testzip()
                return n, path
            except Exception:
                os.remove(path)
        subprocess.run(["curl", "-sS", "-L", "--max-time", "400", "-o", path, f"https://revistas.inpi.gov.br/txt/RM{n}.zip"],
                       capture_output=True)
    return n, path if os.path.exists(path) else None


def setup(con):
    con.executescript("""
    CREATE TABLE IF NOT EXISTS edicoes(n INTEGER PRIMARY KEY, data TEXT, ok INTEGER, erro TEXT);
    CREATE TABLE IF NOT EXISTS marcas(numero TEXT PRIMARY KEY, nome TEXT, apresentacao TEXT, natureza TEXT,
        classes TEXT, especificacao TEXT, titulares TEXT, deposito TEXT, concessao TEXT, vigencia TEXT, vienna TEXT,
        primeira_rpi INTEGER, ultima_rpi INTEGER);
    CREATE TABLE IF NOT EXISTS eventos(n INTEGER, numero TEXT, codigo TEXT, despacho TEXT, texto TEXT, titulares TEXT);
    CREATE INDEX IF NOT EXISTS ev_num ON eventos(numero);
    """)


def ingest(con, n, path):
    try:
        z = zipfile.ZipFile(path)
        root = ET.fromstring(z.read(z.namelist()[0]))
    except Exception as e:
        con.execute("INSERT OR REPLACE INTO edicoes VALUES(?,?,?,?)", (n, None, 0, str(e)[:200]))
        return 0
    data = root.get("data")
    k = 0
    for pr in root.iter("processo"):
        num = pr.get("numero")
        tit = " | ".join(f'{t.get("nome-razao-social")} ({t.get("pais") or ""}/{t.get("uf") or ""})' for t in pr.iter("titular"))
        for d in pr.iter("despacho"):
            con.execute("INSERT INTO eventos VALUES(?,?,?,?,?,?)",
                        (n, num, d.get("codigo"), d.get("nome"), (d.findtext("texto-complementar") or "")[:400], tit))
        m = pr.find("marca")
        classes = [c.get("codigo") for c in pr.iter("classe-nice")]
        espec = " || ".join(f'{c.get("codigo")}: {(c.findtext("especificacao") or "")[:700]}' for c in pr.iter("classe-nice"))
        nome = m.findtext("nome") if m is not None else None
        row = con.execute("SELECT nome, classes, primeira_rpi FROM marcas WHERE numero=?", (num,)).fetchone()
        if row is None:
            con.execute("INSERT INTO marcas VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (num, nome, m.get("apresentacao") if m is not None else None, m.get("natureza") if m is not None else None,
                         ",".join(classes), espec, tit, pr.get("data-deposito"), pr.get("data-concessao"), pr.get("data-vigencia"),
                         ",".join(c.get("codigo") for c in pr.iter("classe-vienna")), n, n))
        else:
            con.execute("""UPDATE marcas SET nome=COALESCE(?,nome), apresentacao=COALESCE(?,apresentacao), natureza=COALESCE(?,natureza),
                classes=CASE WHEN ?<>'' THEN ? ELSE classes END, especificacao=CASE WHEN ?<>'' THEN ? ELSE especificacao END,
                titulares=CASE WHEN ?<>'' THEN ? ELSE titulares END, deposito=COALESCE(?,deposito), concessao=COALESCE(?,concessao),
                vigencia=COALESCE(?,vigencia), ultima_rpi=? WHERE numero=?""",
                        (nome, m.get("apresentacao") if m is not None else None, m.get("natureza") if m is not None else None,
                         ",".join(classes), ",".join(classes), espec, espec, tit, tit, pr.get("data-deposito"),
                         pr.get("data-concessao"), pr.get("data-vigencia"), n, num))
        k += 1
    con.execute("INSERT OR REPLACE INTO edicoes VALUES(?,?,?,?)", (n, data, 1, None))
    return k


def main(a, b):
    con = sqlite3.connect(DB)
    setup(con)
    done = {r[0] for r in con.execute("SELECT n FROM edicoes WHERE ok=1")}
    todo = [n for n in range(a, b + 1) if n not in done]
    with ThreadPoolExecutor(6) as ex:
        for n, path in ex.map(fetch, todo):          # downloads in parallel, ingests in order
            k = ingest(con, n, path) if path else 0
            if not path:
                con.execute("INSERT OR REPLACE INTO edicoes VALUES(?,?,?,?)", (n, None, 0, "download falhou"))
            con.commit()
            print(n, k, flush=True)
    con.close()


if __name__ == "__main__":
    main(int(sys.argv[1]), int(sys.argv[2]))
