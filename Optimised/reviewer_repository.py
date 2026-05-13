class ReviewerRepository:
    def __init__(self, reviewers):
        self.reviewers = list(reviewers)

    def find_all(self):
        print("[ReviewerRepository] findAll")
        return list(self.reviewers)
