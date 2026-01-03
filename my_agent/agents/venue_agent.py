"""Agent Lieu : propose des lieux adaptés via catalogue + météo."""

from google.adk.agents.llm_agent import Agent

from my_agent.callbacks.logging_callbacks import (
    before_agent_logger,
    after_agent_logger,
    before_model_logger,
    after_model_logger,
    before_tool_logger,
    after_tool_logger,
)
from my_agent.tools.venue_tool import find_venues
from my_agent.tools.weather_tool import get_weather
from my_agent.tools.memory_tools import get_user_profile


venue_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="agent_lieu",
    description="Sélectionne des lieux adaptés (ville, capacité, budget) et vérifie la météo.",
    instruction=(
        "Utilise le catalogue interne pour proposer 2-3 lieux pertinents. "
        "Filtre par ville, capacité et price_band si le budget est connu. "
        "Appelle la météo pour la ville pour signaler les risques (pluie/vent) si l'événement est extérieur. "
        "Présente un tableau synthétique (nom, capacité, indoor, prix, remarques)."
    ),
    tools=[find_venues, get_weather, get_user_profile],
    before_agent_callback=before_agent_logger,
    after_agent_callback=after_agent_logger,
    before_model_callback=before_model_logger,
    after_model_callback=after_model_logger,
    before_tool_callback=before_tool_logger,
    after_tool_callback=after_tool_logger,
)
