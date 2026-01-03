# Assistant de planification d’événements (ADK) — Documentation détaillée

## Concept général

Assistant multi-agents construit avec Google ADK pour organiser un événement (anniversaire, conférence, mariage…). Il orchestre des agents LLM spécialisés (cadrage, budget, lieux, logistique, planning) et plusieurs outils (météo, validation des contacts, catalogue interne, mémoire utilisateur) afin de produire un plan complet et évaluable.

## Périmètre et dépendances

- Python 3.10+
- Dépendances : `google-adk==1.21.0`, `requests>=2.31.0` (voir `requirements.txt`)
- Réseau : requis pour l’API Open-Meteo (géocodage + météo) via le tool `get_weather`
- Secrets : `my_agent/.env` contient `GOOGLE_API_KEY` (à fournir) et `GOOGLE_GENAI_USE_VERTEXAI` (0 pour exécution locale). Ne committez pas de clé réelle.

## Installation et exécution rapides

```bash
pip install -r requirements.txt
# Exemple d’usage programmatique (Runner ADK) :
python - <<'PY'
from google.adk import Runner
from google.adk.sessions.in_memory_session_service import InMemorySessionService
from my_agent.agent import root_agent

runner = Runner(
    app_name="event_planner",
    agent=root_agent,
    session_service=InMemorySessionService(),
)
session_id = runner.session_service.create_session("event_planner", user_id="demo")
events = runner.run(
    session_id=session_id,
    user_input="Organise un anniversaire à Paris pour 50 invités le 20 juin, budget 8000€.",
)
for e in events:
    print(e)
PY

# Lancer l’évaluation
python evaluate.py
```

## Arborescence et rôle des éléments

```text
.
├─ README.md                  # Documentation détaillée du projet
├─ requirements.txt           # Dépendances (google-adk, requests)
├─ evaluate.py                # Script d’évaluation ADK (AgentEvaluator)
├─ my_agent/
│  ├─ .env                    # Variables d’environnement (clé API, Vertex)
│  ├─ __init__.py             # Export de root_agent
│  ├─ agent.py                # Construit le SequentialAgent racine (assistant_evenement)
│  ├─ agents/                 # Agents spécialisés (cadrage, budget, lieu, logistique, planning)
│  ├─ tools/                  # Tools : météo, validation contact, catalogue lieux, mémoire user
│  ├─ memory/                 # Catalogue statique VENUES
│  ├─ callbacks/              # Callbacks de logs (agents, modèles, tools)
│  └─ evals/                  # Jeux de test + config d’évaluation ADK
└─ .adk/                      # Artéfacts ADK (user_memory.json créé à la volée)
```

### Description des dossiers (rôle)

- `my_agent/` : package principal (agent racine, agents spécialisés, outils, mémoires, callbacks, jeux de test).
- `my_agent/agents/` : tous les agents LLM spécialisés (cadrage, budget, lieux, logistique, planning).
- `my_agent/tools/` : outils appelables par les agents (météo, validation contact, catalogue lieux, mémoire utilisateur).
- `my_agent/memory/` : données applicatives statiques (catalogue de lieux) et exports de dataclasses.
- `my_agent/callbacks/` : callbacks d’observabilité (logs agents, modèles, tools).
- `my_agent/evals/` : données de test et configuration d’évaluation ADK.
- `.adk/` : artéfacts générés par ADK (dont `artifacts/user_memory.json` pour la mémoire utilisateur).
- `requirements.txt` : dépendances.
- `evaluate.py` : lance l’évaluation.
- `README.md` : ce document.

### Où sont les tools ? À quoi servent-ils ?

- `my_agent/tools/validator_tool.py` : vérifie email/téléphone via regex et renvoie un statut.
- `my_agent/tools/venue_tool.py` : filtre le catalogue `VENUES` (ville, capacité, fourchette de prix, indoor).
- `my_agent/tools/weather_tool.py` : interroge Open-Meteo (géocodage + météo courante), gère les erreurs et retourne un statut explicite.
- `my_agent/tools/memory_tools.py` : lit/écrit la mémoire utilisateur persistante (`my_agent/.adk/artifacts/user_memory.json`) avec fusion conditionnelle.
- `my_agent/tools/__init__.py` : centralise les exports publics des tools.

### Où sont les memory ? À quoi servent-elles ?

