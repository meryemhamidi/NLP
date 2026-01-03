"""Assistant de planification d'événements (multi-agents ADK)."""

from google.adk.agents import SequentialAgent

from my_agent.agents.budget_agent import budget_agent
from my_agent.agents.event_type_agent import event_type_agent
from my_agent.agents.logistics_agent import logistics_agent
from my_agent.agents.planning_agent import planning_agent
from my_agent.agents.venue_agent import venue_agent


def build_root_agent() -> SequentialAgent:
    """Construit un arbre d’agents frais pour éviter les conflits de parenté."""
    event_agent = event_type_agent.clone()
    budget = budget_agent.clone()
    venue = venue_agent.clone()
    logistics = logistics_agent.clone()
    planning = planning_agent.clone()

    root = SequentialAgent(
        name="assistant_evenement",
        description="Assistant multi-agents pour organiser un événement (anniversaire, conférence, mariage).",
        sub_agents=[
            event_agent,
            budget,
            venue,
            logistics,
            planning,
        ],
    )
    return root


root_agent = build_root_agent()
