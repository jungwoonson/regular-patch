from domain.config import Config
from infra.browser_controller import BrowserController


class BrowserService:

    def __init__(self, config: Config):
        self.controller = BrowserController(config)

    def start_db_patch(self):
        self.controller.patch_db()

    def patch_multilingual(self):
        self.controller.create_multilingual()