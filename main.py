import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

window = tk.Tk()

window.title("MY NOTEPAD")
window.geometry("700x500")
window.configure(bg="#c9dff0")

title = tk.Label(
    window,
    text="MY NOTEPAD 📝",
    font=("Arial", 18, "bold"),
    bg="#f7cbcb"
)

title.pack(pady=10)

font_size = 13
modified = False
dark_mode = False

tabs = {}


def get_current_frame():
    current_tab = notebook.select()

    if current_tab:
        return notebook.nametowidget(current_tab)

    return None


text = tk.Text(
    window,
    font=("Arial", 13),
    bg="white",
    fg="black",
    padx=10,
    pady=10,
    undo=True
)

notebook = ttk.Notebook(window)

notebook.pack(
    expand=True,
    fill="both",
    padx=15,
    pady=15
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


def update_tab_counter(frame):
    current_text = tabs[frame]["text"]
    current_counter = tabs[frame]["counter"]

    content = current_text.get(
        "1.0",
        "end-1c"
    )

    number_characters = len(content)
    words = content.split()
    number_words = len(words)

    current_counter.config(
        text=f"Characters: {number_characters} | "
             f"words: {number_words}"
    )


def update_tab_title(frame):
    name = tabs[frame]["name"]

    if tabs[frame]["modified"]:
        notebook.tab(
            frame,
            text=f"{name} *"
        )
    else:
        notebook.tab(
            frame,
            text=name
        )


def mark_tab_modified(frame, event=None):
    tabs[frame]["modified"] = True
    update_tab_counter(frame)
    update_tab_title(frame)


def new_tab(name="Untitled"):
    frame = tk.Frame(notebook)

    new_text = tk.Text(
        frame,
        font=("Arial", font_size),
        bg="white",
        fg="black",
        padx=10,
        pady=10,
        undo=True
    )

    new_counter = tk.Label(
        frame,
        text="Characters: 0 | words: 0",
        font=("Arial", 10),
        bg="#c9e2f3"
    )

    new_counter.pack(
        side="bottom",
        pady=5
    )

    new_text.pack(
        expand=True,
        fill="both"
    )

    notebook.add(
        frame,
        text=name
    )

    tabs[frame] = {
        "text": new_text,
        "counter": new_counter,
        "file": None,
        "modified": False,
        "name": name
    }

    new_text.bind(
        "<KeyRelease>",
        lambda event: mark_tab_modified(frame)
    )

    notebook.select(frame)


def new():
    name = simpledialog.askstring(
        "New Tab",
        "Enter the name of the tab:"
    )

    if name:
        new_tab(name)


def rename_tab():
    current_frame = get_current_frame()

    if current_frame:
        new_name = simpledialog.askstring(
            "Rename Tab",
            "Enter the new name:"
        )

        if new_name:
            tabs[current_frame]["name"] = new_name
            update_tab_title(current_frame)


def close_tab():
    current_frame = get_current_frame()

    if current_frame:

        if tabs[current_frame]["modified"]:

            save_answer = messagebox.askyesnocancel(
                "Unsaved Changes",
                "This tab has unsaved changes. Do you want to save?"
            )

            if save_answer is None:
                return

            if save_answer:
                if not save():
                    return

        current_tab = notebook.select()

        del tabs[current_frame]

        notebook.forget(current_tab)


def open2():
    file = filedialog.askopenfilename(
        filetypes=[("text files", "*.txt")]
    )

    if file:

        try:
            with open(
                file,
                "r",
                encoding="utf-8"
            ) as file_open:

                content = file_open.read()

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not open the file:\n{error}"
            )
            return

        file_name = file.split("/")[-1]

        new_tab(file_name)

        current_frame = get_current_frame()
        current_text = tabs[current_frame]["text"]

        current_text.insert(
            "1.0",
            content
        )

        tabs[current_frame]["file"] = file
        tabs[current_frame]["modified"] = False

        update_tab_counter(current_frame)
        update_tab_title(current_frame)


def save():
    current_frame = get_current_frame()

    if not current_frame:
        return False

    current_text = tabs[current_frame]["text"]
    current_file = tabs[current_frame]["file"]

    if current_file is None:

        current_file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("text files", "*.txt")]
        )

        if not current_file:
            return False

        tabs[current_frame]["file"] = current_file

    content = current_text.get(
        "1.0",
        tk.END
    )

    try:
        with open(
            current_file,
            "w",
            encoding="utf-8"
        ) as file_save:

            file_save.write(content)

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"Could not save the file:\n{error}"
        )

        return False

    tabs[current_frame]["modified"] = False

    update_tab_title(current_frame)

    return True


