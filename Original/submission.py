from dataclasses import dataclass


@dataclass
class Submission:
    submission_id: str
    title: str
    abstract: str
    content: str
    author: str
