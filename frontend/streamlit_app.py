from __future__ import annotations

import httpx
import streamlit as st

from app.config.settings import settings


def analyze_request(customer_id: int, message: str) -> dict[str, object]:
    with httpx.Client(base_url=settings.API_BASE_URL, timeout=settings.DEFAULT_TIMEOUT_SECONDS) as client:
        response = client.post(
            "/analyze",
            json={"customer_id": customer_id, "message": message},
        )
        response.raise_for_status()
        return response.json()


def fetch_execution(execution_id: str) -> dict[str, object]:
    with httpx.Client(base_url=settings.API_BASE_URL, timeout=settings.DEFAULT_TIMEOUT_SECONDS) as client:
        response = client.get(f"/executions/{execution_id}")
        response.raise_for_status()
        return response.json()


st.set_page_config(page_title="AI Operations Agent", page_icon="🤖")

st.title("AI Operations Agent")
st.caption("Sistema multiagente de inteligência operacional")

customer_id = st.number_input("Customer ID", min_value=1, step=1)
user_request = st.text_area("Solicitação do cliente", height=180)

if st.button("ANALISAR SOLICITAÇÃO"):
    if not user_request.strip():
        st.warning("Informe a solicitação antes de continuar.")
    else:
        try:
            result = analyze_request(int(customer_id), user_request)
            st.success("Solicitação processada.")
            st.subheader("Resposta ao cliente")
            st.write(result.get("final_response", ""))

            decision = result.get("decision") or {}
            evaluation = result.get("evaluation") or {}
            left, right = st.columns(2)
            with left:
                st.metric("Decisão", str(decision.get("decision", "-")))
            with right:
                st.metric("Pontuação", str(evaluation.get("overall_score", "-")))

            with st.expander("Detalhes da execução"):
                st.json(result)
                execution_id = result.get("execution_id")
                if execution_id:
                    st.json(fetch_execution(str(execution_id)))
        except httpx.HTTPStatusError as error:
            st.error(f"A API recusou a solicitação: {error.response.text}")
        except httpx.HTTPError as error:
            st.error(f"Não foi possível conectar à API: {error}")
