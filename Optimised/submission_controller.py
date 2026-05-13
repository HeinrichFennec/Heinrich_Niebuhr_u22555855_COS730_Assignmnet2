class SubmissionController:
    def __init__(self, validator, submission_repository, reviewer_manager, evaluation_manager):
        self.validator = validator
        self.submission_repository = submission_repository
        self.reviewer_manager = reviewer_manager
        self.evaluation_manager = evaluation_manager

    def submit(self, submission, ui):
        print("[SubmissionController] submit")
        valid = self.validator.validate_format(submission)

        if not valid:
            ui.return_error("invalid submission")
            return

        # repository handles persistence, controller does not touch the database
        submission_id = self.submission_repository.save(submission)
        print(f"[SubmissionController] submissionId: {submission_id}")

        # manager owns reviewer fetching, eligibility filtering and the assignment loop
        assigned = self.reviewer_manager.assign_reviewers(submission)
        self.evaluation_manager.evaluate(submission, assigned)
