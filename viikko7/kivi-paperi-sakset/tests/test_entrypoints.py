import importlib


def test_web_ui_module_exposes_main():
    m = importlib.import_module("web_ui")
    assert callable(m.main)


def test_index_main_catches_value_error(monkeypatch):
    # Patch index.UserIO and index.KPSApp to avoid real IO.
    import index as idx

    shown = []

    class FakeIO:
        def show(self, *values):
            shown.append(" ".join(str(v) for v in values))

    class FakeApp:
        def __init__(self, io):
            self.io = io

        def run(self):
            raise ValueError("boom")

    monkeypatch.setattr(idx, "UserIO", FakeIO)
    monkeypatch.setattr(idx, "KPSApp", FakeApp)

    idx.main()
    assert any("An error occured" in s for s in shown)
