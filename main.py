import tkinter as tk
from tkinter.filedialog import askopenfile
import tree
from dataset import Dataset
from PIL import Image, ImageTk

root = tk.Tk()
root.title('Regression Tree')

file_name = None
dataset = None

canvas = tk.Canvas(root, width=800, height=100)
canvas.grid(columnspan=12, rowspan=3)

tree_img = Image.open('tree_img.png')
tree_img = tree_img.resize((80, 80))
tree_img = ImageTk.PhotoImage(tree_img)
tree_img_label = tk.Label(image=tree_img)
tree_img_label.grid(columnspan=12, column=0, row=0)

process_canvas = tk.Canvas(root, width=800, height=100)

label = tk.Label(root, text='Select CSV file', font='Arial')
label.grid(columnspan=12, column=0, row=1)

browse_text = tk.StringVar()
browse_btn = tk.Button(root, textvariable=browse_text, command=lambda: open_file())
browse_text.set('Files')
browse_btn.grid(columnspan=12, column=0, row=2)

show_tree_btn = tk.Button(root, command=lambda: call_tree(file_name), text='Show Tree')

file_name_val = tk.StringVar('')
file_name_tag = tk.Label(root, textvariable=file_name_val)
file_name_tag.grid(columnspan=12, column=0, row=3)

header_val = tk.StringVar('')
header_tag = tk.Label(root, textvariable=header_val)
header_tag.config(wraplength=790)

a = tk.Label(root, text="Ignore Columns")
b = tk.Label(root, text="Numeric Columns")
a1 = tk.Entry(root)
b1 = tk.Entry(root)
b2 = tk.Button(root, command=lambda: all_columns(Dataset.get_headers(dataset.data)), text='All')


tree_txbox = tk.Text(root, height=50, width=100, xscrollcommand=True, )


def open_file():
    global file_name
    browse_text.set('Loading...')
    file = askopenfile(parent=root, mode='rb', title="Choose a CSV")
    if file:
        if '.csv' not in file.name:
            file_name_val.set('not valid')
            browse_text.set('Files')
            tree_txbox.grid_forget()
            file_name = None
        else:
            print(file.name)
            file_name = file.name
            process_canvas.grid(columnspan=12, rowspan=3)
            file_name_val.set(file_name)
            browse_text.set('Change File')
            show_form()
            prep_data(file_name)
            set_headers(Dataset.get_headers(dataset.data))
            header_tag.grid(columnspan=12, row=5, column=0)
            show_tree_btn.grid(columnspan=12, row=8, column=0)
            tree_txbox.grid_forget()
            # call_tree(file_name)


def call_tree(file):
    tree_txbox.grid_forget()
    ignore_cols = a1.get().split(',') if a1.get() != '' else []
    numeric_cols = b1.get().split(',') if b1.get() != '' else []
    for i in range(len(ignore_cols)):
        ignore_cols[i] = int(ignore_cols[i])
    for i in range(len(numeric_cols)):
        numeric_cols[i] = int(numeric_cols[i])
    print(ignore_cols, numeric_cols)
    tree_txbox.config(state='normal')
    tree_txbox.delete("1.0", "end")
    dataset.prepare_data(numeric_cols, ignore_cols)
    dataset.call_tree()
    tree_var = dataset.tree
    tree_txbox.insert(1.0, tree_var)
    tree_txbox.config(state='disabled')
    tree_txbox.grid(columnspan=12, rowspan=2, row=9)


def all_columns(headers):
    global b1
    string = ''
    for i in range(len(headers)):
        string += str(i) + ','
    b1.delete(0, 'end')
    b1.insert(0, string)


def set_headers(headers):
    string = 'HEADERS: | '
    for i in range(len(headers)):
        string += str(i) + ' - ' + str(headers[i]) + ' | '
    header_val.set(string)


def show_form():
    a.grid(row=6, column=2, columnspan=2)
    b.grid(row=7, column=2, columnspan=2)
    a1.grid(row=6, column=4, columnspan=4)
    b1.grid(row=7, column=4, columnspan=4)
    b2.grid(row=7, column=8, columnspan=1)


def prep_data(file):
    global dataset
    dataset = Dataset(file)


root.mainloop()


