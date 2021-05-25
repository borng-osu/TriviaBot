from tkinter import *
from tkinter import filedialog
from chat import chat, bot_name

MAIN_BG = "#474647"
SECOND_BG = "#3E5A79"
TEXT = "#EDFDFA"

HEAD_FONT = "Helvetica 13 bold"
FONT = "Helvetica 12"
ABOUT = "TEST!"

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

        # creates header space
        header = Label(self.window, bg=MAIN_BG, height=35)
        header.place(relwidth=1)

        # creates header label
        header_lbl = Label(header, text="Welcome to TriviaBot", font=HEAD_FONT, fg=TEXT, bg=MAIN_BG, pady=15)
        header_lbl.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)

        # hover info
        info_btn = Button(header, text="How To", fg="#1F1E1F", font=HEAD_FONT, width=20, bg=SECOND_BG, command=self.click)
        info_btn.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

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

    def _on_enter(self, e):
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

    def click(e):
        pop = Toplevel()
        pop.title("How to TriviaBot")
        pop.geometry("350x450")
        pop.configure(bg=SECOND_BG)

        head = Label(pop, height=50)
        head.place(relwidth=1)

        title = Label(head, text="TriviaBot Commands", font=HEAD_FONT, fg=TEXT, bg=MAIN_BG, pady=1)
        title.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)

        body = Text(pop, height=200, bg=MAIN_BG, fg=TEXT, font=FONT)
        body.place(relwidth=1, rely=0.2)

        info = open("howto.txt", 'r')
        data = info.read()
        body.insert(END, data)
        info.close()

        scroll = Scrollbar(body)
        scroll.place(relheight=1, relx=0.974)
        scroll.configure(command=body.yview)


        body.configure(cursor="arrow", state=DISABLED)


    

if __name__ == "__main__":
    app = TriviaBot()
    app.run()