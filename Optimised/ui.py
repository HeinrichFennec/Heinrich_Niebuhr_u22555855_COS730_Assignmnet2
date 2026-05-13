class UI:
    def __init__(self, controller):
        self.controller = controller
        self.last_error = None
        # set per submission so return_error can route the display_error arrow back to the researcher (UI -> Researcher: display error in the diagram)
        self.current_researcher = None

    def submit_research_output(self, researcher, submission):
        print("[UI] submit")
        self.current_researcher = researcher
        self.controller.submit(submission, self)

    def return_error(self, message):
        print(f"[UI] error: {message}")
        self.last_error = message
        # diagram: UI -> Researcher: display error
        if self.current_researcher is not None:
            self.current_researcher.display_error(message)
