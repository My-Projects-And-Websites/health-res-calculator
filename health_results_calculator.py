import tkinter #the tkinter module alows the user to make a graphical user interface
import sqlite3 #this module allows the user to create a database
import tkinter.messagebox
import time
from tkinter import ttk

db = sqlite3.connect("FitnessDatabase.db") #connects this database file to the program

db.execute('PRAGMA foreign_keys = ON') #allows foreign keys to be used in the program

cursor = db.cursor() #a cursor is used to interact with the database

#execute script = there are multiple instructions being injected to the database with SQL
cursor.executescript('''CREATE TABLE IF NOT EXISTS
                         ClientDetails(ClientID INTEGER PRIMARY KEY NOT NULL,
                                      TName TEXT, CName TEXT,
                                      Age INTEGER, Gender CHARACTER(1),
                                      Weight REAL, Height REAL);

                        CREATE TABLE IF NOT EXISTS
                        BodyDetails(ClientID INTEGER PRIMARY KEY,
                                    MHR INTEGER, IdealWeight REAL, BMR REAL, BMI REAL, Category TEXT,
                                    FOREIGN KEY(ClientID) REFERENCES ClientDetails(ClientID));
                                    ''')
                        #this is where the tables are created
                        #CREATE TABLE IF NOT EXISTS = this stops the same tables from being created everytime the program is ran
                        #the table name is then written and all the field names the user wants to make is created inside the brackets of the table name
                        #the capital letters are the data types for each field

fontstyle = "Arial"
label_font_size = 25
button_font_size = 60
txt_font_size = 40
txt_width = 9 #a variable to set the width for the textboxes

root = tkinter.Tk() #the Tk method means this is the first window

root.title("Please Enter Your Name") #title of the window
root.geometry('700x390') #this is the size of the window

tkinter.Label(root, text="Login Page", font = (fontstyle, 50), padx=10, pady=10, bg="green").place(x=180, y=10) #this is a label placed on the window with the font properties applied
#the grid method allows the user to pick the positioning of the objects
#the grid method has a relative point and will always start at the top left

tkinter.Label(root, text="Trainer Name:", font = (fontstyle, 20), padx=10, pady=10, fg="green").place(x=70, y=125)
tkinter.Label(root, text="Customer Name:", font = (fontstyle, 20), padx=10, pady=10, fg="green").place(x=70, y=225)

txt_TrainerName = tkinter.Entry(root, width=txt_width, font = (fontstyle, txt_font_size)) #a textbox variable
txt_TrainerName.place(x=362, y=120) #padx and pady adjusts the padding of the object it is assigned to

txt_CustomerName = tkinter.Entry(root, width=txt_width, font = (fontstyle, txt_font_size))
txt_CustomerName.place(x=362, y=220)

def admin_login():
    global LOGINform
    global admin_username
    global admin_password
    
    LOGINform = tkinter.Toplevel(main_input)
    LOGINform.title("View Data")
    LOGINform.geometry("400x260")
    LOGINform.bind('<Return>', data_view)

    tkinter.Label(LOGINform, text="Admin Login", font=(fontstyle, 30)).place(x=100, y=10)
    tkinter.Label(LOGINform, text="Username:", font=(fontstyle, 20)).place(x=20, y=80)
    tkinter.Label(LOGINform, text="Password:", font=(fontstyle, 20)).place(x=20, y=140)
    
    admin_username = tkinter.Entry(LOGINform, width=15, font=(fontstyle, 20))
    admin_username.place(x=160, y=80)

    admin_password = tkinter.Entry(LOGINform, width=15, font=(fontstyle, 20), show="*")
    admin_password.place(x=160, y=140)

    btn_Confirm = tkinter.Button(LOGINform, text="Confirm", command=data_view, font=(fontstyle, 20))
    btn_Confirm.place(x=150, y=190)

