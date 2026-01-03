"""Agent Planning : synthétise le plan global et enregistre les préférences."""

from google.adk.agents.llm_agent import Agent

from my_agent.callbacks.logging_callbacks import (
    before_agent_logger,
    after_agent_logger,
    before_model_logger,
    after_model_logger,
    before_tool_logger,
    after_tool_logger,
)
from my_agent.tools.memory_tools import remember_user_profile, get_user_profile


planning_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="agent_planning",
    description="Compile les sorties des autres agents et produit un rétroplanning actionnable.",
    instruction=(
        "Récupère les décisions prises (type d'événement, budget, lieux, logistique) et génère : "
        "1) un rétroplanning semaine par semaine, "
        "2) un plan B météo si besoin, "
        "3) un résumé exécutif en bullet points. "
        "Enregistre les préférences clés (ville, type, budget) dans la mémoire utilisateur."
    ),
    tools=[remember_user_profile, get_user_profile],
    before_agent_callback=before_agent_logger,
    after_agent_callback=after_agent_logger,
    before_model_callback=before_model_logger,
    after_model_callback=after_model_logger,
    before_tool_callback=before_tool_logger,
    after_tool_callback=after_tool_logger,
)
