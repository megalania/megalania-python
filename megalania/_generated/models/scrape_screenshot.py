from enum import StrEnum


class ScrapeScreenshot(StrEnum):
    FULL = "full"
    VIEWPORT = "viewport"

    def __str__(self) -> str:
        return str(self.value)
