class UI:
    def __init__(self, controller):
        self.controller = controller
        self.last_error = None

    def submit_research_output(self, submission):
        print("[UI] submit")
        self.controller.submit(submission, self)

    def return_error(self, message):
        print(f"[UI] error: {message}")
        self.last_error = message
