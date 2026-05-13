class SubmissionController:
    def __init__(self, validator, database, reviewer_manager, evaluation_manager):
        self.validator = validator
        self.database = database
        self.reviewer_manager = reviewer_manager
        self.evaluation_manager = evaluation_manager

    def submit(self, submission, ui):
        print("[SubmissionController] submit")
        valid = self.validator.validate_format(submission)

        if not valid:
            ui.return_error("invalid submission")
            return

        # capture confirmation per diagram return arrow Database -> SubmissionController
        confirmation = self.database.save_submission(submission)
        print(f"[SubmissionController] confirmation: {confirmation}")

        reviewers = self.reviewer_manager.get_available_reviewers(submission)

        for r in reviewers:
            r.assign_review(submission)

        self.evaluation_manager.start_evaluation(submission, reviewers)
