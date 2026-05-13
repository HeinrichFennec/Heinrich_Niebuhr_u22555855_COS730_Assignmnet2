from submission import Submission
from researcher import Researcher
from ui import UI
from submission_controller import SubmissionController
from validator import Validator
from submission_repository import SubmissionRepository
from reviewer_repository import ReviewerRepository
from reviewer_manager import ReviewerManager
from reviewer import Reviewer
from evaluation_manager import EvaluationManager
from notification_service import NotificationService


def build_system(reviewer_pool):
    submission_repo = SubmissionRepository()
    reviewer_repo = ReviewerRepository(reviewer_pool)
    researcher = Researcher("Dr Khumalo")
    notifier = NotificationService()
    rm = ReviewerManager(reviewer_repo)
    evaluator = EvaluationManager(submission_repo, rm, notifier, researcher)
    controller = SubmissionController(Validator(), submission_repo, rm, evaluator)
    ui = UI(controller)
    return researcher, ui


def run_invalid():
    print("\n--- invalid submission ---")
    pool = [Reviewer("R1", "Alice"), Reviewer("R2", "Bongani")]
    researcher, ui = build_system(pool)
    bad = Submission("S001", "", "", "x", "Dr Khumalo")
    researcher.submit_research_output(ui, bad)


def run_accept():
    print("\n--- valid submission, expecting acceptance ---")
    pool = [
        Reviewer("R1", "Alice", bias=2.5),
        Reviewer("R2", "Bongani", bias=2.5),
        Reviewer("R3", "Chen", bias=2.5),
    ]
    researcher, ui = build_system(pool)
    sub = Submission("S002", "On Optimisation", "abstract here",
                     "lorem ipsum dolor sit amet " * 4, "Dr Khumalo")
    researcher.submit_research_output(ui, sub)
    print(f"inbox: {researcher.notifications}")


def run_revision():
    print("\n--- valid submission, expecting revision ---")
    pool = [
        Reviewer("R1", "Alice", bias=-1.0),
        Reviewer("R2", "Bongani", bias=0.5),
        Reviewer("R3", "Chen", bias=-0.5),
    ]
    researcher, ui = build_system(pool)
    sub = Submission("S003", "Mediocre Study", "abstract",
                     "filler content goes here " * 4, "Dr Khumalo")
    researcher.submit_research_output(ui, sub)
    print(f"inbox: {researcher.notifications}")

def run_reject():
    print("\n--- valid submission, expecting rejection ---")
    pool = [
        Reviewer("R1", "Alice", bias=-4.0),
        Reviewer("R2", "Bongani", bias=-4.0),
        Reviewer("R3", "Chen", bias=-4.0),
    ]
    researcher, ui = build_system(pool)
    sub = Submission("S004", "Flawed Methodology", "abstract",
                     "filler content here goes " * 4, "Dr Khumalo")
    researcher.submit_research_output(ui, sub)
    print(f"inbox: {researcher.notifications}")


if __name__ == "__main__":
    run_invalid()
    run_accept()
    run_reject()
    run_revision()
