from enum import StrEnum


class ScrapeExtractModel(StrEnum):
    DEFAULT = "default"
    FAST = "fast"
    NON_CHINA = "non_china"

    def __str__(self) -> str:
        return str(self.value)
