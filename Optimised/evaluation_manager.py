class EvaluationManager:
    def __init__(self, submission_repository, reviewer_manager, notifier, researcher):
        self.submission_repository = submission_repository
        self.reviewer_manager = reviewer_manager
        self.notifier = notifier
        self.researcher = researcher

    def evaluate(self, submission, assigned_reviewers):
        print("[EvaluationManager] evaluate")
        scores = self.reviewer_manager.collect_scores(assigned_reviewers, submission)
        # one batched write of all scores instead of N individual saveScore calls
        confirmation = self.submission_repository.save_scores(submission.submission_id, scores)
        print(f"[EvaluationManager] confirmation: {confirmation}")
        decision = self.determine_outcome(scores)
        # diagram: notify(researcher, decision). NS owns the routing internally.
        self.notifier.notify(self.researcher, decision)
        return decision

    # collapses calculateAverage + checkConsensus + applyRules into one method.
    def determine_outcome(self, scores):
        print("[EvaluationManager] determineOutcome")
        if not scores:
            return "revision"

        recs = [s.recommendation for s in scores]
        consensus = len(set(recs)) == 1

        if consensus:
            if recs[0] == "accept":   # R1
                return "accepted"
            if recs[0] == "reject":   # R2
                return "rejected"
            if recs[0] == "revise":   # R3
                return "revision"

        average = sum(s.value for s in scores) / len(scores)
        if average >= 7.0:            # R4
            return "accepted"
        if average < 4.0:             # R5
            return "rejected"
        return "revision"             # R6
