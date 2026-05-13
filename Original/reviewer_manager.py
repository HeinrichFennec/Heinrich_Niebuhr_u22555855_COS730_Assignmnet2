MAX_WORKLOAD = 3


class ReviewerManager:
    def __init__(self, database, reviewer_pool):
        self.database = database
        self.pool = {r.reviewer_id: r for r in reviewer_pool}

    def get_available_reviewers(self, submission):
        print("[ReviewerManager] getAvailableReviewers")
        records = self.database.fetch_reviewers()
        records = self.filter_conflicts(records, submission)
        records = self.check_workload(records)
        return [self.pool[r["reviewer_id"]] for r in records
                if r["reviewer_id"] in self.pool]

    def filter_conflicts(self, records, submission):
        print("[ReviewerManager] filterConflicts")
        return [r for r in records
                if submission.author not in r.get("conflicts", [])]

    def check_workload(self, records):
        print("[ReviewerManager] checkWorkload")
        return [r for r in records if r.get("workload", 0) < MAX_WORKLOAD]
