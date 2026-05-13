class NotificationService:
    # diagram: EvaluationManager -> NotificationService: notify(researcher, decision)
   
    def notify(self, researcher, decision):
        print("[NotificationService] notify")
        # routeByDecision(decision) in the diagram is a single-arg self call, so it only sees the decision. notify() composes the final message by combining the routed outcome text with the submission title held on the researcher.
        outcome_text = self.route_by_decision(decision)
        title = (
            researcher.current_submission.title
            if researcher.current_submission is not None
            else "your submission"
        )
        message = f"'{title}' {outcome_text}"
        self._send(researcher, message)

    def route_by_decision(self, decision):
        print("[NotificationService] routeByDecision")
        if decision == "accepted":
            return "has been ACCEPTED"
        if decision == "rejected":
            return "has been REJECTED"
        if decision == "revision":
            return "requires REVISION"
        return "has an unknown outcome"

    def _send(self, researcher, message):
        print("[NotificationService] sendNotification")
        researcher.receive_notification(message)
