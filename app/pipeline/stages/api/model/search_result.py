from enum import Enum


class SearchResult(Enum):
    FOUND = "Found"
    NOT_FOUND = "Not Found"
    ERROR = "Error"
