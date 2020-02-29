import tkinter as tk

window = tk.Tk()
window.title('mywindow')
window.geometry('300x200')

var1 = tk.StringVar()
label1 = tk.Label(window,text='empty', bg='yellow', width=20)
label1.pack()


def print_selection():
    label1.config(text='you have selected' + var1.get())


# radiobutton 多个button共用一个var，随时改动
rb1 = tk.Radiobutton(window, text='Option A', variable=var1,
                     value='A', command=print_selection)
rb1.pack()
rb2 = tk.Radiobutton(window, text='Option B', variable=var1,
                     value='B', command=print_selection)
rb2.pack()
rb3 = tk.Radiobutton(window, text='Option C', variable=var1,
                     value='C', command=print_selection)
rb3.pack()

tk.mainloop()