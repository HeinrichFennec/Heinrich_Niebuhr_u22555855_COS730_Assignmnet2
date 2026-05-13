import random
from score import Score


class Reviewer:
    def __init__(self, reviewer_id, name, conflicts=None, workload=0, bias=0.0):
        self.reviewer_id = reviewer_id
        self.name = name
        self.conflicts = list(conflicts or [])
        self.workload = workload
        self.bias = bias
        self.assigned = []

    def assign_review(self, submission):
        print(f"[Reviewer {self.reviewer_id}] assignReview")
        self.assigned.append(submission)
        self.workload += 1

    # diagram has requestScore returning a score, so the reviewer just hands it back.So no more direct call into the evaluator - that coupling is gone.
    def request_score(self, submission):
        value = self._compute_score(submission)
        if value >= 7.0:
            rec = "accept"
        elif value <= 4.0:
            rec = "reject"
        else:
            rec = "revise"
        score = Score(submission.submission_id, self.reviewer_id, value, rec)
        print(f"[Reviewer {self.reviewer_id}] requestScore -> {value} ({rec})")
        return score

    # seeded so the optimised run produces the same scores as the baseline run
    def _compute_score(self, submission):
        rng = random.Random(f"{self.reviewer_id}|{submission.submission_id}")
        return round(max(0.0, min(10.0, rng.uniform(3.0, 9.5) + self.bias)), 2)
