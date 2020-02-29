import tkinter as tk

window = tk.Tk()
window.title('myWindow')
window.geometry('300x200')

l = tk.Label(window, text='you choose nothing', width=20)
l.pack()

def print_selection():
    if var1.get() == 1 and var2.get() == 0:
        l.config(text='you choose Python')
    elif var1.get() == 0 and var2.get() == 1:
        l.config(text='you choose C++')
    elif var1.get() == 1 and var2.get() == 1:
        l.config(text='you choose Python,C++')
    else:
        l.config(text='you choose nothing')


var1 = tk.IntVar()
var2 = tk.IntVar()

# checkbutton 选中为1未选中为0，需要有一个标记
cb1 = tk.Checkbutton(window, text='Python', variable=var1, onvalue=1, offvalue=0,
                     command=print_selection)
cb2 = tk.Checkbutton(window, text='C++', variable=var2, onvalue=1, offvalue=0,
                     command=print_selection)
cb1.pack()
cb2.pack()

window.mainloop()
