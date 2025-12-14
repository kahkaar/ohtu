from kps_logic import KPSAdvancedAILogic, KPSAILogic, KPSLogic
from kps_types import KPSType, KPSTypes
from user_io import UserIO


class KPSApp():
    """Main application class for the KPS game."""

    def __init__(self, io: UserIO) -> None:
        self._io = io
        self._types = KPSTypes(
            KPSType("a", "Ihmistä vastaan"),
            KPSType("b", "Tekoälyä vastaan"),
            KPSType("c", "Parannettua tekoälyä"),
        )

    def _display_options(self) -> None:
        """Display the available options to the user."""
        self._io.show("Valitse pelataanko")
        for kps_type in self._types.get_types():
            self._io.show(f" {kps_type}")
        self._io.show("Muilla valinnoilla lopetetaan")

    def logic_factory(self, game_type: str) -> KPSLogic:
        """Factory method to create KPSLogic instances based on type."""

        if game_type == "a":
            return KPSLogic(self._io)
        if game_type == "b":
            return KPSAILogic(self._io)
        if game_type == "c":
            return KPSAdvancedAILogic(self._io)

        raise ValueError("Unknown game type.")

    def run(self) -> None:
        """Run the main application loop."""
        valid_types = self._types.get_key_of_types()

        while True:
            self._display_options()
            option = self._io.get()

            if option not in valid_types:
                break

            self._io.show(
                "Peli loppuu kun pelaaja antaa virheellisen "
                "siirron eli jonkun muun kuin k, p tai s, "
                "tai kun jompikumpi voittaa 5 kertaa"
            )

            logic = self.logic_factory(option)
            logic.play()
