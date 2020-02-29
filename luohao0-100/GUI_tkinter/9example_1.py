import tkinter as tk
import pickle
from tkinter import messagebox


def set_win_center(root, win_width=200, win_height=100):
    """
    将窗口居中
    :param root:主窗体的实例tk.Tk()
    :param win_width: 主窗口的宽度，默认200
    :param win_height: 主窗口长度，默认100
    :return:
    """

    screen_width, screen_height = root.maxsize()
    cen_x = (screen_width - win_width) / 2
    cen_y = (screen_height - win_height) / 2
    size_xy = '%dx%d+%d+%d' % (win_width, win_height, cen_x, cen_y)
    root.geometry(size_xy)


window = tk.Tk()
window.title('Welcome to My Python')
set_win_center(window, 680, 500)
window.resizable(0, 0) # 禁止拉伸

# welcome image
canvas = tk.Canvas(window, width=680, height=300)
image_file = tk.PhotoImage(file='welcome.png')
image = canvas.create_image(0, 0, anchor='nw', image=image_file)
canvas.pack(side='top')

# label
tk.Label(window, text='User name:', font=('Times', 20)).place(x=50, y=300)
tk.Label(window, text='Password:', font=('Times', 20)).place(x=50, y=350)

# entry
var_user_name = tk.StringVar()
var_user_pwd = tk.StringVar()
var_user_name.set('example:xxxx@163.com')
entry_user_name = tk.Entry(window, textvariable=var_user_name, width=25, font=('Times', 20))
entry_user_name.place(x=210, y=300)
entry_user_pwd = tk.Entry(window, textvariable=var_user_pwd, width=25, font=('Times', 20), show='*')
entry_user_pwd.place(x=210, y=350)


def usr_login():
    usr_name = var_user_name.get()
    usr_pwd = var_user_pwd.get()
    # 创建用户名字典文件，如果没有创建就先创建一个，默认加入一个admin管理员的账号
    try:
        with open('usrs_info.pickle', 'rb') as usr_file:
            usrs_info = pickle.load(usr_file)
    except FileNotFoundError:
        with open('usrs_info.pickle', 'wb') as usr_file:
            usrs_info = {'admin': 'admin'}
            pickle.dump(usrs_info, usr_file)

    if usr_name in usrs_info:
        if usr_pwd == usrs_info[usr_name]:
            tk.messagebox.showinfo(title='Welcome', message='How are you?' + usr_name)
        elif usr_pwd == '':
            tk.messagebox.showinfo(title='Error!', message='Your have not input your password.')
        else:
            tk.messagebox.showerror(message='Error! Your password is wrong, try again.')
    else:
        is_sign_up = tk.messagebox.askyesno(title='Welcome', message='You have not sign up yet. Sign up today?')
        if is_sign_up:
            usr_sign_up()


def usr_sign_up():
    def sign_to_my_python():
        nn = new_name.get()
        np = new_pwd.get()
        np_c = new_pwd_comfirm.get()
        with open('usrs_info.pickle', 'rb') as usr_file:
            exist_usrs_info = pickle.load(usr_file)
        # 先判断密码输入是否一样
        if np != np_c:
            tk.messagebox.showerror('Error!', 'Password and confirm password must be the same!')
        # 再判断是否已存在用户名
        elif nn in exist_usrs_info:
            tk.messagebox.showerror('Error', 'The user name has already exist sign up, try another name.')
        # 正确输入，注册成功
        else:
            exist_usrs_info[nn] = np
            with open('usrs_info.pickle', 'wb') as usr_file:
                pickle.dump(exist_usrs_info, usr_file)
            tk.messagebox.showinfo('Welcome!', 'You have successfully sign up')
            # window摧毁
            window_sign_up.destroy()

    window_sign_up = tk.Toplevel(window) # 弹窗
    window_sign_up.title('Sign up window')
    set_win_center(window_sign_up, 350, 200)
    window_sign_up.resizable(0, 0)

    new_name = tk.StringVar()
    new_name.set('example:xxx@163.com')
    new_pwd = tk.StringVar()
    new_pwd_comfirm = tk.StringVar()
    tk.Label(window_sign_up, text='User name:', font=('Times', 13)).place(x=10, y=10)
    entry_new_name = tk.Entry(window_sign_up, textvariable=new_name, font=('Times', 13), width=20).place(x=150, y=10)
    tk.Label(window_sign_up, text='Password:', font=('Times', 13)).place(x=10, y=50)
    entry_new_pwd = tk.Entry(window_sign_up, textvariable=new_pwd, font=('Times', 13),
                             width=20, show='*').place(x=150, y=50)
    tk.Label(window_sign_up, text='Confirm password:', font=('Times', 13)).place(x=10, y=90)
    entry_new_pwd = tk.Entry(window_sign_up, textvariable=new_pwd_comfirm, font=('Times', 13),
                             width=20, show='*').place(x=150, y=90)

    btn_confirm_sign_up=tk.Button(window_sign_up, text='Sign up', font=('Times', 15), command=sign_to_my_python)
    btn_confirm_sign_up.place(x=135, y=130)


# login button
btn_login = tk.Button(window, text='Login', font=('Times', 18), command=usr_login)
btn_login.place(x=170, y=400)
btn_sign_up = tk.Button(window, text='Sign up', font=('Times', 18), command=usr_sign_up)
btn_sign_up.place(x=370, y=400)


window.mainloop()

