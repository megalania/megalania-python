from enum import StrEnum


class GeosRoutesItemEngine(StrEnum):
    BROWSER = "browser"
    HTTP = "http"

    def __str__(self) -> str:
        return str(self.value)
