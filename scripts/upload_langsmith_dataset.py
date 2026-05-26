import argparse
import json
import os
import uuid
from pathlib import Path

from dotenv import load_dotenv
from langsmith import Client
from langsmith.schemas import DataType


DEFAULT_DATASET_NAME = "hr_agent_role_tests"
DEFAULT_DATASET_PATH = Path("datasets/hr_agent_role_tests.jsonl")


def load_cases(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as file:
        return [json.loads(line) for line in file if line.strip()]


def get_or_create_dataset(client: Client, dataset_name: str):
    try:
        return client.read_dataset(dataset_name=dataset_name)
    except Exception:
        return client.create_dataset(
            dataset_name,
            description="Role classification tests for the HR LangGraph agent.",
            data_type=DataType.kv,
        )


def stable_example_id(dataset_name: str, case_id: str) -> uuid.UUID:
    return uuid.uuid5(uuid.NAMESPACE_URL, f"langsmith:{dataset_name}:{case_id}")


def upload_cases(client: Client, dataset_name: str, cases: list[dict]) -> None:
    dataset = get_or_create_dataset(client, dataset_name)

    for case in cases:
        example_id = stable_example_id(dataset_name, case["id"])
        kwargs = {
            "example_id": example_id,
            "dataset_id": dataset.id,
            "inputs": case["inputs"],
            "outputs": case["outputs"],
            "metadata": {
                **case.get("metadata", {}),
                "case_id": case["id"],
            },
            "split": case.get("metadata", {}).get("split", "test"),
        }

        try:
            client.create_example(**kwargs)
            action = "created"
        except Exception:
            client.update_example(
                example_id,
                inputs=kwargs["inputs"],
                outputs=kwargs["outputs"],
                metadata=kwargs["metadata"],
                split=kwargs["split"],
                dataset_id=dataset.id,
            )
            action = "updated"

        print(f"{action}: {case['id']}")

    print(f"dataset: {dataset_name}")
    print(f"examples: {len(cases)}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", default=os.getenv("LANGSMITH_DATASET_NAME", DEFAULT_DATASET_NAME))
    parser.add_argument("--path", default=str(DEFAULT_DATASET_PATH))
    args = parser.parse_args()

    load_dotenv(override=True)
    client = Client(
        api_key=os.getenv("LANGSMITH_API_KEY"),
        api_url=os.getenv("LANGSMITH_ENDPOINT", "https://eu.api.smith.langchain.com"),
    )

    upload_cases(client, args.name, load_cases(Path(args.path)))


if __name__ == "__main__":
    main()
