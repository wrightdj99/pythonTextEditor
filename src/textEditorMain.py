from tkinter import *
from tkinter import filedialog
from tkinter import font
from tkinter import messagebox
from tkinter import colorchooser
from datetime import datetime

#Do we have an open file?
global open_status_name
open_status_name = False

#Is any text currently being selected?
global selected
selected = False

#Save as confirmation
def save_confirm(file_name):
    if(open_status_name):
        status_bar.config(text=f'{open_status_name}')
    else:
        status_bar.config(text=f'{file_name}')

#Creating New File Function
def new_file():
    my_text.delete("1.0", END)
    root.title("New File - Pytext")
    status_bar.config(text="New File        ")
    global open_status_name
    open_status_name = False
    
def open_file():
    #Delete old text in text box
    my_text.delete("1.0", END)
    #Get filename
    text_file = filedialog.askopenfilename(initialdir="/Users/danwright99/Desktop", title="Open File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    if text_file:
        global open_status_name
        open_status_name = text_file
    name = text_file
    status_bar.config(text=f'{name}        ')
    name = name.replace("/Users/danwright99/", "")
    root.title(f'{name} - Pytext')
    
    #Open File
    text_file = open(text_file, 'r')
    content_text_file = text_file.read()
    my_text.insert(END, content_text_file)
    #Close opened file
    text_file.close()

#Pulls up the actual save as file screen
def save_as():
    global open_status_name
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="/Users/danwright99/Desktop", title="Save File", filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"), ("Python Files", "*.py"), ("All Files", "*.*")))
    if(text_file):
        #Some simple user interface configuration to show what the end-user is working on.
        name = text_file
        status_bar.config(text=f'Saved: {name}        ')
        status_bar.after(3000, save_confirm(name))
        open_status_name = name
        name = name.replace("/Users/danwright99/", "")
        root.title(f'{name} - Pytext')
        text_file = open(text_file, 'w')
        text_file.write(my_text.get("1.0", END))
        text_file.close()
        
#Save file normally        
def save_file():
    #Is there a file open already?
    global open_status_name
    if open_status_name:
        text_file = open(open_status_name, 'w')
        text_file.write(my_text.get("1.0", END))
        text_file.close()
        status_bar.config(text=f'Saved: {open_status_name}')
        status_bar.after(3000, save_confirm(open_status_name))
    #No? Then save as...
    else:
        save_as()
        
#Cut selected text
def cut_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if my_text.selection_get():
            #Grab selected text from text box
            selected = my_text.selection_get()
            #Delete selected text from text box
            my_text.delete("sel.first", "sel.last")
            root.clipboard_clear()
            root.clipboard_append(selected)
    pass
#Copy selected text
def copy_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    if my_text.selection_get():
        selected = my_text.selection_get()
        root.clipboard_clear()
        root.clipboard_append(selected)
        
#Paste selected text
def paste_text(e):
    global selected
    if e:
        selected = root.clipboard_get()
    else:
        if selected:
            position = my_text.index(INSERT)
            my_text.insert(position, selected)
            
#Python's built-in undo and redo functions were oddly being squirrely until I did this... weird...
#Also, this handles both keystrokes and menu interactions
def undo_text(e):
    my_text.edit_undo()

def redo_text(e):
    my_text.edit_redo()
    
#Bolding text
def bold_text():
    bold_font = font.Font(my_text, my_text.cget("font"))
    bold_font.configure(weight="bold")
    #Configure Bold Tag
    my_text.tag_configure("bold", font=bold_font)
    #Has this been set? The tag is kinda like a boolean to see if something has been bolded or not
    current_tags = my_text.tag_names("sel.first")
    if "bold" in current_tags:
        my_text.tag_remove("bold", "sel.first", "sel.last")
    else:
        my_text.tag_add("bold", "sel.first", "sel.last")
        
#Italicizing text
def ital_text():
    ital_font = font.Font(my_text, my_text.cget("font"))
    ital_font.configure(slant="italic")
    #Configure Bold Tag
    my_text.tag_configure("italic", font=ital_font)
    #Has this been set? The tag is kinda like a boolean to see if something has been bolded or not
    current_tags = my_text.tag_names("sel.first")
    if "italic" in current_tags:
        my_text.tag_remove("italic", "sel.first", "sel.last")
    else:
        my_text.tag_add("italic", "sel.first", "sel.last")

#Alter text color
def change_color():
    my_color = colorchooser.askcolor()[1]
    if my_color:
        status_bar.config(text=my_color)
        color_font = font.Font(my_text, my_text.cget("font"))
        color_font.configure(slant="italic")
        #Configure Bold Tag
        my_text.tag_configure("colored", font=color_font, foreground=my_color)
        #Has this been set? The tag is kinda like a boolean to see if something has been bolded or not
        current_tags = my_text.tag_names("sel.first")
        if "colored" in current_tags:
            my_text.tag_remove("colored", "sel.first", "sel.last")
        else:
            my_text.tag_add("colored", "sel.first", "sel.last")

#All the base creation of the text editor here
root = Tk()
root.title('Pytext')
root.resizable(height=None, width=None)
#Creating main graphical frame
my_frame = Frame(root)
my_frame.pack(expand=True, fill=BOTH, pady=5, padx=5)
#Create "hamburger" scrollbar
text_scroll = Scrollbar(my_frame)
text_scroll.pack(side=RIGHT, fill=Y)
#Create "hotdog" scrollbar
hor_scroll = Scrollbar(my_frame, orient='horizontal')
hor_scroll.pack(side=BOTTOM, fill=X)
my_text = Text(my_frame, font=("Helvetica", 16), selectbackground="yellow", selectforeground="black", undo=True)
#One of the weird quirks of Tkinter, this will make the scrollbar be responsive.
my_text.config(yscrollcommand=text_scroll.set, wrap="none", xscrollcommand=hor_scroll.set)
my_text.pack(expand=True, fill=BOTH, pady=5)
#Scrollbar time
text_scroll.config(command=my_text.yview)
hor_scroll.config(command=my_text.xview)
#Toolbar
toolbar_frame = Frame(root)
toolbar_frame.pack(fill=X, side=TOP)
#Create Menus
my_menu = Menu(root)
root.config(menu=my_menu)
#Create the file save, new, save as menu
file_menu = Menu(my_menu)
my_menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Save As", command=save_as)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)

#Create the edit cut, copy, paste menu. Note, everything lambda is made that way to accomodate keystrokes
edit_menu = Menu(my_menu)
my_menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Cut \t\t\t(CTRL-X)", command=lambda: cut_text(False))
edit_menu.add_command(label="Copy \t\t(CTRL-C)", command=lambda: copy_text(False))
edit_menu.add_command(label="Paste \t\t(CTRL-V)", command=lambda: paste_text(False))
edit_menu.add_command(label="Undo \t\t(CTRL-Z)", command=lambda: undo_text(False))
edit_menu.add_command(label="Redo \t\t(CTRL-Y)", command=lambda: redo_text(False))

#Status bar
status_bar = Label(root, text='Ready        ', anchor=E)
status_bar.pack(fill=X, side=TOP, ipady=5)

#Key bindings
root.bind('<Control-x>', cut_text)
root.bind('<Control-c>', copy_text)
root.bind('<Control-v>', paste_text)
root.bind('<Control-z>', undo_text)
root.bind('<Control-y>', redo_text)

#Buttons for toolbar
bold_button = Button(toolbar_frame, text="Bold", command=bold_text)
bold_button.grid(row=0, column=0, sticky=W)
ital_button = Button(toolbar_frame, text="Italic", command=ital_text)
ital_button.grid(row=0, column=1)
undo_button = Button(toolbar_frame, text="Undo", command=lambda: undo_text(False))
undo_button.grid(row=0, column=2)
redo_button = Button(toolbar_frame, text="Redo", command=lambda: redo_text(False))
redo_button.grid(row=0, column=3)

#Text Color
color_text_button = Button(toolbar_frame, text="Text Color", command=change_color)
color_text_button.grid(row=0, column=4)

root.mainloop()