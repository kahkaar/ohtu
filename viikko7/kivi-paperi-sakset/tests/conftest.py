import sys
from pathlib import Path

import pytest

# Ensure `src/` is on sys.path so tests can import modules like `kps_app` and `frontend`.
SRC_DIR = Path(__file__).resolve().parents[1] / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


@pytest.fixture(autouse=True)
def reset_frontend_state():
    """Reset the global frontend state between tests."""
    try:
        from frontend.state import state

        state.reset()
    except Exception:
        # Some tests don't import frontend at all.
        pass

    yield

    try:
        from frontend.state import state

        state.reset()
    except Exception:
        pass
