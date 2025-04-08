import threading
import tkinter as tk
from tkinter import filedialog, messagebox
from typing import List

from domain.config import Config
from ui.button_command import ButtonCommand


class PatchGUI:
    def __init__(self, remote_names: List[str], button_command: ButtonCommand):
        self.button_command = button_command
        self.action_btns = {}

        self.root = tk.Tk()
        self.root.title("패치 프로그램")
        self.root.geometry("1200x700")

        # 선택된 회사명 버튼을 추적하기 위한 변수
        self.selected_button = None

        # 상단 프레임: 패치루트 선택 + 회사명 버튼들
        self.top_frame = tk.Frame(self.root)
        self.top_frame.pack(side="top", fill="x", expand=False)

        # 패치루트 선택
        self.patch_frame = tk.Frame(self.top_frame)
        self.patch_frame.pack(side="top", fill="x", expand=False)

        self.patch_frame.columnconfigure(0, weight=1)
        self.patch_frame.columnconfigure(1, weight=0)

        self.source_dir = tk.StringVar()
        self.source_dir_input = tk.Entry(self.patch_frame, textvariable=self.source_dir, state="readonly")
        self.source_dir_input.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        browse_button = tk.Button(self.patch_frame, text="패치폴더선택", width=15, command=self.__browse_directory)
        browse_button.grid(row=0, column=1, padx=10, pady=10)

        # 회사명 버튼들
        self.company_button_frame = tk.Frame(self.top_frame)
        self.company_button_frame.pack(side="top", fill="x", expand=False, padx=10)
        self.__create_company_buttons(remote_names)

        # 메인 content 프레임
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(side="top", fill="both", expand=True)

        # content_frame을 3행 x 2열로 구성
        # row=0,1: 왼쪽(Server/Browser), 오른쪽(파란 박스)
        # row=2   : 로그 (colspan=2)
        self.content_frame.rowconfigure(0, weight=0)
        self.content_frame.rowconfigure(1, weight=0)
        self.content_frame.rowconfigure(2, weight=1)
        self.content_frame.columnconfigure(0, weight=1)  # 왼쪽 확장
        self.content_frame.columnconfigure(1, weight=0)  # 오른쪽은 확장하지 않음

        # Server Info (왼쪽 상단)
        self.remote_frame = tk.LabelFrame(self.content_frame, text="Server Info", padx=10, pady=10)
        self.remote_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))

        self.remote_label = tk.Label(self.remote_frame, anchor="nw", justify="left")
        self.remote_label.pack(fill="both", expand=True)

        # Web Info (왼쪽 중단)
        self.browser_frame = tk.LabelFrame(self.content_frame, text="Web Info", padx=10, pady=10)
        self.browser_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        self.browser_label = tk.Label(self.browser_frame, anchor="nw", justify="left")
        self.browser_label.pack(fill="both", expand=True)

        # 파란 박스 (오른쪽)
        self.custom_frame = tk.LabelFrame(
            self.content_frame,
            text="Actions",
            bg="lightblue",
            padx=10,
            pady=10,
            width=200
        )
        # row=0, column=1, rowspan=2로 배치
        self.custom_frame.grid(row=0, column=1, rowspan=2, sticky="ns", padx=10, pady=5)
        # 내부 내용에 따라 크기가 변하지 않도록
        self.custom_frame.grid_propagate(False)

        # 로그 출력 (아래쪽)
        self.log_text = tk.Text(self.content_frame, state="disabled")
        self.log_text.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=10, pady=(5, 10))

    def __browse_directory(self):
        dir_path = filedialog.askdirectory(title="패치폴더선택")
        if dir_path:
            self.source_dir_input.configure(state="normal")
            self.source_dir.set(dir_path)
            self.source_dir_input.configure(state="readonly")
            self.button_command.set_patch_dir(dir_path)

    def __create_company_buttons(self, remote_names):
        for widget in self.company_button_frame.winfo_children():
            widget.destroy()

        for remote_name in remote_names:
            btn = tk.Button(
                self.company_button_frame,
                text=remote_name,
                width=20,
            )
            btn.config(command=lambda a=remote_name, b=btn: self.on_company_click(a, b))
            btn.pack(side="left", padx=5)

    def on_company_click(self, remote_name: str, button):
        if self.selected_button is not None:
            self.selected_button.config(bg="SystemButtonFace")
        button.config(bg="#90ee90")
        self.selected_button = button

        config: Config = self.button_command.choose_remote(remote_name)
        self.__show_config_details(config)
        self.__update_action_buttons(config)

    def __update_action_buttons(self, config: Config):

        for btn in self.action_btns.values():
            btn.pack_forget()

        prefix = f"{config.get_company_name()}_"
        for key, btn in self.action_btns.items():
            if key.startswith(prefix):
                btn.pack(fill="x", pady=5)

    def __show_config_details(self, config: Config):
        remote_info = [f"remote_host: {config.get_remote_host()}",
                       f"remote_port: {config.get_remote_port()}",
                       f"remote_username: {config.get_remote_username()}",
                       f"remote_webroot: {config.get_remote_webroot()}",
                       f"jdk_version: {config.get_jdk_version()}"]
        remote_text = "\n".join(remote_info)
        self.remote_label.config(text=remote_text)

        browser_info = [f"browser_url: {config.get_browser_url()}",
                        f"browser_id: {config.get_browser_id()}"]
        browser_text = "\n".join(browser_info)
        self.browser_label.config(text=browser_text)

    def __create_button(self, config, button_text, on_click, color=None):
        button = tk.Button(self.custom_frame, text=button_text, command=on_click)
        if color:
            button.config(bg=color)

        key = f"{config.company_name}_{button_text}"
        self.action_btns[key] = button

    def __create_immediate_button(self, config, button_text, command, color=None):
        def on_click():
            threading.Thread(target=command, args=config).start()

        self.__create_button(config, button_text, on_click, color)

    def __create_confirm_button(self, config, button_text, command, color=None):
        def on_click():
            if messagebox.askyesno("확인", f"{button_text} 정말 실행하시겠습니까?"):
                threading.Thread(target=command, args=config).start()

        self.__create_button(config, button_text, on_click, color)

    def init_action_buttons(self, config_list):
        for config in config_list:
            if not config.is_mobile():
                self.__create_immediate_button(config, "patch_list_import.sql 전송", self.button_command.transfer_patch_sql, "#B0E0E6")
                self.__create_immediate_button(config, "DB패치실행", self.button_command.start_browser_for_db_patch, "#B0E0E6")

            self.__create_confirm_button(config, "WebRoot전송", self.button_command.transfer_webroot, "#C8E6C9")
            self.__create_confirm_button(config, "classes전송", self.button_command.transfer_classes, "#C8E6C9")
            self.__create_confirm_button(config, "시스템프로퍼티수정", self.button_command.deploy_system_properties, "#C8E6C9")

            self.__create_confirm_button(config, "서버종료", self.button_command.stop_server, "#FFDAB9")
            self.__create_confirm_button(config, "서버시작", self.button_command.start_server, "#FFDAB9")

            self.__create_immediate_button(config, "서버프로세스확인", self.button_command.check_process, "#FFFACD")
            self.__create_immediate_button(config, "서버로그시작", self.button_command.start_server_log, "#FFFACD")
            self.__create_immediate_button(config, "서버로그종료", self.button_command.stop_server_log, "#FFFACD")

    def get_log_widget(self):
        return self.log_text

    def run(self):
        self.root.mainloop()
