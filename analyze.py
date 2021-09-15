import os

from utils import (
    make_issue,
    prepare_result,
    publish_results,
    get_files,
)


def analyze():
    codepath = os.environ.get("CODE_PATH", "/code")

    issues = []
    lines = []

    bad_caps = {"autofix": "Autofix"}

    issues_dir = os.path.join(codepath, ".deepsource", "analyzer", "issues")

    for filepath in get_files(issues_dir):
        try:
            with open(filepath) as fp:
                lines = fp.readlines()
        except FileNotFoundError:
            continue

        for idx, line in enumerate(lines):
            lno = idx + 1
            for bad_ds, rec in bad_caps.items():
                if bad_ds in line:
                    issues.append(
                        make_issue(
                            "ARM-I0001",
                            f"Badly capitalized word: {bad_ds}. Expected {rec}",
                            filepath,
                            lno,
                            0
                        )
                    )

    results = prepare_result(issues)
    publish_results(results)


if __name__ == "__main__":
    analyze()
