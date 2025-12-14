from __future__ import annotations

import sys
from pathlib import Path


def main() -> None:
    # Ensure src/ is on sys.path so `import frontend` works without installing the project.
    project_root = Path(__file__).resolve().parent
    src_path = project_root / "src"
    sys.path.insert(0, str(src_path))

    from frontend.__main__ import main as run

    run()


if __name__ == "__main__":
    main()
