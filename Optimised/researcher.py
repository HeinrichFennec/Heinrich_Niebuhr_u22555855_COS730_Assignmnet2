class Researcher:
    def __init__(self, name):
        self.name = name
        self.notifications = []
        self.errors = []
        # remembered so NotificationService can build a title-aware message while matching the diagram signature notify(researcher, decision)
        self.current_submission = None

    def submit_research_output(self, ui, submission):
        print(f"[Researcher] submitResearchOutput({submission.submission_id})")
        self.current_submission = submission
        ui.submit_research_output(self, submission)

    def receive_notification(self, message):
        # receives the diagram's NotificationService -> Researcher: sendNotification(decision) arrow
        self.notifications.append(message)

    def display_error(self, message):
        print(f"[Researcher] displayError: {message}")
        self.errors.append(message)
