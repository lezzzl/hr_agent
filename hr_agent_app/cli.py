from hr_agent_app.service import handle_message


def main() -> None:
    chat_id = "cli"
    print("HR agent is ready. Type /exit to stop.")

    while True:
        text = input("> ").strip()
        if text in {"/exit", "/quit"}:
            break
        if not text:
            continue

        print(handle_message(chat_id, text))


if __name__ == "__main__":
    main()
