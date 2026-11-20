"""Classify INPI similar-mark hits (buscar_nomes.py output) by legal status and relevance."""
import json, sys

DEAD = {"IPAS024": "indeferido", "IPAS235": "indeferido (recurso não provido)", "IPAS157": "arquivado (sem pagamento)",
        "IPAS047": "inexistente (sem pagamento)", "IPAS139": "arquivado (exigência)", "IPAS106": "arquivado (procuração)",
        "IPAS161": "extinto (vigência)", "IPAS304": "extinto (caducidade)", "IPAS669": "caducidade deferida",
        "IPAS409": "cancelado de ofício", "IPAS414": "extinto (art. 217)"}
GRANT = {"IPAS158", "IPAS770"}
REVIVE = {"IPAS237", "IPAS360"}           # recurso provido / recurso pendente after a refusal
CORE = {"9", "09", "35", "42"}
NEAR = {"38", "39", "36", "41", "45", "16"}
RPI_ZIP = "https://revistas.inpi.gov.br/txt/RM{n}.zip"


def status(m):
    ev = m.get("eventos", [])
    st, granted = "pedido em andamento", False
    for e in ev:
        c = e["codigo"]
        if c in GRANT:
            granted, st = True, "concedido"
        elif c in DEAD:
            st = DEAD[c]
        elif c in REVIVE and st.startswith("indeferido"):
            st = "indeferido, com recurso" if c == "IPAS360" else ("concedido" if granted else "pedido em andamento (recurso provido)")
    if st == "concedido" and m.get("vigencia") and m["vigencia"][-4:] < "2026":
        st = "vigência expirada"
    ativo = st in ("concedido", "pedido em andamento", "pedido em andamento (recurso provido)", "indeferido, com recurso")
    return st, ativo


def main(inp, out):
    data = json.load(open(inp))["resultados"]
    summary = {}
    for cand, hits in data.items():
        rel = []
        for m in hits:
            st, ativo = status(m)
            cls = set((m["classes"] or "").split(",")) - {""}
            m["situacao"], m["ativo"] = st, ativo
            m["classes_core"] = sorted(cls & CORE)
            m["classes_proximas"] = sorted(cls & NEAR)
            last = m["eventos"][-1]["rpi"] if m["eventos"] else None
            m["fonte_rpi"] = RPI_ZIP.format(n=last) if last else None
            if ativo and m["score"] >= 88:
                tier = "crítico" if (m["classes_core"] and m["score"] >= 92) else ("alto" if m["classes_core"] else ("moderado" if m["classes_proximas"] else "baixo"))
                rel.append({k: m[k] for k in ("numero", "nome", "apresentacao", "classes", "titulares", "deposito", "concessao",
                                              "vigencia", "situacao", "score", "motivo", "especificacao", "fonte_rpi")} | {"nivel": tier})
        order = {"crítico": 0, "alto": 1, "moderado": 2, "baixo": 3}
        rel.sort(key=lambda r: (order[r["nivel"]], -r["score"]))
        summary[cand] = {"total_semelhantes": len(hits), "ativos_relevantes": len(rel),
                         "por_nivel": {k: sum(1 for r in rel if r["nivel"] == k) for k in order}, "ocorrencias": rel}
    json.dump(summary, open(out, "w"), ensure_ascii=False, indent=1)
    for c, s in summary.items():
        print(f"{c:8} semelhantes={s['total_semelhantes']:5} ativos_relevantes={s['ativos_relevantes']:4} {s['por_nivel']}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
