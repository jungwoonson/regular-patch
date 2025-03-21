import tkinter as tk
from tkinter import filedialog, messagebox
import threading
from ui.logger import global_logger

class PatchGUI:
    def __init__(self, set_source_callback=None):
        self.set_source_callback = set_source_callback
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

        browse_button = tk.Button(self.patch_frame, text="패치루트선택", width=15, command=self.browse_directory)
        browse_button.grid(row=0, column=1, padx=10, pady=10)

        # 회사명 버튼들
        self.button_frame = tk.Frame(self.top_frame)
        self.button_frame.pack(side="top", fill="x", expand=False, padx=10)

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

        global_logger.set_text_widget(self.log_text)
        self.logger = global_logger

    def browse_directory(self):
        dir_path = filedialog.askdirectory(title="패치폴더선택")
        if dir_path:
            self.source_dir_input.configure(state="normal")
            self.source_dir.set(dir_path)
            self.source_dir_input.configure(state="readonly")
            if self.set_source_callback:
                self.set_source_callback(dir_path)

    def create_config_buttons(self, config_list):
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        for idx, config in enumerate(config_list):
            btn = tk.Button(
                self.button_frame,
                text=config.company_name,
                width=20,
            )
            btn.config(command=lambda c=config, b=btn: on_company_click(c, b))
            btn.pack(side="left", padx=5)

        def on_company_click(conf, button):
            if self.selected_button is not None:
                self.selected_button.config(bg="SystemButtonFace")
            button.config(bg="#90ee90")
            self.selected_button = button
            self.show_config_details(conf)
            self.update_action_buttons(conf)
            self.logger.message(f"서버 변경: [{conf.company_name}] {conf.remote_host}:{conf.remote_port}")

    def show_config_details(self, config):
        remote_mapping = {
            "remote_host": "HOST",
            "remote_port": "PORT",
            "remote_username": "USER",
            "remote_webroot": "WebRoot경로",
            "jdk_version": "JDK Version"
        }
        remote_info = []
        for key, label in remote_mapping.items():
            remote_info.append(f"{label}: {config.get(key)}")
        remote_text = "\n".join(remote_info)
        self.remote_label.config(text=remote_text)

        browser_keys = {
            "browser_url": "URL",
            "browser_id": "ID",
        }
        browser_info = []
        for key, label in browser_keys.items():
            browser_info.append(f"{label}: {config.get(key)}")
        browser_text = "\n".join(browser_info)
        self.browser_label.config(text=browser_text)

    def init_action_buttons(self, config_list, commands):
        def createActionButton(button_text, command_name, color=None):
            button = tk.Button(
                self.custom_frame,
                text=button_text,
                command=lambda a=config: threading.Thread(target=commands.get(command_name), args=(a,), ).start()
            )

            if color:
                button.config(bg=color)

            return button

        def createDobulCheckButton(text, command_name, color, conf=None):
            def on_click():
                result = messagebox.askyesno("확인", f"{text} 정말 실행하시겠습니까?")
                if result:
                    threading.Thread(
                        target=commands.get(command_name),
                        args=(conf,),
                    ).start()

            return tk.Button(
                self.custom_frame,
                text=text,
                bg=color,
                command=on_click
            )

        for idx, config in enumerate(config_list):
            if not config.is_mobile():
                list_import_btn = createActionButton("patch_list_import.sql 전송", "send_list_import", "#B0E0E6")
                self.action_btns[f"{config.company_name}_patch_list_import_btn"] = list_import_btn

                start_patch_btn = createActionButton("DB패치실행", "start_db_patch", "#B0E0E6")
                self.action_btns[f"{config.company_name}_start_db_patch"] = start_patch_btn

            send_webroot_btn = createDobulCheckButton("WebRoot전송", "send_webroot", "#C8E6C9", config)
            self.action_btns[f"{config.company_name}_send_webroot"] = send_webroot_btn

            send_classes_btn = createDobulCheckButton("classes전송", "send_classes", "#C8E6C9", config)
            self.action_btns[f"{config.company_name}_send_classes"] = send_classes_btn

            deploy_properties_btn = createDobulCheckButton("시스템프로퍼티수정", "deploy_properties", "#C8E6C9", config)
            self.action_btns[f"{config.company_name}_deploy_properties"] = deploy_properties_btn

            stop_server_btn = createDobulCheckButton("서버종료", "stop_server", "#FFDAB9", config)
            self.action_btns[f"{config.company_name}_stop_server"] = stop_server_btn

            start_server_btn = createDobulCheckButton("서버시작", "start_server", "#FFDAB9", config)
            self.action_btns[f"{config.company_name}_start_server"] = start_server_btn

            check_server_btn = createActionButton("서버프로세스확인", "check_server_process", "#FFFACD")
            self.action_btns[f"{config.company_name}_check_server_process"] = check_server_btn

            start_log_btn = createActionButton("서버로그시작", "start_server_log", "#FFFACD")
            self.action_btns[f"{config.company_name}_start_server_log"] = start_log_btn

            stop_log_btn = createActionButton("서버로그종료", "stop_server_log", "#FFFACD")
            self.action_btns[f"{config.company_name}_stop_server_log"] = stop_log_btn


    def update_action_buttons(self, config):

        for btn in self.action_btns.values():
            btn.pack_forget()

        prefix = f"{config.company_name}_"
        for key, btn in self.action_btns.items():
            if key.startswith(prefix):
                btn.pack(fill="x", pady=5)

    def run(self):
        self.root.mainloop()
