from __future__ import annotations

import httpx
import streamlit as st

from app.config.settings import settings

def _api_headers() -> dict[str, str]:
    return {"X-API-Key": settings.API_AUTH_TOKEN} if settings.API_AUTH_TOKEN else {}

def analyze_request(customer_id: int, message: str) -> dict[str, object]:
    with httpx.Client(
        base_url=settings.API_BASE_URL,
        timeout=settings.DEFAULT_TIMEOUT_SECONDS,
    ) as client:
        response = client.post(
            "/analyze",
            json={"customer_id": customer_id, "message": message},
            headers=_api_headers(),
        )
        response.raise_for_status()
        return response.json()

def fetch_execution(execution_id: str) -> dict[str, object]:
    with httpx.Client(
        base_url=settings.API_BASE_URL,
        timeout=settings.DEFAULT_TIMEOUT_SECONDS,
    ) as client:
        response = client.get(f"/executions/{execution_id}", headers=_api_headers())
        response.raise_for_status()
        return response.json()

def _label(value: object, fallback: str = "Não informado") -> str:
    text = str(value or "").strip().replace("_", " ")
    return text.title() if text else fallback

def _render_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --ink: #17212b;
            --muted: #647381;
            --line: #dbe3e8;
            --paper: #f6f8f7;
            --teal: #087f76;
            --teal-dark: #075d5a;
            --orange: #e28b48;
        }
        .stApp { background: var(--paper); color: var(--ink); }
        [data-testid="stHeader"] { background: rgba(246, 248, 247, 0.88); }
        [data-testid="stSidebar"] { background: #172b36; }
        [data-testid="stSidebar"] * { color: #edf5f2; }
        [data-testid="stSidebar"] .stCaption { color: #a9c2bd; }
        .brand { display: flex; align-items: center; gap: 12px; margin: 10px 0 42px; }
        .brand-mark { background: var(--orange); color: #172b36; border-radius: 11px; padding: 9px 11px; font-size: 21px; font-weight: 800; }
        .brand-name { color: #fff; font-size: 16px; font-weight: 750; letter-spacing: .02em; }
        .brand-sub { color: #9fbab5; font-size: 11px; margin-top: 2px; }
        .eyebrow { color: var(--teal); font-size: 12px; font-weight: 800; letter-spacing: .14em; text-transform: uppercase; margin-bottom: 8px; }
        .hero-title { color: var(--ink); font-size: clamp(30px, 4vw, 48px); line-height: 1.05; font-weight: 800; letter-spacing: -.03em; margin: 0; }
        .hero-copy { color: var(--muted); font-size: 16px; line-height: 1.55; max-width: 680px; margin: 14px 0 28px; }
        .section-title { color: var(--ink); font-size: 20px; font-weight: 760; margin: 26px 0 8px; }
        .response-card { background: #fff; border: 1px solid var(--line); border-left: 5px solid var(--teal); border-radius: 8px; padding: 25px 28px; box-shadow: 0 10px 30px rgba(23, 33, 43, .06); }
        .response-kicker { color: var(--teal); font-size: 11px; font-weight: 800; letter-spacing: .12em; text-transform: uppercase; }
        .response-text { color: var(--ink); font-size: 18px; line-height: 1.65; margin-top: 10px; }
        .status-line { color: var(--muted); font-size: 13px; margin-top: 12px; }
        div[data-testid="stMetric"] { background: #fff; border: 1px solid var(--line); border-radius: 8px; padding: 14px 16px; }
        div[data-testid="stMetricLabel"] { color: var(--muted); }
        div[data-testid="stMetricValue"] { color: var(--ink); }
        .stButton > button { background: var(--teal); border: 0; border-radius: 6px; color: #fff; font-weight: 750; min-height: 44px; }
        .stButton > button:hover { background: var(--teal-dark); color: #fff; }
        .stTextArea textarea, .stNumberInput input { background: #fff; border: 1px solid var(--line); border-radius: 6px; }
        .hint { background: #e9f2ef; border-radius: 6px; color: #28655f; font-size: 13px; line-height: 1.5; padding: 12px 14px; }
        .footer { border-top: 1px solid var(--line); color: var(--muted); font-size: 12px; margin-top: 48px; padding: 18px 0 8px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

st.set_page_config(page_title="AI Operations Agent", page_icon="AO", layout="wide")
_render_styles()

with st.sidebar:
    st.markdown(
        """
        <div class="brand">
            <div class="brand-mark">AO</div>
            <div>
                <div class="brand-name">AI Operations</div>
                <div class="brand-sub">Operational intelligence console</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("WORKSPACE")
    st.markdown("**Atendimento inteligente**")
    st.caption("Fluxo multiagente conectado à API operacional.")
    st.divider()
    st.caption("SYSTEM STATUS")
    st.success("API configurada")
    st.caption(f"Endpoint: {settings.API_BASE_URL}")
    st.caption("SQLite · Auditoria ativa")

st.markdown('<div class="eyebrow">Operational intelligence</div>', unsafe_allow_html=True)
st.markdown('<h1 class="hero-title">Transforme solicitações em decisões.</h1>', unsafe_allow_html=True)
st.markdown(
    '<p class="hero-copy">Investigue o contexto do cliente, recupere conhecimento relevante e produza uma próxima ação rastreável em poucos segundos.</p>',
    unsafe_allow_html=True,
)

st.markdown('<div class="section-title">Nova análise</div>', unsafe_allow_html=True)
input_col, context_col = st.columns([1.7, 1], gap="large")
with input_col:
    user_request = st.text_area(
        "Solicitação do cliente",
        height=150,
        placeholder="Ex.: Meu refrigerador voltou a apresentar a mesma falha depois do reparo.",
        label_visibility="visible",
    )
with context_col:
    customer_id = st.number_input("Customer ID", min_value=1, value=1001, step=1)
    st.markdown(
        '<div class="hint">A análise combina histórico, tickets, políticas aplicáveis e regras de decisão antes de gerar a resposta.</div>',
        unsafe_allow_html=True,
    )

analyze = st.button("Executar análise", type="primary", use_container_width=True)

if analyze:
    if not user_request.strip():
        st.warning("Informe a solicitação antes de continuar.")
    else:
        try:
            with st.spinner("Orquestrando agentes e consolidando evidências..."):
                result = analyze_request(int(customer_id), user_request)

            decision = result.get("decision") or {}
            evaluation = result.get("evaluation") or {}
            response_text = str(result.get("final_response", ""))

            st.markdown('<div class="section-title">Resultado da operação</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="response-card"><div class="response-kicker">Resposta pronta para o cliente</div><div class="response-text">{response_text}</div></div>',
                unsafe_allow_html=True,
            )
            st.markdown('<div class="status-line">Resposta gerada com base no estado compartilhado e nas evidências recuperadas.</div>', unsafe_allow_html=True)

            metric_one, metric_two, metric_three = st.columns(3)
            with metric_one:
                st.metric("Decisão", _label(decision.get("decision")))
            with metric_two:
                st.metric("Qualidade", f'{evaluation.get("overall_score", "-")}/100')
            with metric_three:
                st.metric("Risco de alucinação", _label(evaluation.get("hallucination_risk")))

            with st.expander("Ver auditoria da execução"):
                execution_id = result.get("execution_id")
                st.caption(f"Execution ID: {execution_id}")
                if execution_id:
                    st.json(fetch_execution(str(execution_id)))
        except httpx.HTTPStatusError as error:
            st.error(f"A API recusou a solicitação: {error.response.text}")
        except httpx.HTTPError as error:
            st.error(f"Não foi possível conectar à API: {error}")

st.markdown('<div class="footer">AI Operations Agent · Decision support for customer operations</div>', unsafe_allow_html=True)
