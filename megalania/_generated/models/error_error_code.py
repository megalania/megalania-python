from enum import StrEnum


class ErrorErrorCode(StrEnum):
    ACTION_FAILED = "action_failed"
    BAD_EXTRACT = "bad_extract"
    BAD_PARAMETER = "bad_parameter"
    BAD_TOKEN = "bad_token"
    BLOCKED = "blocked"
    BODY_TOO_LARGE = "body_too_large"
    BUSY = "busy"
    CAPACITY_SPENT = "capacity_spent"
    CONVERT_CAP = "convert_cap"
    FETCH_ERROR = "fetch_error"
    FORBIDDEN_TARGET = "forbidden_target"
    INSUFFICIENT_CREDITS = "insufficient_credits"
    INTERNAL = "internal"
    LLM_GLOBAL_STOP = "llm_global_stop"
    LLM_TOKEN_CAP = "llm_token_cap"
    LLM_UNAVAILABLE = "llm_unavailable"
    OVER_CONCURRENCY = "over_concurrency"
    REPLAYED = "replayed"
    TIMEOUT = "timeout"
    UNAVAILABLE = "unavailable"
    UNSUPPORTED_MEDIA_TYPE = "unsupported_media_type"
    UPSTREAM_CAP = "upstream_cap"
    WRONG_SCOPE = "wrong_scope"

    def __str__(self) -> str:
        return str(self.value)
