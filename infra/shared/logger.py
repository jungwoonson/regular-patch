from infra.shared.logger_model import LoggerModel
from infra.shared.logger_view import LoggerView


class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.model = LoggerModel()
            cls._instance.view = LoggerView()
        return cls._instance

    def bind_text_widget(self, widget):
        self.view.bind(widget)

    def log(self, *msgs):
        message = " ".join(str(m) for m in msgs)
        self.model.save(message)
        self.view.display(message)

    def server_log(self, *msgs):
        message = " ".join(str(m) for m in msgs)
        clean_message = self.model.clean(message)
        self.model.save(clean_message)
        self.view.display(clean_message)
