import tkinter as tk

from tkinter import filedialog

window = tk.Tk()

window.title("MY NOTEPAD")

window.geometry("700x500")

window.configure(bg="#c9dff0")

title = tk.Label(
    window,
    text="MY NOTEPAD 📝",
    font=("Arial", 18 , "bold"),
    bg="#f7cbcb"
)

title.pack(pady=10)

font_size = 13

text = tk.Text(
    window,
    font=("Arial", 13),
    bg="white",
    fg="black",
    padx=10,
    pady=10
)

counter = tk.Label(
    window,
    text="Caracteres:0 | Words: 0",
    font=("Arial", 10),
    bg="#c9e2f3"
)

counter.pack(side="bottom", pady=5)

text.pack(
    expand=True,
    fill="both",
    padx=15,
    pady=15
    )

def new():
    text.delete("1.0", tk.END)

def open2():
    file = filedialog.askopenfilename(
        filetypes=[("text files", "*.txt")]
    )

    if file:
        with open(file, "r", encoding="utf-8") as file_open:
            content = file_open.read()

        text.delete("1.0", tk.END)
        text.insert(tk.END, content)

def save():
    file = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("text files", "*.txt")]
    )

    if file:
        content = text.get("1.0", tk.END)

        with open(file, "w", encoding="utf-8") as file_save:
            file_save.write(content)

def update_counter(event=None):
    content = text.get("1.0", "end-1c")
    number_characters = len(content)
    words = content.split()
    words_characters = len(words)
    counter.config(
        text=f"Characters: {number_characters} | "
             f"words: {words_characters}"
    )

def increase_font():
    global font_size
    font_size += 2
    text.config(
        font=("Arial", font_size)
    )
def decrease_font():
    global font_size
    font_size -= 2
    if font_size < 8:
        font_size = 8
    text.config(
        font=("Arial", font_size)
    )

def bold():

    text.tag_configure(
        "bold",
        font=("Arial", font_size, "bold")
    )

    try:

        text.tag_add(
        "bold",
        "sel.first",
        "sel.last"
        )

    except tk.TclError: pass
        
def italic():
        
    text.tag_configure(
        "italic",
        font=("Arial", font_size, "italic")
    )
        
    try:
    
        text.tag_add(
             "italic",
             "sel.first",
             "sel.last"
    )

    except tk.TclError: pass

def underline():

    text.tag_configure(
        "underline",
        font=("Arial", font_size, "underline")
    )
     
    try:

        text.tag_add(
            "underline",
            "sel.first",
            "sel.last"
        )
        
    except tk.TclError: pass


menu = tk.Menu(window)

menu_file = tk.Menu(menu, tearoff=0)

menu_file.add_command(label="New", command=new)

menu_file.add_command(label="Open", command=open2)

menu_file.add_command(label="Save", command=save)

menu_file.add_separator()

menu_file.add_command(label="Exit", command=window.destroy)

menu_format= tk.Menu(menu, tearoff=0)

menu_format.add_command(
    label="Increase Font",
    command=increase_font
)

menu_format.add_command(
    label="Decrease Font",
    command=decrease_font
)

menu_format.add_command(
    label="Bold",
    command=bold
)

menu_format.add_command(
    label="Italic",
    command=italic
)

menu_format.add_command(
    label="Underline",
    command=underline
)

menu.add_cascade(label="File", menu=menu_file)

menu.add_cascade(label="Format", menu=menu_format)

window.config(menu=menu)

window.bind("<Control-n>", lambda event: new())

window.bind("<Control-o>", lambda event: open2())

window.bind("<Control-s>", lambda event: save())

text.bind("<KeyRelease>",update_counter)

window.mainloop()
