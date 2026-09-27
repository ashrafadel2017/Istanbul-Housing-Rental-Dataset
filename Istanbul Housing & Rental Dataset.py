from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from housing import Database

# ===== Database Connection =====

db = Database("istanbul.db")

# ===== Main Window =====

root = Tk()
root.title('Istanbul Housing & Rental Dataset')
root.geometry('1500x1000+0+0')
root.resizable(False, False)
root.configure(bg='#2c3e50')

# ===== Variables =====

neighbourhood = StringVar()
latitude = StringVar()
longitude = StringVar()
room_type = StringVar()
price = StringVar()
minimum_nights = StringVar()
number_of_reviews = StringVar()
last_review = StringVar()
reviews_per_month = StringVar()
calculated_host_listings_count = StringVar()
availability_365 = StringVar()
number_of_reviews_ltm = StringVar()

# ===== Entries Frame =====

# كبرنا الارتفاع لـ 950 عشان يملأ طول الشاشة كلها وميبقاش فيه فراغ
entries_frame = Frame(root, bg="#2c70b4")
entries_frame.place(x=1, y=1, width=360, height=950)

title = Label(entries_frame, text='Istanbul Housing Data', font=('Calibri', 20, 'bold'), fg='white', bg='#2c3e50')
title.place(x=10, y=1)

labels = ["Neighbourhood","Latitude","Longitude","Room Type","Price","Min Nights",
          "Number of Reviews","Last Review","Reviews/Month","Host Listings","Availability","Reviews LTM"]
variables = [neighbourhood, latitude, longitude, room_type, price, minimum_nights,
             number_of_reviews, last_review, reviews_per_month,
             calculated_host_listings_count, availability_365, number_of_reviews_ltm]

# مصفوفة لحفظ خانات الإدخال عشان ميزة الـ Enter
entry_widgets = []

for i, (lbl, var) in enumerate(zip(labels, variables)):
    Label(entries_frame, text=lbl, font=('Calibri', 13, 'bold'), bg="#b4b58b", fg='black').place(x=10, y=50+i*45)

    ent = Entry(entries_frame, textvariable=var, font=('Calibri', 13))
    ent.place(x=160, y=50+i*45, width=190)
    entry_widgets.append(ent)

# دالة ذكية للانتقال للحقل التالي عند الضغط على Enter
def focus_next(event):
    current_widget = event.widget
    try:
        index = entry_widgets.index(current_widget)
        if index < len(entry_widgets) - 1:
            entry_widgets[index + 1].focus()
        else:
            add_record() # لو في آخر خانة يضيف علطول
    except ValueError:
        pass

# ربط الخانات بزر الـ Enter
for ent in entry_widgets:
    ent.bind("<Return>", focus_next)

# ===== Buttons Frame =====

btn_frame = Frame(entries_frame, bg='white', bd=1, relief=SOLID)
btn_frame.place(x=10, y=600, width=340, height=120)

def clear_fields():
    for var in variables:
        var.set("")
    entry_widgets[0].focus()

def add_record():
    db.insert(*[var.get() for var in variables])
    messagebox.showinfo("Success", "Record added successfully!")
    displayAll()
    clear_fields()

def update_record():
    selected = tv.focus()
    if not selected:
        messagebox.showerror("Error", "Select a record to update!")
        return
    data = tv.item(selected)["values"]
    db.update(data[0], *[var.get() for var in variables])
    messagebox.showinfo("Success", "Record updated successfully!")
    displayAll()
    clear_fields()

def delete_record():
    selected = tv.focus()
    if not selected:
        messagebox.showerror("Error", "Select a record to delete!")
        return
    data = tv.item(selected)["values"]
    db.remove(data[0])
    messagebox.showinfo("Deleted", "Record deleted successfully!")
    displayAll()
    clear_fields()

Button(btn_frame, text='Add', width=15, font=('Calibri', 15, 'bold'), bg="#27ae60", fg="white", command=add_record).place(x=10, y=10)
Button(btn_frame, text='Update', width=15, font=('Calibri', 15, 'bold'), bg="#2980b9", fg="white", command=update_record).place(x=175, y=10)
Button(btn_frame, text='Delete', width=15, font=('Calibri', 15, 'bold'), bg="#c0392b", fg="white", command=delete_record).place(x=10, y=60)
Button(btn_frame, text='Clear', width=15, font=('Calibri', 15, 'bold'), bg="#f39c12", fg="white", command=clear_fields).place(x=175, y=60)

# ===== Table Frame =====

# كبرنا الفريم لـ 1120 عرض و 950 طول عشان ياخد مساحة الشاشة الـ 1500 كاملة بالملّي
tree_frame = Frame(root, bg='white')
tree_frame.place(x=375, y=1, width=1150, height=1000)

# ===== Scrollbars المباشرة بدون Canvas =====

scroll_y = Scrollbar(tree_frame, orient=VERTICAL)
scroll_y.pack(side=RIGHT, fill=Y)

scroll_x = Scrollbar(tree_frame, orient=HORIZONTAL)
scroll_x.pack(side=BOTTOM, fill=X)


# ===== Treeview =====

style = ttk.Style()
style.configure("mystyle.Treeview", font=('Calibri', 15), rowheight=35)
style.configure("mystyle.Treeview.Heading", font=('Calibri', 15, 'bold'))

columns = ("ID","Neighbourhood","Latitude","Longitude","Room Type","Price",
           "Min Nights","Number of Reviews","Last Review","Reviews/Month",
           "Host Listings","Availability","Reviews LTM")

tv = ttk.Treeview(tree_frame, columns=columns, style="mystyle.Treeview",
                  xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
tv.pack(fill=BOTH, expand=True)

scroll_x.config(command=tv.xview)
scroll_y.config(command=tv.yview)

# الحتة السحرية هنا: إجبار الأعمدة على الظهور أفقياً ومنع انضغاطها
for col in columns:
    tv.heading(col, text=col)
    if col == "ID":
        tv.column(col, width=50, anchor=CENTER, stretch=False)
    elif col == "Neighbourhood":
        tv.column(col, width=90, anchor=CENTER, stretch=False)
    else:
        # باقي الـ 11 عمود هياخدوا عرض 120 بكسل غصب عن الشاشة فالمحور الأفقي هيظهر كامل
        tv.column(col, width=90, anchor=CENTER, stretch=False)

tv['show'] = 'headings'

def getData(event):
    selected = tv.focus()
    if not selected: return
    data = tv.item(selected)["values"]
    if not data: return
    for var, value in zip(variables, data[1:]):  # تخطي الـ ID
        var.set(value)

tv.bind("<ButtonRelease-1>", getData)

def displayAll():
    tv.delete(*tv.get_children())
    try:
        for row in db.fetch():
            tv.insert("", END, values=row)
    except:
        pass

# ===== Run App =====
displayAll()
entry_widgets[0].focus() # يفتح والمؤشر جاهز في أول خانة
root.mainloop()


# Project Description

"""
This project demonstrates how to build a real estate data management system using Python, Tkinter, and SQLite.
The graphical user interface provides an easy-to-use experience for adding, updating, deleting, and viewing property records.
The design includes keyboard navigation with Enter, scrollbars for full visibility, and a consistent layout.
Suitable for academic presentation, combining database concepts and GUI programming, with potential for future enhancements.
"""
