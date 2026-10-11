from enum import StrEnum


class ScrapeEnvelopeScreenshot(StrEnum):
    FULL = "full"
    VIEWPORT = "viewport"

    def __str__(self) -> str:
        return str(self.value)
