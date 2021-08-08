from tkinter import *
from tkinter import messagebox
import backend

main = Tk()
main.title("Contacts")
main.resizable(width=False,height=False)

frame1 = Frame(main)
frame1.pack(side=TOP)
contactList = Listbox(frame1,bg="#21debb",height=15,width=30)
contactList.pack(side=LEFT)
sby = Scrollbar(frame1)
sby.pack(side=LEFT)
contactList.configure(yscrollcommand=sby.set)
sby.configure(command=contactList.yview())


def button_maker(master,text,color,command=None):
    button = Button(master,text=text,relief=RAISED,height=4,highlightbackground=color,command=command)
    button.pack(side=TOP,fill=BOTH,expand=True)
    return button


def label_maker(master,text,r,c):
    label = Label(master,text=text)
    label.grid(row=r,column=c)
    return label


def entry_maker(master,variable,r,c):
    entry = Entry(master,textvariable=variable)
    entry.grid(row=r,column=c)
    return entry


def add_window():
    addWindow = Toplevel(main)
    addWindow.title("ADD CONTACT")
    name_label = label_maker(addWindow,"Name:",0,0)
    name_var = StringVar()
    global name_entry
    name_entry = entry_maker(addWindow,name_var,0,1)
    phone_label = label_maker(addWindow,"Phone Number:",1,0)
    phone_var = StringVar()
    global phone_entry
    phone_entry = entry_maker(addWindow,phone_var,1,1)
    email_label = label_maker(addWindow,"Email:",2,0)
    email_var = StringVar()
    global email_entry
    email_entry = entry_maker(addWindow,email_var,2,1)

    def add_func():
        backend.add(name_entry.get(),phone_entry.get(),email_entry.get())
        view_all()
        addWindow.destroy()

    add_button = Button(addWindow,text="ADD",command= add_func)
    add_button.grid(row=3,column=0,columnspan=2,sticky="ew")


def search_window():
    searchWindow = Toplevel(main)
    searchWindow.title("SEARCH")
    search_name = label_maker(searchWindow,"Name:",0,0)
    search_var = StringVar()
    global search_entry
    search_entry = entry_maker(searchWindow,search_var,0,1)

    def search_func():
        contactList.delete(0,END)
        for contact in backend.search(search_entry.get()):
            contactList.insert(END,contact[1])
        searchWindow.destroy()

    search_button = Button(searchWindow,text="SEARCH", command= search_func)
    search_button.grid(row=1,column=0,columnspan=2,sticky="ew")


def view_all():
    contactList.delete(0,END)
    for contact in sorted(backend.view(),key=lambda contact: contact[1]):
        contactList.insert(END,contact[1])


def select(event):

    global selected_contact

    if len(contactList.curselection()) > 0:

        index = contactList.curselection()[0]
        selected_contact = contactList.get(index)

        contact_window = Toplevel(main)
        contact_window.title(selected_contact)
        name_label = label_maker(contact_window,"Name:",0,0)
        name_variable = StringVar()
        name_entry = entry_maker(contact_window,name_variable,0,1)
        phone_label = label_maker(contact_window, "Phone:", 1, 0)
        phone_variable = StringVar()
        phone_entry = entry_maker(contact_window, phone_variable, 1, 1)
        email_label = label_maker(contact_window, "Email:", 2, 0)
        email_variable = StringVar()
        email_entry = entry_maker(contact_window, email_variable, 2, 1)

        name_entry.insert(END,backend.search(selected_contact)[0][1])
        phone_entry.insert(END, backend.search(selected_contact)[0][2])
        email_entry.insert(END, backend.search(selected_contact)[0][3])

        def delete_func():
            backend.delete(selected_contact)
            view_all()
            contact_window.destroy()

        def edit_func():
            contact = backend.search(selected_contact)[0]
            backend.edit(contact[0],name_entry.get(),phone_entry.get(),email_entry.get())
            view_all()


        def export_func():
            backend.export(
                backend.search(selected_contact)[0][1], backend.search(selected_contact)[0][2], backend.search(selected_contact)[0][3])
            messagebox.showinfo("DONE!","Contact shared successfully:)")


        delete_button = Button(contact_window,text="DELETE",command=delete_func)
        delete_button.grid(row=3,column=0,columnspan=2,sticky="ew")
        edit_button = Button(contact_window, text="EDIT",command=edit_func)
        edit_button.grid(row=4, column=0, columnspan=2, sticky="ew")
        export_button = Button(contact_window, text="Export as .txt",command= lambda: export_func())
        export_button.grid(row=5, column=0, columnspan=2, sticky="ew")



contactList.bind("<Double-1>",select)

addButton = button_maker(main,"Add Contact","#21cede",command=lambda: add_window())

searchButton = button_maker(main,"Search Contacts","#21a2de",command=lambda: search_window())

showButton = button_maker(main,"View All","#2173de",command=lambda: view_all())

view_all()

main.mainloop()
