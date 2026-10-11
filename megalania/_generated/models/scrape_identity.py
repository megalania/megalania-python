from enum import StrEnum


class ScrapeIdentity(StrEnum):
    CHROME = "chrome"
    FIREFOX = "firefox"

    def __str__(self) -> str:
        return str(self.value)
