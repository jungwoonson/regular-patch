import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait


class BrowserController:
    def __init__(self, url, username, password, company_code, is_v03=False):
        self.url = url
        self.username = username
        self.password = password
        self.company_code = company_code
        self.is_v03 = is_v03
        self.driver = None

    def start_driver(self):
        options = Options()
        self.driver = webdriver.Chrome(options=options)

    def login(self):
        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "S_USER_ID"))
        )
        password_input = self.driver.find_element(By.ID, "S_PWD")
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)

        if self.is_v03:
            company_code_input = self.driver.find_element(By.ID, "S_C_CD")
            company_code_input.send_keys(self.company_code)

        password_input.send_keys(Keys.RETURN)

    def move_system_menu(self, is_v03=False):
        sys_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[module_id="sys"]'))
        )
        sys_element.click()
        select_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "PROFILE_ID_MENU"))
        )

        if is_v03:
            time.sleep(2)

        select = Select(select_box)
        select.select_by_value("HR_Admin")
        time.sleep(1)

    def patch_db(self):
        self.start_driver()
        self.driver.get(self.url)
        self.login()
        self.move_system_menu(self.is_v03)
        element = self.driver.find_element(By.CSS_SELECTOR, 'span[menu_id="Jsys1919"]')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
        iframe = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "iframe_biz_sysJsys1919"))
        )
        self.driver.switch_to.frame(iframe)
        time.sleep(1)
        patch_all_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.ID, "import"))
        )
        patch_all_button.click()

    def create_multilingual(self):
        self.start_driver()
        self.driver.get(self.url)
        self.login()
        self.move_system_menu()
        element = self.driver.find_element(By.CSS_SELECTOR, 'span[menu_id="sys121b"]')
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        element.click()