def save_as():
    current_frame = get_current_frame()

    if current_frame:

        current_file = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("text files", "*.txt")]
        )

        if not current_file:
            return

        content = tabs[current_frame]["text"].get(
            "1.0",
            tk.END
        )

        try:
            with open(
                current_file,
                "w",
                encoding="utf-8"
            ) as file_save:

                file_save.write(content)

        except Exception as error:
            messagebox.showerror(
                "Error",
                f"Could not save the file:\n{error}"
            )

            return

        tabs[current_frame]["file"] = current_file

        file_name = current_file.split("/")[-1]

        tabs[current_frame]["name"] = file_name

        tabs[current_frame]["modified"] = False

        update_tab_counter(current_frame)
        update_tab_title(current_frame)


def close_program():
    answer = messagebox.askyesno(
        "Close MY NOTEPAD",
        "Do you want to close the program?"
    )

    if not answer:
        return

    for frame in list(tabs.keys()):

        if tabs[frame]["modified"]:

            notebook.select(frame)

            save_answer = messagebox.askyesnocancel(
                "Unsaved Changes",
                "You have unsaved changes. Do you want to save?"
            )

            if save_answer is None:
                return

            if save_answer:

                if not save():
                    return

    window.destroy()


def update_counter(event=None):
    content = text.get(
        "1.0",
        "end-1c"
    )

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

    current_frame = get_current_frame()

    if current_frame:

        current_text = tabs[current_frame]["text"]

        current_text.config(
            font=("Arial", font_size)
        )


def decrease_font():
    global font_size

    font_size -= 2

    if font_size < 8:
        font_size = 8

    current_frame = get_current_frame()

    if current_frame:

        current_text = tabs[current_frame]["text"]

        current_text.config(
            font=("Arial", font_size)
        )


def toggle_dark_mode():
    global dark_mode

    if dark_mode == False:

        dark_mode = True

        window.configure(
            bg="#202020"
        )

        title.configure(
            bg="#333333",
            fg="white"
        )

        for frame in tabs:

            current_text = tabs[frame]["text"]

            current_counter = tabs[frame]["counter"]

            current_text.configure(
                bg="#2b2b2b",
                fg="white",
                insertbackground="white"
            )

            current_counter.configure(
                bg="#202020",
                fg="white"
            )

    else:

        dark_mode = False

        window.configure(
            bg="#c9dff0"
        )

        title.configure(
            bg="#f7cbcb",
            fg="black"
        )

        for frame in tabs:

            current_text = tabs[frame]["text"]

            current_counter = tabs[frame]["counter"]

            current_text.configure(
                bg="white",
                fg="black",
                insertbackground="black"
            )

            current_counter.configure(
                bg="#c9e2f3",
                fg="black"
            )


def bold():
    current_frame = get_current_frame()

    if current_frame:

        current_text = tabs[current_frame]["text"]

        current_text.tag_configure(
            "bold",
            font=("Arial", font_size, "bold")
        )

        try:
            current_text.tag_add(
                "bold",
                "sel.first",
                "sel.last"
            )

            mark_tab_modified(current_frame)

        except tk.TclError:
            pass


def italic():
    current_frame = get_current_frame()

    if current_frame:

        current_text = tabs[current_frame]["text"]

        current_text.tag_configure(
            "italic",
            font=("Arial", font_size, "italic")
        )

        try:
            current_text.tag_add(
                "italic",
                "sel.first",
                "sel.last"
            )

            mark_tab_modified(current_frame)

        except tk.TclError:
            pass


def underline():
    current_frame = get_current_frame()

    if current_frame:

        current_text = tabs[current_frame]["text"]

        current_text.tag_configure(
            "underline",
            font=("Arial", font_size, "underline")
        )

        try:
            current_text.tag_add(
                "underline",
                "sel.first",
                "sel.last"
            )

            mark_tab_modified(current_frame)

        except tk.TclError:
            pass


def copy_text():
    current_frame = get_current_frame()

    if current_frame:

        current_text = tabs[current_frame]["text"]

        current_text.event_generate("<<Copy>>")


def cut_text():
    current_frame = get_current_frame()

    if current_frame:

        current_text = tabs[current_frame]["text"]

        current_text.event_generate("<<Cut>>")

        mark_tab_modified(current_frame)


def paste_text():
    current_frame = get_current_frame()

    if current_frame:

        current_text = tabs[current_frame]["text"]

        current_text.event_generate("<<Paste>>")

        mark_tab_modified(current_frame)


