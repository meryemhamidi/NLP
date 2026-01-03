"""Agent Logistique : invitations, prestataires, risques, to-dos."""

from google.adk.agents.llm_agent import Agent

from my_agent.callbacks.logging_callbacks import (
    before_agent_logger,
    after_agent_logger,
    before_model_logger,
    after_model_logger,
    before_tool_logger,
    after_tool_logger,
)
from my_agent.tools.memory_tools import get_user_profile
from my_agent.tools.weather_tool import get_weather


logistics_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="agent_logistique",
    description="Prépare la logistique (invitations, prestataires, risques météo, transport).",
    instruction=(
        "Établis une checklist logistique : invitations, prestataires (traiteur, DJ, technique), "
        "assurances, plan B météo, transports/hébergement pour invités. "
        "Si l'événement est extérieur, appelle la météo et propose un plan B intérieur. "
        "Retourne une liste d'actions avec échéances et responsables."
    ),
    tools=[get_weather, get_user_profile],
    before_agent_callback=before_agent_logger,
    after_agent_callback=after_agent_logger,
    before_model_callback=before_model_logger,
    after_model_callback=after_model_logger,
    before_tool_callback=before_tool_logger,
    after_tool_callback=after_tool_logger,
)
