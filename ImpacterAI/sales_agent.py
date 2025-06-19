import json
from pathlib import Path

try:
    from coding_agent import AgenticSystem, safe_log
    from llm_withtools import chat_with_agent
except Exception:  # pragma: no cover - fallback for environments without deps
    class AgenticSystem:
        def __init__(self, *args, **kwargs):
            pass
        def forward(self):
            pass
    def safe_log(*args, **kwargs):
        pass
    def chat_with_agent(*args, **kwargs):
        return []


class SalesAgenticSystem(AgenticSystem):
    """Agent specialized in generating relationship-building content."""

    def __init__(self, sales_strategy, *args, **kwargs):
        super().__init__(problem_statement=sales_strategy, *args, **kwargs)
        self.sales_strategy = sales_strategy

    def forward(self):
        instruction = (
            "You are an autonomous sales agent.\n\n"
            f"<sales_goal>\n{self.sales_strategy}\n</sales_goal>\n\n"
            "Generate actionable steps to build strong client relationships and maximize sales."
        )
        chat_with_agent(instruction, model=getattr(self, 'code_model', None), msg_history=[], logging=safe_log)


def load_sales_tasks(path):
    """Load sales tasks from a JSON file."""
    data = json.loads(Path(path).read_text())
    return [task["description"] for task in data]


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run the sales agent on tasks")
    parser.add_argument("--tasks", default="sales_tasks.json", help="Path to sales tasks JSON")
    parser.add_argument("--git_dir", required=True, help="Repository path")
    parser.add_argument("--base_commit", required=True, help="Base commit hash")
    args = parser.parse_args()

    tasks = load_sales_tasks(args.tasks)
    for task in tasks:
        agent = SalesAgenticSystem(
            sales_strategy=task,
            git_tempdir=args.git_dir,
            base_commit=args.base_commit,
            chat_history_file="sales_chat.md",
            test_description=None,
        )
        agent.forward()


if __name__ == "__main__":
    main()
