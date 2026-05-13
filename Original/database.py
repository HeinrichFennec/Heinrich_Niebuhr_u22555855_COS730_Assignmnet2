class Database:
    def __init__(self, reviewers=None):
        self.submissions = {}
        self.scores = []
        self.reviewer_records = list(reviewers or [])

    def save_submission(self, submission):
        print("[Database] saveSubmission")
        self.submissions[submission.submission_id] = submission
        return f"saved:{submission.submission_id}"

    def fetch_reviewers(self):
        print("[Database] fetchReviewers")
        return [dict(r) for r in self.reviewer_records]

    def save_score(self, score):
        print("[Database] saveScore")
        self.scores.append(score)
