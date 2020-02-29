import tkinter
import tkinter.messagebox

def main():
    flag = True

    # 修改标签上的文字
    def change_label_text():
        nonlocal flag
        flag = not flag
        if flag:
            color, msg = ('red', 'Hello, world!')
        else:
            color, msg = ('blue', 'Goodbye, world!')
        label.config(text=msg, fg=color)

    #  确认退出
    def confirm_to_quit():
        if tkinter.messagebox.askyesnocancel('温馨提示', '确定要退出吗？'):
            window.quit()

    # 创建顶层窗口
    window = tkinter.Tk()
    # size
    window.geometry('240x160')
    # title
    window.title('小游戏')
    # 创建标签对象并添加到顶层窗口
    label = tkinter.Label(window, text='Hello, world!', bg='grey', font=('Arial', 22), fg='red')
    label.pack(expand=1)

    # 创建一个装按钮的容器，多个button放一起
    panel = tkinter.Frame(window)
    buttton1 = tkinter.Button(panel, text='修改', width=15, height=2, command=change_label_text)
    buttton1.pack(side='left')
    buttton2 = tkinter.Button(panel, text='退出',width=15, height=2, command=confirm_to_quit)
    buttton2.pack(side='right')
    panel.pack(side='bottom')
    tkinter.mainloop()


if __name__ == '__main__':
    main()