- `my_agent/memory/app_catalog.py` : définit la dataclass `Venue` et la liste `VENUES` (catalogue statique de lieux Paris/Lyon/Marseille).
- `my_agent/memory/__init__.py` : exporte `VENUES` et `Venue`.
- `my_agent/.adk/artifacts/user_memory.json` (créé au besoin) : stockage persistant des préférences utilisateur, manipulé par `remember_user_profile` / `get_user_profile`.
- Mémoire de session : gérée par ADK (Runner/Session), non stockée dans le code mais utilisée par le runtime.

### Détail par fichier / dossier

- `requirements.txt` : liste minimale des dépendances.
- `evaluate.py` : lance `google.adk.evaluation.AgentEvaluator.evaluate` sur `my_agent/evals/event_planner.test.json`.
- `.adk/` : répertoire d’artéfacts ADK racine (peut rester vide, `user_memory.json` est créé à la demande).

#### Package `my_agent/`

- `.env` : variables d’environnement (`GOOGLE_API_KEY`, `GOOGLE_GENAI_USE_VERTEXAI`).
- `__init__.py` : export `root_agent`.
- `agent.py` : construit le `SequentialAgent` racine `assistant_evenement` en clonant chaque sous-agent.

##### `my_agent/agents/`

- `__init__.py` : marqueur de package.
- `event_type_agent.py` : agent de cadrage (type d’événement, invités, ville, contacts) ; tools `validate_contact`, `get_user_profile`; callbacks de log.
- `budget_agent.py` : ventilation budget (options éco/confort) ; callbacks de log.
- `venue_agent.py` : sélection de lieux via catalogue + météo ; tools `find_venues`, `get_weather`, `get_user_profile`.
- `logistics_agent.py` : checklist prestataires, transports, plan B météo ; tools `get_weather`, `get_user_profile`.
- `planning_agent.py` : synthèse, rétroplanning, plan B, enregistrement des préférences ; tools `remember_user_profile`, `get_user_profile`.

##### `my_agent/tools/`

- `__init__.py` : exports publics des tools.
- `validator_tool.py` : validation légère email/téléphone (regex).
- `venue_tool.py` : filtrage du catalogue `VENUES` (ville, capacité, price_band, indoor).
- `weather_tool.py` : requêtes Open-Meteo (géocodage + météo courante), gestion d’erreurs robuste.
- `memory_tools.py` : persistance JSON des préférences utilisateur dans `my_agent/.adk/artifacts/user_memory.json` (chargement/sauvegarde, fusion conditionnelle).

##### `my_agent/memory/`

- `__init__.py` : export `VENUES`, `Venue`.
- `app_catalog.py` : dataclass `Venue` + liste `VENUES` (Paris, Lyon, Marseille) avec capacité, fourchette de prix (low/mid/high), indoor, notes.

##### `my_agent/callbacks/`

- `logging_callbacks.py` : callbacks de log pour agents, modèles, tools (usage tokens, paramètres, horodatage). Pas de `__init__.py` dédié (package implicite).

##### `my_agent/evals/`

- `event_planner.test.json` : scénario de test (1 requête + référence attendue).
- `test_config.json` : critère d’évaluation (`response_match_score`: 0.6).

## Architecture fonctionnelle

- Agent racine : `assistant_evenement` (`SequentialAgent`) assemble les sous-agents (type, budget, lieu, logistique, planning).
- Modèles : `gemini-2.5-flash-lite` pour réduire coût/latence ; ajustable.
- Mémoires :
  - Session : gérée par ADK (Runner/Session).
  - User : JSON persistant (`my_agent/.adk/artifacts/user_memory.json`) via `remember_user_profile` / `get_user_profile`.
  - App : catalogue global des lieux (`memory/app_catalog.py`).
- Observabilité : callbacks de log avant/après agents, modèles, tools.
- Évaluation : via `evaluate.py` et le dataset `my_agent/evals`.

## Sécurité et bonnes pratiques

- Ne pas committer de clé réelle dans `.env`; préférer des variables d’environnement ou un vault.
- Les appels Open-Meteo peuvent échouer : le tool retourne toujours un statut explicite sans lever d’exception.
- Clonage des sous-agents dans `build_root_agent()` pour éviter les conflits de parentage ADK.
- Remplacer la persistance JSON par un stockage sécurisé en production si nécessaire.
