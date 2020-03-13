import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
import pickle
from tool import Sub_Counts
import datetime
import os
import threading


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


def get_time():
    return '[' + str(datetime.datetime.now()) + ']'


window = tk.Tk()
window.title('字幕文件英文词频统计小程序')
set_win_center(window, 700, 600)
window.resizable(0, 0) # 禁止拉伸

# label
tk.Label(window, text='输入文件目录:', font=('微软雅黑', 12)).place(x=10, y=20)
tk.Label(window, text='输出保存目录:', font=('微软雅黑', 12)).place(x=10, y=120)
tk.Label(window, text='待处理文件:', font=('微软雅黑', 13)).place(x=10, y=240)
tk.Label(window, text='处理细节：', font=('微软雅黑', 13)).place(x=10, y=425)

# entry
var_input_path = tk.StringVar()
entry_input_path = tk.Entry(window, textvariable=var_input_path, width=60, font=('微软雅黑', 10)).place(x=120, y=22)
var_save_path = tk.StringVar()
entry_save_path = tk.Entry(window, textvariable=var_save_path, width=60, font=('微软雅黑', 10)).place(x=120, y=122)

# Frame: listbox + scroll
frame_f = tk.Frame(window, width=70, height=8)
frame_f.place(x=120, y=180)
frame_d = tk.Frame(window, width=70, height=6)
frame_d.place(x=120, y=380)
listbox_file_list = tk.Listbox(frame_f, font=('微软雅黑', 10), width=65, height=8, selectmode='extended') # 可多选
listbox_file_list.pack(side='left')
scr_f = tk.Scrollbar(frame_f)
scr_f.pack(side='right', expand=1, fill='y')
listbox_detail = tk.Listbox(frame_d, font=('微软雅黑', 10), width=65, height=6, takefocus=False)
listbox_detail.pack(side='left')
scr_d = tk.Scrollbar(frame_d)
scr_d.pack(side='right', expand=1, fill='y')

# 关联listbox 和 scroll
listbox_file_list.config(yscrollcommand=scr_f.set)
scr_f.config(command=listbox_file_list.yview)
listbox_detail.config(yscrollcommand=scr_d.set)
scr_d.config(command=listbox_detail.yview)

# listbox init
try:
    with open('files_info.pickle', 'rb') as path_list:
        files_info = pickle.load(path_list)
    for file in files_info:
        listbox_file_list.insert('end', file)
except FileNotFoundError:
    with open('files_info.pickle', 'wb') as path_list:
        files_info = []
        pickle.dump(files_info, path_list)


def insert_to_list():
    new_path = var_input_path.get()
    if new_path.isspace() or new_path == '':
        tk.messagebox.showinfo('提示', '输入路径为空！请输入路径')
        listbox_detail.insert('end', get_time() + '新文件路径加入失败！')
    elif new_path in files_info:
        tk.messagebox.showinfo('提示', '该文件路径已经加入')
        listbox_detail.insert('end', get_time() + '新文件路径加入失败！')
    elif not os.path.exists(new_path):
        tk.messagebox.showerror('错误', '该文件路径不存在，请输入正确路径')
        listbox_detail.insert('end', get_time() + '新文件路径加入失败！')
    else:
        listbox_file_list.insert('end', new_path)
        files_info.append(new_path)
        with open('files_info.pickle', 'wb') as path_list:
            pickle.dump(files_info, path_list)
        listbox_detail.insert('end', get_time() + '新文件路径加入成功！')
    var_input_path.set('')


def delete_file_from_list():
    if listbox_file_list.curselection():
        for each in listbox_file_list.curselection()[::-1]:
            listbox_file_list.delete(each)
            del files_info[int(each)]
        with open('files_info.pickle', 'wb') as path_list:
            pickle.dump(files_info, path_list)
        listbox_detail.insert('end', get_time() + '文件路径已删除.')
        if len(files_info) == 0:
            tk.messagebox.showinfo('提示', '目录存储文件已空')
            listbox_detail.insert('end', get_time() + '文件路径删除失败.')
    else:
        tk.messagebox.showinfo('提示', '请指定删除文件夹或文件')
        listbox_detail.insert('end', get_time() + '文件路径删除失败.')


