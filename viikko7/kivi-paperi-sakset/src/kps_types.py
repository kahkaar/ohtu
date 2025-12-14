class KPSType():
    def __init__(
            self,
            key: str,
            option: str,
    ) -> None:
        self._key = key
        self._option = option

    @property
    def key(self) -> str:
        return self._key

    @property
    def option(self) -> str:
        return self._option

    def __str__(self) -> str:
        return f"({self._key}) {self._option}"


class KPSTypes():
    def __init__(self, *types: KPSType) -> None:
        self._types = types

    def get_types(self) -> tuple[KPSType, ...]:
        """Return all KPSType instances."""
        return self._types

    def get_type(self, key: str) -> KPSType | None:
        """Return the KPSType instance matching the provided key, or None if not found."""
        for kps_type in self._types:
            if kps_type.key == key:
                return kps_type
        return None

    def get_key_of_types(self) -> list[str]:
        """Return a list of all keys of the KPSType instances."""
        return [type.key for type in self._types]
