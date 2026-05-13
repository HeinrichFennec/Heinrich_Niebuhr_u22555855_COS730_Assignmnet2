from submission import Submission


class Validator:
    def validate_format(self, submission):
        print("[Validator] validateFormat")
        # maps to the submission format decision table (task 3) rule R1 (all four conditions hold) -> valid, R2..R5 -> invalid
        if not isinstance(submission, Submission):
            return False
        if not submission.submission_id:
            return False
        if not submission.title.strip():
            return False
        if not submission.author.strip():
            return False
        if len(submission.content.strip()) < 10:
            return False
        return True
