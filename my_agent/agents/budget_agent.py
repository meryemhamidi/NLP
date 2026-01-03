"""Agent Budget : calcule et répartit le budget."""

from google.adk.agents.llm_agent import Agent

from my_agent.callbacks.logging_callbacks import (
    before_agent_logger,
    after_agent_logger,
    before_model_logger,
    after_model_logger,
    before_tool_logger,
    after_tool_logger,
)


budget_agent = Agent(
    model="gemini-2.5-flash-lite",  # miniaturisation for cost/latency
    name="agent_budget",
    description="Estime le budget, répartit postes de dépense et propose des ajustements.",
    instruction=(
        "Prends les contraintes utilisateur (budget total, invités, ville, type d'événement). "
        "Propose une répartition poste par poste (lieu, traiteur, technique, animation, déco, imprévus). "
        "Donne 1 option éco et 1 option confort. Résume en tableau texte."
    ),
    before_agent_callback=before_agent_logger,
    after_agent_callback=after_agent_logger,
    before_model_callback=before_model_logger,
    after_model_callback=after_model_logger,
    before_tool_callback=before_tool_logger,
    after_tool_callback=after_tool_logger,
)
