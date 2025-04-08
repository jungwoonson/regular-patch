from infra.shared.logger import Logger
from service.browser_controller import BrowserController

class BrowserAutomator:
    def __init__(self):
        pass

    def start_db_patch(self, config):
        controller = self.create_browser_controller(config)
        Logger().server_log(f"[{config.company_name}] DB 패치 시작")
        controller.patch_db()

    def patch_multilingual(self, config):
        controller = self.create_browser_controller(config)
        Logger().server_log(f"[{config.company_name}] 다국어 생성 시작")
        controller.create_multilingual()

    def create_browser_controller(self, config):
        return BrowserController(
            config.browser_url,
            config.browser_id,
            config.browser_pw,
            config.company_code,
            config.is_v03()
        )
