"""Global (app-level) catalog of venues and services."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class Venue:
    city: str
    name: str
    capacity: int
    price_band: str  # low | mid | high
    indoor: bool
    notes: str


VENUES: List[Venue] = [
    Venue(
        city="Paris",
        name="Loft Marais",
        capacity=80,
        price_band="high",
        indoor=True,
        notes="Loft modulable, cuisine équipée, proche métro Saint-Paul.",
    ),
    Venue(
        city="Paris",
        name="Pavillon Diderot",
        capacity=150,
        price_band="mid",
        indoor=True,
        notes="Salle lumineuse, traiteur partenaire, sono incluse.",
    ),
    Venue(
        city="Lyon",
        name="Rooftop Confluence",
        capacity=120,
        price_band="high",
        indoor=False,
        notes="Vue Saône, idéal cocktails, plan B couvert disponible.",
    ),
    Venue(
        city="Lyon",
        name="La Fabrique",
        capacity=90,
        price_band="mid",
        indoor=True,
        notes="Ancienne usine rénovée, style industriel, mobilier fourni.",
    ),
    Venue(
        city="Marseille",
        name="Terrasse du Vieux-Port",
        capacity=60,
        price_band="mid",
        indoor=False,
        notes="Vue mer, idéale pour soirées estivales, options DJ.",
    ),
    Venue(
        city="Marseille",
        name="Atelier Joliette",
        capacity=120,
        price_band="low",
        indoor=True,
        notes="Budget maîtrisé, traiteur libre, chaises/tables incluses.",
    ),
]
