import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langsmith import Client
from langsmith.evaluation import evaluate

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hr_agent_app.graph import graph

DATASET_NAME = os.getenv("LANGSMITH_DATASET_NAME", "hr_agent_role_tests")


def target(inputs: dict) -> dict:
    result = graph.invoke(inputs)
    return {"final_answer": result.get("final_answer") or result.get("assistant_response")}


def exact_final_role(outputs: dict, reference_outputs: dict) -> bool:
    return outputs.get("final_answer") == reference_outputs.get("final_answer")


def main() -> None:
    load_dotenv(override=True)
    client = Client(
        api_key=os.getenv("LANGSMITH_API_KEY"),
        api_url=os.getenv("LANGSMITH_ENDPOINT", "https://eu.api.smith.langchain.com"),
    )

    evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[exact_final_role],
        experiment_prefix="hr-agent-role-tests",
        client=client,
        max_concurrency=1,
    )


if __name__ == "__main__":
    main()
