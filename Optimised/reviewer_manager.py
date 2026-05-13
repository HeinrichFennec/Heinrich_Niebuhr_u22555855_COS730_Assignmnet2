MAX_WORKLOAD = 3


class ReviewerManager:
    def __init__(self, reviewer_repository):
        self.reviewer_repository = reviewer_repository

    # was: controller fetched reviewers then looped assignReview itself.
    # now the manager owns the whole flow (Information Expert).
    def assign_reviewers(self, submission):
        print("[ReviewerManager] assignReviewers")
        reviewers = self.reviewer_repository.find_all()
        eligible = self.get_eligible_reviewers(reviewers, submission)
        for r in eligible:
            r.assign_review(submission)
        return eligible

    # single-pass filter: both conditions from the reviewer eligibility decision table (task 3) are evaluated together, no two separate filter passes anymore
    def get_eligible_reviewers(self, reviewers, submission):
        print("[ReviewerManager] getEligibleReviewers")
        return [
            r for r in reviewers
            if submission.author not in r.conflicts and r.workload < MAX_WORKLOAD
        ]

    # evaluator used to call each reviewer directly. now it asks the manager for a list of scores, the manager owns the reviewer interaction.
    def collect_scores(self, assigned_reviewers, submission):
        print("[ReviewerManager] collectScores")
        scores = []
        for r in assigned_reviewers:
            scores.append(r.request_score(submission))
        return scores
