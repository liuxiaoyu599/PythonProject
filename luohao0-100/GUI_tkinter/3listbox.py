import tkinter as tk

window = tk.Tk()
window.title('myWindow')

entry_text = tk.StringVar()
e1 = tk.Entry(window, bg='blue', textvariable=entry_text, width=4)
e1.pack()

label_text = tk.StringVar()
label_text.set('***')
l1 = tk.Label(window, bg='yellow', textvariable=label_text, width=4)
l1.pack()


def insert_to_list():
    list_box.insert('end', e1.get())


def print_selection():
    label_text.set(list_box.get(list_box.curselection()))


def delete_selection():
    list_box.delete('end', list_box.get(list_box.curselection()))


b1 = tk.Button(window, text='insert to list', width=15, height=2,
               command=insert_to_list)
b1.pack()
b2 = tk.Button(window, text='print selection', width=15, height=2,
               command=print_selection)
b2.pack()
b3 = tk.Button(window, text='delete selection', width=15, height=2,
               command=delete_selection)
b3.pack()

# label_list
list_text = tk.StringVar()
list_text.set((11, 22, 33, 44))
list_box = tk.Listbox(window, listvariable=list_text)
list_box.pack()

tk.mainloop()
