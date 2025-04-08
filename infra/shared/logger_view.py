import tkinter as tk

class LoggerView:
    def __init__(self):
        self.text_widget = None

    def bind(self, text_widget):
        self.text_widget = text_widget

    def display(self, msg):
        if self.text_widget:
            self.text_widget.configure(state="normal")
            self.text_widget.insert(tk.END, msg + "\n")
            self.text_widget.configure(state="disabled")
            self.text_widget.see(tk.END)
