import tkinter as tk

window = tk.Tk()
window.title('myWindow')
window.geometry('300x200')

var = tk.StringVar()
l1 = tk.Label(window, bg='yellow', width=20, text='empty')
l1.pack()


def print_selection(v):
    l1.config(text='you have selected'+v)


# scale：标签、数值范围、横竖朝向、长短、是否显示取值、单位标量,精度
scale1 = tk.Scale(window, label='try me', from_=5, to=20, orient=tk.HORIZONTAL,
                  length=200, showvalue=0, tickinterval=5, resolution=0.001,
                  command=print_selection)
scale1.pack()

window.mainloop()
