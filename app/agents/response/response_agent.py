from __future__ import annotations

from typing import Any

from app.agents.base_agent import BaseAgent


class ResponseAgent(BaseAgent):
    name = "response"

    def run(self, state: dict[str, Any]) -> dict[str, Any]:
        customer = state.get("customer_data") or {}
        product = state.get("product_data") or {}
        decision = state.get("decision") or {}
        root_cause = state.get("root_cause") or {}

        customer_name = customer.get("name", "cliente")
        product_name = product.get("name", "seu produto")
        decision_code = decision.get("decision", "provide_initial_guidance")

        if decision_code == "escalate_technical":
            response = (
                f"Olá, {customer_name}. Entendemos a importância do problema com {product_name}. "
                "Identificamos um histórico que precisa de atenção técnica e vamos encaminhar o caso "
                "para avaliação prioritária. Nossa equipe analisará os atendimentos anteriores e "
                "retornará com a próxima ação."
            )
        elif decision_code == "continue_investigation":
            response = (
                f"Olá, {customer_name}. Recebemos sua solicitação sobre {product_name}. "
                "Estamos complementando a análise do caso e validando o procedimento aplicável. "
                "Manteremos o atendimento em acompanhamento e informaremos a próxima etapa."
            )
        else:
            response = (
                f"Olá, {customer_name}. Recebemos sua solicitação sobre {product_name}. "
                "Para orientar o próximo passo com segurança, precisamos confirmar alguns detalhes "
                "do problema e do atendimento anterior. Envie, por favor, quando o problema começou "
                "e se houve alguma tentativa de reparo."
            )

        state["final_response"] = response
        state.setdefault("execution_metadata", {})
        state["execution_metadata"].setdefault("agents", [])
        state["execution_metadata"]["agents"].append(self.name)
        state["execution_metadata"]["response_metadata"] = {
            "decision_used": decision_code,
            "customer_name_used": bool(customer.get("name")),
            "product_name_used": bool(product.get("name")),
            "contains_internal_recommendation": False,
        }
        return state