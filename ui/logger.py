import os
import re
import tkinter as tk
import datetime


class Logger:
    def __init__(self, text_widget=None, log_dir="./logs"):
        self.text_widget = text_widget

        os.makedirs(log_dir, exist_ok=True)

        self.log_filename = f"./{log_dir}/log_{datetime.datetime.now().strftime('%Y%m%d')}.txt"
        self.ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')

    def set_text_widget(self, text_widget):
        self.text_widget = text_widget

    def message(self, *msgs):
        combined_msg = " ".join(str(m) for m in msgs)
        self.print_log(combined_msg)

    def server_message(self, *msgs):
        combined_msg = " ".join(str(m) for m in msgs)
        clean_message = self.ansi_escape.sub('', combined_msg)
        self.print_log(clean_message)

    def print_log(self, clean_message):
        if self.text_widget:
            self.text_widget.configure(state="normal")
            self.text_widget.insert(tk.END, clean_message + "\n")
            self.text_widget.see(tk.END)
            self.text_widget.configure(state="disabled")

        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_line = f"[{timestamp}] {clean_message}\n"

        with open(self.log_filename, "a", encoding="utf-8") as log_file:
            log_file.write(log_line)

    def message_error(self, message):
        self.message(message)


global_logger = Logger()
