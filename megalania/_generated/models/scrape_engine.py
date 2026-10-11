from enum import StrEnum


class ScrapeEngine(StrEnum):
    BROWSER = "browser"
    HTTP = "http"

    def __str__(self) -> str:
        return str(self.value)
