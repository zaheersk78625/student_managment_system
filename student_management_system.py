import sqlite3
from tkinter import *
from tkinter import messagebox

# ---------------- DATABASE ----------------

conn = sqlite3.connect("students.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS student(
id INTEGER PRIMARY KEY AUTOINCREMENT,
name TEXT,
roll TEXT,
course TEXT,
marks INTEGER
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS users(
id INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT,
password TEXT
)
""")
conn.commit()

cur.execute("SELECT * FROM users")
if cur.fetchone() is None:
    cur.execute("INSERT INTO users VALUES(NULL,'admin','admin123')")
    conn.commit()

# ---------------- COLORS ----------------

BG = "#1e1e2e"
FG = "#ffffff"
BTN = "#4CAF50"
BTN2 = "#2196F3"
DEL = "#f44336"

# ---------------- LOGIN ----------------

def login():
    cur.execute("SELECT * FROM users WHERE username=? AND password=?",
                (user_var.get(), pass_var.get()))
    if cur.fetchone():
        messagebox.showinfo("Success","Login Successful")
        login_win.destroy()
        open_sms()
    else:
        messagebox.showerror("Error","Invalid Login")

# ---------------- SMS ----------------

def open_sms():
    root = Tk()
    root.title("Student Management System")
    root.geometry("700x500")
    root.configure(bg=BG)

    def add_student():
        cur.execute("INSERT INTO student VALUES(NULL,?,?,?,?)",
                    (name_var.get(), roll_var.get(), course_var.get(), marks_var.get()))
        conn.commit()
        show_students()

    def show_students():
        listbox.delete(0,END)
        cur.execute("SELECT * FROM student")
        for row in cur.fetchall():
            listbox.insert(END,row)

    def delete_student():
        row = listbox.get(ACTIVE)
        if row:
            cur.execute("DELETE FROM student WHERE id=?", (row[0],))
            conn.commit()
            show_students()

    def update_student():
        row = listbox.get(ACTIVE)
        if row:
            cur.execute("UPDATE student SET name=?,roll=?,course=?,marks=? WHERE id=?",
                        (name_var.get(), roll_var.get(), course_var.get(), marks_var.get(), row[0]))
            conn.commit()
            show_students()

    name_var = StringVar()
    roll_var = StringVar()
    course_var = StringVar()
    marks_var = StringVar()

    Label(root,text="Student Management System",
          font=("Segoe UI",20,"bold"),bg=BG,fg=FG).pack(pady=10)

    form = Frame(root,bg=BG)
    form.pack()

    def field(label,var):
        Label(form,text=label,font=("Segoe UI",11),bg=BG,fg=FG).grid(sticky=W,pady=5)
        Entry(form,textvariable=var,font=("Segoe UI",11),width=30).grid(row=form.grid_size()[1]-1,column=1)

    field("Name",name_var)
    field("Roll No",roll_var)
    field("Course",course_var)
    field("Marks",marks_var)

    btns = Frame(root,bg=BG)
    btns.pack(pady=15)

    Button(btns,text="Add",bg=BTN,fg="white",width=12,command=add_student).grid(row=0,column=0,padx=5)
    Button(btns,text="Update",bg=BTN2,fg="white",width=12,command=update_student).grid(row=0,column=1,padx=5)
    Button(btns,text="Delete",bg=DEL,fg="white",width=12,command=delete_student).grid(row=0,column=2,padx=5)

    listbox = Listbox(root,width=85,height=10,font=("Consolas",10))
    listbox.pack()

    show_students()
    root.mainloop()

# ---------------- LOGIN UI ----------------

login_win = Tk()
login_win.title("Login")
login_win.geometry("350x300")
login_win.configure(bg=BG)

user_var = StringVar()
pass_var = StringVar()

Label(login_win,text="LOGIN",
      font=("Segoe UI",20,"bold"),bg=BG,fg=FG).pack(pady=20)

Entry(login_win,textvariable=user_var,font=("Segoe UI",12),width=25).pack(pady=5)
Entry(login_win,textvariable=pass_var,font=("Segoe UI",12),show="*",width=25).pack(pady=5)

Button(login_win,text="Login",bg=BTN,fg="white",width=20,command=login).pack(pady=20)

login_win.mainloop()
