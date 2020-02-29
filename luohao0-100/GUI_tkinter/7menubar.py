import tkinter as tk

window = tk.Tk()
window.title('mywindow')
window.geometry('300x200')

l1 = tk.Label(window, text='', bg='yellow', width=10).pack()


def new_file():
    pass

def open_file():
    pass

def save_file():
    pass

def comfirm_to_quit():
    window.quit()

def cut_file():
    pass

def copy_file():
    pass

def paste_file():
    pass

# Menubar
# 菜单栏1
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=0) #tearoff表示是否可展开
menubar.add_cascade(label='Flie', menu=filemenu)
filemenu.add_command(label='New', command=new_file)
filemenu.add_command(label='Open', command=open_file)
filemenu.add_command(label='Save', command=save_file)
filemenu.add_separator() # 分割线
filemenu.add_command(label='Exit', command=comfirm_to_quit)

# 菜单栏2
editmenu = tk.Menu(menubar, tearoff=0) #tearoff表示是否可展开
menubar.add_cascade(label='Edit', menu=editmenu)
editmenu.add_command(label='Cut', command=cut_file)
editmenu.add_command(label='Copy', command=copy_file)
editmenu.add_command(label='Paste', command=paste_file)

# 菜单栏下加子单元
submenu = tk.Menu(editmenu,tearoff=0)
editmenu.add_cascade(label='Import', menu=submenu, underline=1)
submenu.add_command(label='submenu1')


# 改变window的菜单参数
window.config(menu=menubar)
window.mainloop()
