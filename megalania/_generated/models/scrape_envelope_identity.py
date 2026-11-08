from enum import StrEnum


class ScrapeEnvelopeIdentity(StrEnum):
    CHROME = "chrome"
    FIREFOX = "firefox"

    def __str__(self) -> str:
        return str(self.value)
