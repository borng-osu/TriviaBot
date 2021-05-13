from tkinter import *
from chat import chat, bot_name

MAIN_BG = "#474647"
SECOND_BG = "#3E5A79"
TEXT = "#EDFDFA"

HEAD_FONT = "Helvetica 13 bold"
FONT = "Helvetica 12"

class TriviaBot:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("TriviaBot")
        self.window.resizable(width=False,height=False)
        self.window.configure(width=520, height=640, bg=MAIN_BG)

        # creates header
        header = Label(self.window, bg=MAIN_BG, fg=TEXT, text="Welcome to TriviaBot", font=HEAD_FONT, pady=15)
        header.place(relwidth=1)

        # creates div
        line = Label(self.window, width=480, bg=SECOND_BG)
        line.place(relwidth=1, rely=0.08, relheight=0.012)

        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=MAIN_BG, fg=TEXT, font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)

        # scrolling functionality
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)

        # bottom label
        bottom_label = Label(self.window, bg=SECOND_BG, height=90)
        bottom_label.place(relwidth=1, rely=0.825)

        # message input
        self.msg_entry = Entry(bottom_label, bg="#EDFDFA", fg="#1F1E1F", font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter)

        # send button
        send_btn = Button(bottom_label, text="Send", fg="#1F1E1F", font=HEAD_FONT, width=20, bg=SECOND_BG, command=lambda: self._on_enter(None))
        send_btn.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    def _on_enter(self, event):
        msg = self.msg_entry.get()
        self._insert_msg(msg, "You")

    def _insert_msg(self, msg, sender):
        if not msg:
            return
        
        self.msg_entry.delete(0, END)

        msg_disp = f"{sender}: {msg}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg_disp)
        self.text_widget.configure(state=DISABLED)

        response = f"{bot_name}: {chat(msg)}\n\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, response)
        self.text_widget.configure(state=DISABLED)

if __name__ == "__main__":
    app = TriviaBot()
    app.run()