import tkinter as tk

window = tk.Tk()
window.title('mywindow')
window.geometry('300x200')

tk.Label(window, text='On the window', bg='red').pack()

frm = tk.Frame(window)
frm.pack()
frm_1 = tk.Frame(frm)
frm_r = tk.Frame(frm)
frm_1.pack(side='left')
frm_r.pack(side='right')

tk.Label(frm_1, text='on the frm_l1').pack()
tk.Label(frm_1, text='on the frm_l2').pack()
tk.Label(frm_1, text='on the frm_l3').pack()
tk.Label(frm_r, text='on the frm_r', bg='yellow').pack()

window.mainloop()

