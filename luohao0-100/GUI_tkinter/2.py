import tkinter as tk
from tkinter import messagebox

class Window(object):
    def __init__(self, handle):
        self.win = handle
        self.win.title('***一个窗口***')
        # self.win.geometry('400x200')
        self.createwindow()
        self.run()

    def createwindow(self):
        # Frame
        self.panel1 = tk.Frame(self.win)
        self.panel1.pack()
        self.panel2 = tk.Frame(self.win)
        self.panel2.pack()
        self.panel3 = tk.Frame(self.win)
        self.panel3.pack()
        # label 1

        self.label1 = tk.Label(self.panel1, text='data path:', font=20)
        self.label1.pack(side='left')
        self.label2 = tk.Label(self.panel2, text='save path:', font=20)
        self.label2.pack(side='left')

        # text_entry
        self.entry1_text = tk.StringVar()
        self.entry1 = tk.Entry(self.panel1, textvariable=self.entry1_text, width=50)
        self.entry1.pack(side='right')
        self.entry2_text = tk.StringVar()
        self.entry2 = tk.Entry(self.panel2, textvariable=self.entry2_text, width=50)
        self.entry2.pack(side='right')

        # button
        self.button1 = tk.Button(self.panel3, text="Start", font=10, width=6, height=2)
        self.button1.pack(side='left')
        self.button2 = tk.Button(self.panel3, text="Quit", font=10, width=6, height=2,
                                 command=self.confirm_to_quit)
        self.button2.pack(side='right')

    def setlabel(self):
        pass

    def confirm_to_quit(self):
        if tk.messagebox.askyesnocancel('Notice', 'Are you sure to quit?'):
            self.win.quit()

    def run(self):
        try:
            self.win.mainloop()
        except Exception as e:
            print("*** exception:\n".format(e))


def main():
    window = tk.Tk()
    Window(window).run()


if __name__ == '__main__':
    main()