def search_text():
    current_frame = get_current_frame()

    if current_frame:

        current_text = tabs[current_frame]["text"]

        word = simpledialog.askstring(
            "Search",
            "Enter the word you want to search for:"
        )

        if word:

            current_text.tag_remove(
                "search",
                "1.0",
                tk.END
            )

            start = "1.0"

            while True:

                position = current_text.search(
                    word,
                    start,
                    tk.END
                )

                if not position:
                    break

                end_position = current_text.index(
                    f"{position} + {len(word)} chars"
                )

                current_text.tag_add(
                    "search",
                    position,
                    end_position
                )

                start = end_position

                current_text.tag_configure(
                    "search",
                    background="yellow"
                )


def undo_text():
    current_frame = get_current_frame()

    if current_frame:

        current_text = tabs[current_frame]["text"]

        try:
            current_text.edit_undo()

            update_tab_counter(current_frame)

            mark_tab_modified(current_frame)

        except tk.TclError:
            pass


def redo_text():
    current_frame = get_current_frame()

    if current_frame:

        current_text = tabs[current_frame]["text"]

        try:
            current_text.edit_redo()

            update_tab_counter(current_frame)

            mark_tab_modified(current_frame)

        except tk.TclError:
            pass


def replace_all():
    current_frame = get_current_frame()

    if current_frame:

        current_text = tabs[current_frame]["text"]

        find_word = simpledialog.askstring(
            "Replace All",
            "Enter the word you want to find:"
        )

        if not find_word:
            return

        replace_word = simpledialog.askstring(
            "Replace All",
            "Enter the word you want to replace it with:"
        )

        if replace_word is None:
            return

        content = current_text.get(
            "1.0",
            tk.END
        )

        new_content = content.replace(
            find_word,
            replace_word
        )

        current_text.delete(
            "1.0",
            tk.END
        )

        current_text.insert(
            "1.0",
            new_content
        )

        update_tab_counter(current_frame)

        mark_tab_modified(current_frame)


menu = tk.Menu(window)

menu_file = tk.Menu(
    menu,
    tearoff=0
)

menu_file.add_command(
    label="New",
    command=new
)

menu_file.add_command(
    label="Open",
    command=open2
)

menu_file.add_command(
    label="Save",
    command=save
)

menu_file.add_command(
    label="Save As",
    command=save_as
)

menu_file.add_separator()

menu_file.add_command(
    label="Exit",
    command=close_program
)


menu_edit = tk.Menu(
    menu,
    tearoff=0
)

menu_edit.add_command(
    label="Copy",
    command=copy_text
)

menu_edit.add_command(
    label="Paste",
    command=paste_text
)

menu_edit.add_command(
    label="Undo",
    command=undo_text
)

menu_edit.add_command(
    label="Redo",
    command=redo_text
)

menu_edit.add_separator()

menu_edit.add_command(
    label="Cut",
    command=cut_text
)

menu_edit.add_separator()

menu_edit.add_command(
    label="Search",
    command=search_text
)

menu_edit.add_command(
    label="Replace All",
    command=replace_all
)

menu_edit.add_separator()

menu_edit.add_command(
    label="Rename Tab",
    command=rename_tab
)

menu_edit.add_command(
    label="Close Tab",
    command=close_tab
)


menu_view = tk.Menu(
    menu,
    tearoff=0
)

menu_view.add_command(
    label="Dark Mode",
    command=toggle_dark_mode
)


menu_format = tk.Menu(
    menu,
    tearoff=0
)

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


menu.add_cascade(
    label="File",
    menu=menu_file
)

menu.add_cascade(
    label="Edit",
    menu=menu_edit
)

menu.add_cascade(
    label="View",
    menu=menu_view
)

menu.add_cascade(
    label="Format",
    menu=menu_format
)

window.config(menu=menu)


window.bind(
    "<Control-n>",
    lambda event: new()
)

window.bind(
    "<Control-o>",
    lambda event: open2()
)

window.bind(
    "<Control-s>",
    lambda event: save()
)

window.bind(
    "<Control-Shift-s>",
    lambda event: save_as()
)

window.bind(
    "<Control-c>",
    lambda event: copy_text()
)

window.bind(
    "<Control-x>",
    lambda event: cut_text()
)

window.bind(
    "<Control-v>",
    lambda event: paste_text()
)

window.bind(
    "<Control-z>",
    lambda event: undo_text()
)

window.bind(
    "<Control-y>",
    lambda event: redo_text()
)

window.bind(
    "<Control-f>",
    lambda event: search_text()
)

window.bind(
    "<Control-h>",
    lambda event: replace_all()
)


def create_first_tab():
    first_tab_name = simpledialog.askstring(
        "New Tab",
        "Enter the name of the first tab:"
    )

    if not first_tab_name:
        first_tab_name = "Untitled"

    new_tab(first_tab_name)


window.protocol(
    "WM_DELETE_WINDOW",
    close_program
)

window.after(
    100,
    create_first_tab
)

window.mainloop()