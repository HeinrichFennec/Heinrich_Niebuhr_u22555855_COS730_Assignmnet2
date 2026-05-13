from dataclasses import dataclass


@dataclass
class Score:
    submission_id: str
    reviewer_id: str
    value: float
    recommendation: str  # accept / reject / revise
