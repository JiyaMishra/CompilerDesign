import os
import subprocess
import sys


class Executor:

    def __init__(self):
        self.generated_file = os.path.join(
            os.path.dirname(__file__),
            "generated",
            "output.py"
        )

    def execute(self):

        if not os.path.exists(self.generated_file):
            raise FileNotFoundError(
                f"Generated file not found:\n{self.generated_file}"
            )

        print("\n========== EXECUTING GENERATED CODE ==========\n")

        result = subprocess.run(
            [sys.executable, self.generated_file],
            capture_output=True,
            text=True
        )

        if result.stdout:
            print(result.stdout)

        if result.stderr:
            print(result.stderr)


if __name__ == "__main__":

    executor = Executor()
    executor.execute()