def data_view(event=None):
    if admin_username.get() == "admin" and admin_password.get() == "admin":
        DATAform = tkinter.Toplevel(LOGINform)
        DATAform.title("Data")
        DATAform.geometry("1000x600")

        LOGINform.withdraw()

        tree_one = ttk.Treeview(DATAform, column=("column1", "column2", "column3", "column4", "column5", "column6", "column7"), show="headings")
        
        tree_one.heading("#1", text="ID")
        tree_one.heading("#2", text="Trainer Name")
        tree_one.heading("#3", text="Customer Name")
        tree_one.heading("#4", text="Customer Age")
        tree_one.heading("#5", text="Customer Gender")
        tree_one.heading("#6", text="Customer Weight")
        tree_one.heading("#7", text="Customer Height")
        tree_one.pack()

        db = sqlite3.connect("FitnessDatabase.db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM ClientDetails")
        rows = cursor.fetchall()
        for row in rows:
            tree_one.insert("", tkinter.END, values=row)
        db.commit()

        tree_two = ttk.Treeview(DATAform, column=("column1", "column2", "column3", "column4", "column5", "column6"), show="headings")
        tree_two.heading("#1", text="ID")
        tree_two.heading("#2", text="Customer MHR")
        tree_two.heading("#3", text="Customer BMR")
        tree_two.heading("#4", text="Customer IBW")
        tree_two.heading("#5", text="Customer BMI")
        tree_two.heading("#6", text="Customer Class")
        tree_two.pack()

        db_two = sqlite3.connect("FitnessDatabase.db")
        cursor_two = db.cursor()
        cursor_two.execute("SELECT * FROM BodyDetails")
        rows_two = cursor_two.fetchall()
        for row_two in rows_two:
            tree_two.insert("", tkinter.END, values=row_two)
        db_two.close()

        def iexit():
            DATAform.destroy()
            LOGINform.destroy()
            main_input.destroy()

        def db_close():
            DATAform.destroy()

        tkinter.Button(DATAform, text="Exit", command=iexit, font=(fontstyle, 40)).place(x=640, y=470)
        tkinter.Button(DATAform, text="Close Database", command=db_close, font=(fontstyle, 40)).place(x=230, y=470)
    else:
        tkinter.messagebox.showerror("Error", "Incorrect details. Please re-enter your credentials and ensure CAPS LOCK is not enabled.")

def open_main_form(event=None): #this is a function
    global main_input #these variables are globalised meaning it can be called from anywhere in the program
    global txt_Age
    global txt_Gender
    global txt_Weight
    global txt_Height

    root.withdraw() #hides the first window

    if txt_TrainerName.get() == "" and txt_CustomerName.get() == "":
        tkinter.messagebox.showerror("Error", "No Details Given")
        root.update()
        root.deiconify()
    elif txt_TrainerName.get() == "" or txt_CustomerName.get() == "":
        tkinter.messagebox.showerror("Error", "Insufficient Details Given")
        root.update()
        root.deiconify()
    elif "1" in txt_TrainerName.get() or "2" in txt_TrainerName.get() or "3" in txt_TrainerName.get() or "4" in txt_TrainerName.get() or "5" in txt_TrainerName.get() or "6" in txt_TrainerName.get() or "7" in txt_TrainerName.get() or "8" in txt_TrainerName.get() or "9" in txt_TrainerName.get() or "0" in txt_TrainerName.get():
        tkinter.messagebox.showerror("Error", "Cannot have numbers on the name. -_-")
        root.update()
        root.deiconify()
        txt_TrainerName.delete("0", tkinter.END)
    elif "1" in txt_CustomerName.get() or "2" in txt_CustomerName.get() or "3" in txt_CustomerName.get() or "4" in txt_CustomerName.get() or "5" in txt_CustomerName.get() or "6" in txt_CustomerName.get() or "7" in txt_CustomerName.get() or "8" in txt_CustomerName.get() or "9" in txt_CustomerName.get() or "0" in txt_CustomerName.get():
        tkinter.messagebox.showerror("Error", "Cannot have numbers on the name. -_-")
        root.update()
        root.deiconify()
        txt_CustomerName.delete("0", tkinter.END)
    else:
        main_input = tkinter.Toplevel() #this opens another window
        
        main_input.title("Fitness Life")
        main_input.geometry("780x570")
        main_input.bind('<Return>', results_page)

        def exit_program():
            main_input.destroy()

        tkinter.Label(main_input, text="Fitness Life", font=(fontstyle, 60), padx=10, pady=10, bg="green").place(x=200, y=10)
        tkinter.Button(main_input, text="View Data", command=admin_login, font=(fontstyle, 15), fg="green").place(x=10, y=10)
        tkinter.Button(main_input, text="Exit", command=exit_program, font=(fontstyle, 15), fg="green").place(x=710, y=10)

        tkinter.Label(main_input, text="Age", font = (fontstyle, label_font_size), padx=10, pady=10, fg="green").place(x=200, y=145)
        tkinter.Label(main_input, text="Gender (M/F)", font = (fontstyle, label_font_size), padx=10, pady=10, fg="green").place(x=135, y=225)
        tkinter.Label(main_input, text="Weight (kg)", font = (fontstyle, label_font_size), padx=10, pady=10, fg="green").place(x=150, y=305)
        tkinter.Label(main_input, text="Height (cm)", font = (fontstyle, label_font_size), padx=10, pady=10, fg="green").place(x=150, y=385)
        #these variables are not assigned to a variable because their purpose is to only display text

        txt_Age = tkinter.Entry(main_input, width=txt_width, font = (fontstyle, txt_font_size)) #this object is placed on the second window
        txt_Age.place(x=385, y=140)
        
        txt_Gender = tkinter.Entry(main_input, width=txt_width, font = (fontstyle, txt_font_size))
        txt_Gender.place(x=385, y=220)
        
        txt_Weight = tkinter.Entry(main_input, width=txt_width, font = (fontstyle, txt_font_size))
        txt_Weight.place(x=385, y=300)
        
        txt_Height = tkinter.Entry(main_input, width=txt_width, font = (fontstyle, txt_font_size))
        txt_Height.place(x=385, y=380)

        buttonDisplayOutput = tkinter.Button(main_input, text="Confirm", command=results_page, font = (fontstyle, 30), fg="green")
        buttonDisplayOutput.place(x=300, y=470)

