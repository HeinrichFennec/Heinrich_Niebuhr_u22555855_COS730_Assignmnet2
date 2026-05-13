class NotificationService:
    def __init__(self, researcher):
        self.researcher = researcher

    def notify_acceptance(self, submission):
        print("[NotificationService] notifyAcceptance")
        self._send(f"'{submission.title}' has been ACCEPTED")

    def notify_rejection(self, submission):
        print("[NotificationService] notifyRejection")
        self._send(f"'{submission.title}' has been REJECTED")

    def notify_revision(self, submission):
        print("[NotificationService] notifyRevision")
        self._send(f"'{submission.title}' requires REVISION")

    def _send(self, message):
        print("[NotificationService] sendNotification")
        self.researcher.receive_notification(message)
