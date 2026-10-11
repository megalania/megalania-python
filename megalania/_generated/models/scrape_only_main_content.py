from enum import StrEnum


class ScrapeOnlyMainContent(StrEnum):
    FALSE = "false"
    TRUE = "true"

    def __str__(self) -> str:
        return str(self.value)
