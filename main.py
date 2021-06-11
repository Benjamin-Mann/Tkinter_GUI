from tkinter import *
from tkinter import messagebox
import random
import json


# ---------------------------- GENERATE PASSWORD BUTTON ------------------------
alphabet = ['a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f', 'F', 'g', 'G', 'h', 'H'
            'i', 'I', 'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'o', 'O', 'p', 'P'
            'q', 'Q', 'r', 'R', 's', 'S', 't', 'T', 'u', 'U', 'v', 'V', 'w', 'W', 'x', 'X'
            'y', 'Y', 'z', 'Z']
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
special = ['!', '@', '#', '$', '%', '&', '*', '?']
group = [alphabet, numbers, special]


def password_gen():
    final = ""
    for i in range(11):
        item = random.choice(group)
        position = random.randint(0, len(item) - 1)
        final += str(item[position])
    entry_pass.insert(0, final)
    entry_pass.clipboard_clear()
    entry_pass.clipboard_append(final)

# -------------------------- SEARCH BUTTON --------------------------------


def search():

    search_item = entry_web.get().title()

    with open('data.json', mode='r') as data_file:
        data = json.load(data_file)
        if search_item in data:     # message box for item in Json. Will return email and pass.
            messagebox.showinfo(entry_web.get().title(), f'Email: {data[search_item]["Email"]}\n'
                                                         f'\nPassword: {data[search_item]["Password"]}')
        else:
            if len(data) == 0:  # Return warning if no items in Json file.
                messagebox.showinfo(title='Warning!', message='No data file found.')
            else:   # Returns error if searched item not in Json file.
                messagebox.showerror(title='Error', message=f'No details for {search_item} exist.')

# ---------------------------- SAVE PASSWORD -------------------------------


def add_pushed():
    # is_ok variable defined due to scope. Message box returns boolean.
    is_ok = 0
    if len(entry_web.get()) > 0 and len(entry_user.get()) > 0 and len(entry_pass.get()) > 0:
        is_ok = messagebox.askokcancel(title=entry_web.get().title(), message=(f'This is the information '
                                                                               f'you have entered:'
                                                                               f'\nUsername: {entry_user.get()}'
                                                                               f'\nPassword: {entry_pass.get()}'))
    else:
        messagebox.showwarning(title='Warning Input Missing', message="Please don't leave any fields empty.")

    json_dump = {
        entry_web.get().title(): {
            "Email": entry_user.get(),
            "Password": entry_pass.get(),
        }   # Format for Json save data. Key is website name.
    }
    if is_ok is True:
        with open('data.json', mode='r') as data_file:
            data = json.load(data_file)
            data.update(json_dump)

        with open('data.json', mode='w') as data_file:
            json.dump(data, data_file, indent=4)
            entry_web.delete(0, END)
            entry_pass.delete(0, END)


# ---------------------------------- UI SETUP-------------------------------------

# --------- WINDOW SETUP

window = Tk()
window.title('Password Manager')
window.config(padx=65, pady=50)

# --------- BACKGROUND IMAGE

canvas = Canvas(width=300, height=200, highlightthickness=0)
photo = PhotoImage(file='logo.png')
canvas.create_image(100, 100, image=photo)
canvas.grid(row=0, column=1, sticky='e')

# ---------- WEBSITE NAME LABEL AND ENTRY

label_web = Label(text='Website:')
label_web.grid(row=1, column=0)

entry_web = Entry(width=29)
entry_web.grid(row=1, column=1, sticky='w')
entry_web.focus()

# ---------- EMAIL/USERNAME LABEL AND ENTRY

label_user = Label(text='Email/Username:')
label_user.grid(row=2, column=0)

entry_user = Entry(width=49)
entry_user.grid(row=2, column=1, columnspan=2, sticky='w')
entry_user.insert(0, 'john.smith@email.com')    # Email inserted for testing. Can be switched for normal operation.

# --------- PASSWORD LABEL, ENTRY, AND GENERATION BUTTON

label_pass = Label(text='Password')
label_pass.grid(row=3, column=0)

entry_pass = Entry(width=29)
entry_pass.grid(row=3, column=1, sticky='w')

button_pass = Button(width=15, text='Generate Password', command=password_gen)
button_pass.grid(row=3, column=1, sticky='e,s')

# --------- ADD AND SEARCH BUTTONS

button_add = Button(width=30, text='Add', command=add_pushed)
button_add.place(x=110, y=280)

button_search = Button(width=15, height=1, text='Search', command=search)
button_search.grid(row=1, column=1, sticky='e,n')


window.mainloop()
