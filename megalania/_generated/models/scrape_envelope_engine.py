from enum import StrEnum


class ScrapeEnvelopeEngine(StrEnum):
    BROWSER = "browser"
    HTTP = "http"

    def __str__(self) -> str:
        return str(self.value)
