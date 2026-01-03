"""Agent spécialisé pour identifier le type d'événement et les attentes."""

from google.adk.agents.llm_agent import Agent

from my_agent.callbacks.logging_callbacks import (
    after_agent_logger,
    after_model_logger,
    before_agent_logger,
    before_model_logger,
    before_tool_logger,
    after_tool_logger,
)
from my_agent.tools.validator_tool import validate_contact
from my_agent.tools.memory_tools import get_user_profile


event_type_agent = Agent(
    model="gemini-2.5-flash-lite",
    name="agent_type_evenement",
    description="Clarifie le type d’événement, l’audience et les contraintes clés.",
    instruction=(
        "Identifie le type d'événement (anniversaire, conférence, mariage, etc.), "
        "le nombre d'invités, la date, la ville préférée et les contraintes de ton utilisateur. "
        "Valide les coordonnées (email/téléphone) si fournies. "
        "Demande les informations manquantes de manière concise. "
        "Résume en bullet points à la fin."
    ),
    tools=[validate_contact, get_user_profile],
    before_agent_callback=before_agent_logger,
    after_agent_callback=after_agent_logger,
    before_model_callback=before_model_logger,
    after_model_callback=after_model_logger,
    before_tool_callback=before_tool_logger,
    after_tool_callback=after_tool_logger,
)
