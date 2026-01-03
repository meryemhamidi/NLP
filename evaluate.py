"""Evaluation runner for the event planner assistant."""

import asyncio
from pathlib import Path

from google.adk.evaluation import AgentEvaluator


async def main():
    base_dir = Path(__file__).parent
    dataset = base_dir / "my_agent" / "evals" / "event_planner.test.json"
    # AgentEvaluator will read test_config.json in the same folder automatically.

    await AgentEvaluator.evaluate(
        agent_module="my_agent.agent",
        eval_dataset_file_path_or_dir=str(dataset),
        num_runs=1,
        print_detailed_results=True,
    )


if __name__ == "__main__":
    asyncio.run(main())
