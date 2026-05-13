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

    # diagram shows submitScore originating from Reviewer, so the reviewer
    # itself issues the call. evaluator drives this in its loop.
    def perform_review_and_submit(self, submission, evaluator):
        value = self._compute_score(submission)
        if value >= 7.0:
            rec = "accept"
        elif value <= 4.0:
            rec = "reject"
        else:
            rec = "revise"
        score = Score(submission.submission_id, self.reviewer_id, value, rec)
        print(f"[Reviewer {self.reviewer_id}] submitScore -> {value} ({rec})")
        evaluator.submit_score(score)

    # I made it seeded so demo runs are reproducible
    def _compute_score(self, submission):
        rng = random.Random(f"{self.reviewer_id}|{submission.submission_id}")
        return round(max(0.0, min(10.0, rng.uniform(3.0, 9.5) + self.bias)), 2)
