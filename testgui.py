from tkinter import *
from datetime import datetime

root = Tk()
root.config(bg="lightblue")

canvas = Canvas(root, width=200, height=200,bg="white")
canvas.grid(row=0,column=0,columnspan=2)

bubbles = []

class BotBubble:
    def __init__(self,master,message=""):
        self.master = master
        self.frame = Frame(master,bg="light grey")
        self.i = self.master.create_window(90,160,window=self.frame)
        Label(self.frame, text=message,font=("Helvetica", 9),bg="light grey").grid(row=1, column=0,sticky="w",padx=5,pady=3)
        root.update_idletasks()
        
def send_message():
    if bubbles:
        canvas.move(ALL, 0, -65)
    a = BotBubble(canvas,message=entry.get())
    bubbles.append(a)

entry = Entry(root,width=26)
entry.grid(row=1,column=0)
Button(root,text="Send",command=send_message).grid(row=1,column=1)
root.mainloop()