class EvaluationManager:
    def __init__(self, database, notifier):
        self.database = database
        self.notifier = notifier
        self.scores = []
        self.average = 0.0
        self.consensus = False
        self.decision = ""

    def start_evaluation(self, submission, reviewers):
        print("[EvaluationManager] startEvaluation")
        self.scores = []

        for r in reviewers:
            r.perform_review_and_submit(submission, self)

        self.calculate_average()
        self.check_consensus()
        self.apply_rules()

        if self.decision == "accepted":
            self.notifier.notify_acceptance(submission)
        elif self.decision == "rejected":
            self.notifier.notify_rejection(submission)
        else:
            self.notifier.notify_revision(submission)

        return self.decision

    def submit_score(self, score):
        print("[EvaluationManager] submitScore")
        self.scores.append(score)
        self.database.save_score(score)

    def calculate_average(self):
        print("[EvaluationManager] calculateAverage")
        if self.scores:
            self.average = sum(s.value for s in self.scores) / len(self.scores)
        else:
            self.average = 0.0

    def check_consensus(self):
        print("[EvaluationManager] checkConsensus")
        recs = {s.recommendation for s in self.scores}
        self.consensus = len(recs) == 1

    def apply_rules(self):
        print("[EvaluationManager] applyRules")
        recs = [s.recommendation for s in self.scores]

        if self.consensus and recs and recs[0] == "accept":
            self.decision = "accepted"
        elif self.consensus and recs and recs[0] == "reject":
            self.decision = "rejected"
        elif self.consensus and recs and recs[0] == "revise":
            self.decision = "revision"
        elif self.average >= 7.0:
            self.decision = "accepted"
        elif self.average < 4.0:
            self.decision = "rejected"
        else:
            self.decision = "revision"