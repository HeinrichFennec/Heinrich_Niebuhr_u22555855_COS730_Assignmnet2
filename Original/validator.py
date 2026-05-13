from submission import Submission


class Validator:
    def validate_format(self, submission):
        print("[Validator] validateFormat")
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
