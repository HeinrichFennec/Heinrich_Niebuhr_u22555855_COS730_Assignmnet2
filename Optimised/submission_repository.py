class SubmissionRepository:
    def __init__(self):
        self.submissions = {}
        # scores belong to a submission so they live here too, no separate ScoreRepository
        self.scores = {}

    def save(self, submission):
        print("[SubmissionRepository] save")
        self.submissions[submission.submission_id] = submission
        return submission.submission_id

    # one batched write instead of N saveScore calls inside the scoring loop
    def save_scores(self, submission_id, scores):
        print("[SubmissionRepository] saveScores")
        self.scores[submission_id] = list(scores)
        return f"saved:{submission_id}:{len(scores)} scores"