root.bind('<Return>', open_main_form)
openMainForm = tkinter.Button(root, text="Confirm", command=open_main_form, font = (fontstyle, 30), fg="green")
openMainForm.place(x=250, y=300) #this is the button in the first window to open the main form where the user can enter their details such as age, gender, etc.

def results_page(event=None): #the function to open the MHR interface
    global RESULTSform #globalised variable

    main_input.withdraw()

    if txt_Age.get() == "" and txt_Gender.get() == "" and txt_Weight.get() == "" and txt_Height.get() == "":
        tkinter.messagebox.showerror("Error", "No Details Given")
        main_input.update()
        main_input.deiconify()
    elif txt_Age.get() == "" or txt_Gender.get() == "" or txt_Weight.get() == "" or txt_Height.get() == "":
        tkinter.messagebox.showerror("Error", "Insufficient Details Given")
        main_input.update()
        main_input.deiconify()
    elif txt_Age.get() == "0":
        tkinter.messagebox.showerror("Error", "Invalid age entered.")
        main_input.update()
        main_input.deiconify()
    else:
        RESULTSform = tkinter.Toplevel()
        
        RESULTSform.title("Health Results")
        RESULTSform.geometry("670x520")
            
        def ireturn():
            main_input.update()
            main_input.deiconify()
            RESULTSform.destroy()

            txt_Age.delete("0", tkinter.END)
            txt_Gender.delete("0", tkinter.END)
            txt_Weight.delete("0", tkinter.END)
            txt_Height.delete("0", tkinter.END)

            db = sqlite3.connect("FitnessDatabase.db")
        
        def iexit():
            RESULTSform.destroy()
            tkinter.messagebox.showinfo("Exit", "Thank you for using this service. See you soon!")

        tkinter.Button(RESULTSform, text="Return", command=ireturn, font = (fontstyle, 20), fg="green").place(x=10, y=10)
        tkinter.Label(RESULTSform, text="Results", font = (fontstyle, 70), padx=10, pady=10, bg="green").place(x=180, y=10)
        tkinter.Button(RESULTSform, text="Exit", command=iexit, font = (fontstyle, 20), fg="green").place(x=580,y=10)

        MHRformula = 220 - int(txt_Age.get()) #this is the formula to calculate the MHR according to the details entered by the user
        #the get method takes the content of the textbox and int means the content is an integer

        BMIformula = float(txt_Weight.get())/((float(txt_Height.get()) / 100) ** 2)
        if BMIformula < 16:
            category = "Severe Thinness"
        elif BMIformula > 16 and BMIformula < 17:
            category = "Moderate Thinness"
        elif BMIformula > 17 and BMIformula < 18.5:
            category = "Mild Thinness"
        elif BMIformula > 18 and BMIformula < 25:
            category= "Normal"
        elif BMIformula > 25 and BMIformula < 30:
            category = "Overweight"
        elif BMIformula > 30 and BMIformula < 35:
            category = "Obese Class 1"
        elif BMIformula > 35 and BMIformula < 40:
            category = "Obese Class 2"
        else:
            category = "Obese Class 3"

        if txt_Gender.get() == "M" or txt_Gender.get() == "Male" or txt_Gender.get() == "m" or txt_Gender.get() == "male":
            BMRformula = (float(txt_Height.get()) * 6.25) + (float(txt_Weight.get()) * 9.99) - (int(txt_Age.get()) * 4.92) + 5
            IBWformula = 50 + (2.3 * ((float(txt_Height.get()) / 2.54) - 60))
            
        elif txt_Gender.get() == "F" or txt_Gender.get() == "Female" or txt_Gender.get() == "f" or txt_Gender.get() == "female":
            BMRformula = (float(txt_Height.get()) * 6.25) + (float(txt_Weight.get()) * 9.99) - (int(txt_Age.get()) * 4.92) - 161
            IBWformula = 45 + (2.3 * ((float(txt_Height.get()) / 2.54) - 60))

        tkinter.Label(RESULTSform, text="Maximum Heart Rate", font=(fontstyle, label_font_size), padx=10, pady=10, fg="green").place(x=60,y=150)
        lbl_MHR = tkinter.Label(RESULTSform, text=MHRformula, fg = "red", font = (fontstyle, label_font_size), padx=10, pady=10)
        lbl_MHR.place(x=450, y=150)

        tkinter.Label(RESULTSform, text="Basal Metabolic Rate", font=(fontstyle, label_font_size), padx=10, pady=10, fg="green").place(x=60, y=220)
        lbl_BMR = tkinter.Label(RESULTSform, text=round(BMRformula, 2), fg = "red", font=(fontstyle, label_font_size), padx=10, pady=10)
        lbl_BMR.place(x=450, y=220)

        tkinter.Label(RESULTSform, text="Ideal Body Weight", font=(fontstyle, label_font_size), padx=10, pady=10, fg="green").place(x=85, y=290)
        lbl_IBW = tkinter.Label(RESULTSform, text=round(IBWformula, 2), fg = "red", font=(fontstyle, label_font_size), padx=10, pady=10)
        lbl_IBW.place(x=450, y=290)

        tkinter.Label(RESULTSform, text="Body Mass Index", font=(fontstyle, label_font_size), padx=10, pady=10, fg="green").place(x=85,y=360)
        lbl_BMI = tkinter.Label(RESULTSform, text=round(BMIformula, 2), fg = "red", font=(fontstyle, label_font_size), padx=10, pady=10)
        lbl_BMI.place(x=450, y=360)

        tkinter.Label(RESULTSform, text="Classification", font=(fontstyle, label_font_size), padx=10, pady=10, fg="green").place(x=115, y=430)
        lbl_Category = tkinter.Label(RESULTSform, text=category, fg = "red", font=(fontstyle, label_font_size), padx=10, pady=10)
        lbl_Category.place(x=450, y=430)
        
        cursor.execute('''INSERT INTO ClientDetails(ClientID, TName, CName, Age, Gender, Weight, Height)
                       VALUES(?, ?, ?, ?, ?, ?, ?)''',
                      (None, txt_TrainerName.get(), txt_CustomerName.get(), txt_Age.get(), txt_Gender.get(), txt_Weight.get(), txt_Height.get()))
        
        cursor.execute('''INSERT INTO BodyDetails(ClientID, MHR, IdealWeight, BMR, BMI, Category)
                       VALUES(?, ?, ?, ?, ?, ?)''',
                      (None, int(MHRformula), float(round(BMRformula, 2)), float(round(IBWformula, 2)), float(round(BMIformula, 2)), category))
        
        db.commit()

root.mainloop()

    
    

    




