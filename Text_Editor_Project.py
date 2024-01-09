from tkinter import *
from tkinter import filedialog, simpledialog
from tkinter.scrolledtext import ScrolledText
from tkinter import messagebox
from tkinter.ttk import *
import re

root = Tk()
root.title('Text Editor')

# scrollable text
textPad = ScrolledText(root, width=100, height=50)
filename = ''
current_content = ""

# functions
def newFile():
    global filename, current_content
    if len(textPad.get('1.0', END + '-1c')) > 0:
        if current_content != textPad.get('1.0', END):
            save_changes = messagebox.askyesnocancel("Save", "Do you want to save changes?")
            if save_changes:
                saveFile()
            elif save_changes is None:
                return  # User clicked Cancel, do nothing
    textPad.delete('1.0', END)
    root.title("TEXT EDITOR")
    current_content = ""


def saveFile():
    global current_content
    f = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    if f is not None:
        data = textPad.get('1.0', END)
        try:
            f.write(data)
            current_content = data
        except:
            messagebox.showerror(title="Oops!!", message="Unable to save file!")

def saveAs():
    global current_content
    f = filedialog.asksaveasfile(mode='w', defaultextension='.txt')
    t = textPad.get(0.0, END)
    try:
        f.write(t.rstrip())
        current_content = t
    except:
        messagebox.showerror(title="Oops!!", message="Unable to save file!")

def openFile():
    global current_content
    f = filedialog.askopenfile(parent=root, mode='r')
    t = f.read()
    textPad.delete(0.0, END)
    textPad.insert(0.0, t)
    current_content = t

def about_command():
    label = messagebox.showinfo("About", "Just Another TextPad \nNo information from the Developer")

def handle_click(event):
    textPad.tag_config('Found', background='white', foreground='grey')

def find_pattern():
    textPad.tag_remove("Found", '1.0', END)
    find = simpledialog.askstring("Find....", "Enter text:")
    if find:
        idx = '1.0'
        while 1:
            idx = textPad.search(find, idx, nocase=1, stopindex=END)
            if not idx:
                break
            lastidx = '%s+%dc' % (idx, len(find))
            textPad.tag_add('Found', idx, lastidx)
            idx = lastidx
    textPad.tag_config('Found', foreground='white', background='black')
    textPad.bind("<1>", handle_click)

def copy_text():
    textPad.clipboard_clear()
    textPad.clipboard_append(textPad.selection_get())

def find_pattern():
    textPad.tag_remove("Found", '1.0', END)
    find = simpledialog.askstring("Find....", "Enter text:")
    if find:
        idx = '1.0'
        while 1:
            idx = textPad.search(find, idx, nocase=1, stopindex=END)
            if not idx:
                break
            lastidx = '%s+%dc' % (idx, len(find))
            textPad.tag_add('Found', idx, lastidx)
            idx = lastidx
    textPad.tag_config('Found', foreground='white', background='black')
    textPad.bind("<1>", handle_click)

def select_all_text():
    textPad.tag_add(SEL, '1.0', END)
    textPad.mark_set(INSERT, '1.0')
    textPad.see(INSERT)
    return 'break'

def cut_text():
    copy_text()
    textPad.delete(SEL_FIRST, SEL_LAST)

def paste_text():
    textPad.insert(INSERT, textPad.clipboard_get())

def printme():
    label = messagebox.showinfo("Text", "Welcome to the text editor")

def exit_command():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

# creating menu
menuM = Menu(root)
root.configure(menu=menuM)

fileM = Menu(menuM)
menuM.add_cascade(label='File', menu=fileM)
fileM.add_command(label='New', accelerator='Ctrl+N', command=newFile)
fileM.add_command(label='Open', accelerator='Ctrl+O', command=openFile)
fileM.add_command(label='Save', accelerator='Ctrl+S', command=saveFile)
fileM.add_command(label='Select All', accelerator='Ctrl+A', command=select_all_text)
fileM.add_command(label='Save As', accelerator='Ctrl+Shift+S', command=saveAs)
fileM.add_separator()
fileM.add_command(label='Exit',accelerator='Ctrl+Q', command=exit_command)

editM = Menu(menuM)
menuM.add_cascade(label='Edit', menu=editM)
editM.add_command(label='Cut', accelerator='Ctrl+X', command=cut_text)
editM.add_command(label='Copy', accelerator='Ctrl+C', command=copy_text)
editM.add_command(label='Paste', accelerator='Ctrl+V', command=paste_text)


viewM = Menu(menuM)
menuM.add_cascade(label='View', menu=viewM)
viewM.add_command(label='Text', command=printme)

aboutM = Menu(menuM)
menuM.add_cascade(label='About', menu=aboutM)
aboutM.add_command(label='About',accelerator='Ctrl+H', command=about_command)

findM = Menu(menuM)
menuM.add_cascade(label='Find', menu=findM)
findM.add_command(label='Find',accelerator='Ctrl+F', command=find_pattern)

textPad.pack()

# Bind keyboard shortcuts
root.bind("<Control-n>", lambda event: newFile())
root.bind("<Control-o>", lambda event: openFile())
root.bind("<Control-s>", lambda event: saveFile())
root.bind("<Control-S>", lambda event: saveAs())
root.bind("<Control-q>", lambda event: exit_command())
root.bind("<Control-f>", lambda event: find_pattern())
root.bind("<Control-a>", lambda event: select_all_text())
root.bind("<Control-h>", lambda event: about_command())


root.mainloop()
