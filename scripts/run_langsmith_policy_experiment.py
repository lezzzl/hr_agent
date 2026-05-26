import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from langsmith import Client
from langsmith.evaluation import evaluate

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from hr_agent_app.graph import graph

DATASET_NAME = os.getenv("LANGSMITH_POLICY_DATASET_NAME", "hr_agent_dialog_policy_tests")


def target(inputs: dict) -> dict:
    result = graph.invoke(inputs)
    return {
        "assistant_response": result.get("assistant_response"),
        "guardrail_status": result.get("guardrail_status"),
        "current_step_id": result.get("current_step_id"),
        "final_answer": result.get("final_answer"),
    }


def response_contains(outputs: dict, reference_outputs: dict) -> bool:
    response = outputs.get("assistant_response") or ""
    expected_parts = reference_outputs.get("assistant_response_contains", [])
    return all(part in response for part in expected_parts)


def no_final_answer(outputs: dict, reference_outputs: dict) -> bool:
    return outputs.get("final_answer") is None


def main() -> None:
    load_dotenv(override=True)
    client = Client(
        api_key=os.getenv("LANGSMITH_API_KEY"),
        api_url=os.getenv("LANGSMITH_ENDPOINT", "https://eu.api.smith.langchain.com"),
    )

    evaluate(
        target,
        data=DATASET_NAME,
        evaluators=[response_contains, no_final_answer],
        experiment_prefix="hr-agent-dialog-policy-tests",
        client=client,
        max_concurrency=1,
    )


if __name__ == "__main__":
    main()