def start_counts():
    save_path = var_save_path.get()
    if save_path.isspace() or save_path == '':
        tk.messagebox.showerror('错误', '保存文件路径为空，请输入完整文件夹或文件')
        listbox_detail.insert('end', get_time() + '程序运行失败')
    elif len(files_info) == 0:
        tk.messagebox.showerror('错误', '没有文件需要处理，请输入文件夹或文件')
        listbox_detail.insert('end', get_time() + '程序运行失败')
    else:
        listbox_detail.insert('end', get_time() + '程序开始运行')
        listbox_detail.insert('end', get_time() + '正忙...请勿操作')
        all_input_path = []
        for file in files_info:
            all_input_path.extend(Sub_Counts.find_srt_file(file))
        sub = Sub_Counts(all_input_path, save_path)
        btn_start.config(state='disabled')
        sub.mainloop()
        listbox_detail.insert('end', get_time() + '处理结束，输出文件和日志文件已保存!')
        btn_start.config(state='normal')

        # Treeview
        window_treeview = tk.Toplevel(window)
        window_treeview.title("运行结果显示")
        # set_win_center(window_treeview, 800, 300)
        # window_treeview.resizable(0, 0)
        # window_treeview.geometry('600x300')
        columns = ("序号", "文件路径", "字幕类型", "英文词频")
        treeview = ttk.Treeview(window_treeview, height=18, show='headings', columns=columns)
        treeview.column("序号", width=70, anchor='center')
        treeview.column("文件路径", width=600, anchor='w')
        treeview.column("字幕类型", width=100, anchor='center')
        treeview.column("英文词频", width=100, anchor='center')

        treeview.heading("序号", text="序号")
        treeview.heading("文件路径", text="文件路径")
        treeview.heading("字幕类型", text="字幕类型")
        treeview.heading("英文词频", text="英文词频")

        # scroll
        scr_tree_y = tk.Scrollbar(window_treeview, command=treeview.yview)
        treeview.config(yscrollcommand=scr_tree_y.set)
        scr_tree_y.pack(side='right', fill='y')

        treeview.pack(side='left', expand=1, fill='both')

        # display
        for i in range(len(sub.files_path)):
            treeview.insert('', i, value=(i, sub.files_path[i], sub.str_types[i], float(sub.word_freq[i])))

        # 自动排序
        def treeview_sort_column(tv, col, reverse):
            l = [(tv.set(k, col), k) for k in tv.get_children('')]
            l.sort(reverse=reverse)
            for index, (val, k) in enumerate(l):
                tv.move(k, '', index)
            tv.heading(col, command=lambda: treeview_sort_column(tv, col, not reverse))

        for col in columns:
            treeview.heading(col, text=col, command=lambda _col=col: treeview_sort_column(treeview, _col, False))


def thread_it(func, *args):
    """ 将函数打包进线程 """
    t = threading.Thread(target=func, args=args)
    t.setDaemon(True)
    t.start()


def confirm_to_quit():
    if tk.messagebox.askyesnocancel('提示', '确定要退出？'):
        window.quit()


def open_input_file():
    var_input_path.set('')
    is_dir = tk.messagebox.askyesno(title='请选择打开文件类型', message='文件夹(Yes)/文件(No)')
    if is_dir:
        new_file = filedialog.askdirectory()
    else:
        new_file = filedialog.askopenfilename()
    var_input_path.set(new_file)


def open_save_dir():
    var_save_path.set('')
    var_save_path.set(filedialog.askdirectory())


# button
btn_open_input = tk.Button(window, text='浏  览', width=8, font=('微软雅黑', 10), command=open_input_file)
btn_open_input.place(x=618, y=16)
btn_open_save = tk.Button(window, text='浏  览', width=8, font=('微软雅黑', 10), command=open_save_dir)
btn_open_save.place(x=618, y=116)
btn_insert_file = tk.Button(window, text='添加文件路径', font=('微软雅黑', 12), command=insert_to_list)
btn_insert_file.place(x=150, y=60)
btn_delete_file = tk.Button(window, text='删除文件路径', font=('微软雅黑', 12), command=delete_file_from_list)
btn_delete_file.place(x=400, y=60)
btn_start = tk.Button(window, text='开始运行', font=('微软雅黑', 12), command=lambda: thread_it(start_counts))
btn_start.place(x=200, y=520)
btn_quit = tk.Button(window, text='退    出', font=('微软雅黑', 12), command=confirm_to_quit)
btn_quit.place(x=450, y=520)


if __name__ == '__main__':
    window.mainloop()
