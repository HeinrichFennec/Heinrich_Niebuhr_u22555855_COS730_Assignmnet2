class Researcher:
    def __init__(self, name):
        self.name = name
        self.notifications = []

    def submit_research_output(self, ui, submission):
        print(f"[Researcher] submitResearchOutput({submission.submission_id})")
        ui.submit_research_output(submission)

    def receive_notification(self, message):
        # here  i receive the diagram's NotificationService -> Researcher: sendNotification() arrow
        self.notifications.append(message)