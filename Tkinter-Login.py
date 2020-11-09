import tkinter as tk; from tkinter import messagebox; from tkinter import ttk
import random
import string
import mysql.connector; from mysql.connector import Error; from mysql.connector import errorcode
from captcha.image import ImageCaptcha
import os
from PIL import Image, ImageTk
import hashlib
root = tk.Tk()
root.geometry("500x400+500+200")
root.title("JVD")
logged_in = False
failed_captcha = 0
failed_login = 0
captcha_on = False

def sign_in():                  #Checking if the input equals to the data in the files to login, or give an error if it is not
    global logged_in; global failed_login; global captcha_on
        
        #return
    email = ut.get()     #Getting the user input from login_page() entries
    password = pt.get()
    failed_login = failed_login
    logged_in = False
    root.update()

    if captcha_on == True:
        captcha_input = captcha_entry.get()
        if captcha_text != captcha_input.upper():
            messagebox.showerror("Error", "Captcha incorrect, try again!")
            captcha_show()
            pt.delete('0', tk.END)
            root.update()
            return
    
    if email == "" or password == "":            #If the username or password entry is empty, show error
        messagebox.showerror("Error", "Please fill in all fields")
        return

    else:
        encrypting(password)
        sql_select_Query = "select * from personal_information"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        for row in records:
            if row[1] == email:
                if row[2] == key:
                    print("logged in")
                    failed_login = 0
                    global logged_username
                    logged_username = row[3]
                    logged_in = True
                    captcha_on = False
                    break
                    
        if logged_in == False:
            pt.delete('0', tk.END)
            failed_login += 1
            if failed_login >= 3:
                captcha_on = True
                messagebox.showerror("Error", "Username or Password is not correct\nMaybe you would like to sign up?")
                captcha_show()
            else:
                messagebox.showerror("Error", "Username or Password is not correct\nMaybe you would like to sign up?")
            return
        delete_key()
        os.remove('captcha.jpg')
        home_page()

###################################################################################

def sign_up():
    global failed_captcha
    failed_captcha = failed_captcha
    username = sut.get()    #Getting the user input from signup_page() entries
    password = spt.get()
    #age = age_entry.get()
    email = email_entry.get()
    captcha_input = captcha_entry.get()
    try:
        age = int(age_entry.get())
    except:
        age = "nan"
        messagebox.showerror("Error", "The age field should be a number")
        return

    if captcha_text != captcha_input.upper():
        messagebox.showerror("Error", "Captcha incorrect, try again!")
        failed_captcha += 1
        if failed_captcha >= 3:
            sut.delete('0', tk.END)
            spt.delete('0', tk.END)
            email_entry.delete('0', tk.END)
            age_entry.delete('0', tk.END)
            failed_captcha = 0
        captcha_entry.delete('0', tk.END)
        captcha()
        root.update()
        return
    
    elif len(username) > 20:
        messagebox.showerror("Error", "Name can't be longer than 20 characters")
        return
    elif len(password) > 100:
        messagebox.showerror("Error", "Password can't be longer than 100 characters")
        return
    elif username == "" or password == "":    #If username or password is empty, give error
        messagebox.showerror("Error", "Please fill in all fields")
        return
    elif len(password) < 6:
        messagebox.showerror("Error", "Passwords needs to be longer than 5 characters!")
        return
    elif username.isspace() == True or password.isspace() == True or email.isspace() == True:      #If username or password contains only spaces, give error
        messagebox.showerror("Error", "None of the fields can only contain spaces!")
        return
    elif " " in email:
        messagebox.showerror("Error", "There should not be a space in an email")
        return
    elif age < 8:
        messagebox.showerror("Error", "You are too young to register")
        return
    elif age > 123:
        messagebox.showerror("Error", "Please enter a realistic age\n\n(You're not older than the oldest person in the world)")
        return

    else:
        sql_select_Query = "select * from personal_information"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        for row in records:
            if row[1] == email:
                messagebox.showerror("Error", "Your email is already registered\nMaybe you would like to login?")
                return

        encrypting(password)
        mySql_insert_query = """INSERT INTO personal_information (emails, passwords, names, ages) 
                           VALUES 
                           ('{}', '{}', '{}', {}) """.format(email, key, username, age) ################################# NEED FULL NAME AND AGE
        cursor = connection.cursor()
        cursor.execute(mySql_insert_query)
        connection.commit()
        cursor.close()
        print(username + " registered")
        failed_captcha = 0
        delete_key()
        os.remove('captcha.jpg')
        login_page() #After registering, move user to login
            

###################################################################################
#Entry the input for both username and password fields          
def login_page():
    delete_screen()
    global ut; global pt; global ul; global pl; global logged_in; global signin   
    
    ut = tk.Entry()
    pt = tk.Entry(show = "*")
    ut.pack()
    pt.pack()
    ut.place(x = 101, y = 1, height = 20, width = 175)
    pt.place(x = 101, y = 30, height = 20, width = 175)
    loginMessage = ""
    ul = tk.Label(          #Label to show user which entry is for username/password
        text = "Email:",
        font=("Arial", 10),
        fg = "black",
        anchor = "e"
    )
    pl = tk.Label(          #Label to show user which entry is for username/password
        text = "Password:",
        font=("Arial", 10),
        fg = "black",
        anchor = "e"
    )
    ul.pack()
    pl.pack()
    ul.place(x = 1, y = 1, height = 20, width = 100)
    pl.place(x = 1, y = 30, height = 20, width = 100)

    signin = tk.Button(     #signin button
        text = "Sign in",
        width = 10,
        height = 1,
        bg = "green",
        fg = "black",
        command=lambda: sign_in()
    )
    signin.pack()
    signin.place(x = 145.5, y = 60)

    logged_in = tk.Label(   #Label to show the login worked
        font=("Bebas", 10),
        fg = "black",
        anchor = "center"
    )
    logged_in.pack()
    logged_in.place(x = 200, y = 120)

    
    topframe = tk.Frame(root)
    topframe.pack(anchor="ne")
    home_button = HoverButton(topframe, activebackground='green', text="Home", fg="black", width=10, height=1, command=lambda: home_page())
    home_button.pack( side = tk.RIGHT, padx=5 )

    signup_button = HoverButton(topframe, activebackground='green', text="Sign up", fg="black", width=10, height=1, command=lambda: signup_page())
    signup_button.pack( side = tk.RIGHT, padx=5 )
###################################################################################
def signup_page():
    delete_screen()
    topframe = tk.Frame(root)
    topframe.pack(anchor="ne")

    home_button = HoverButton(topframe, activebackground='green', text="Home", fg="black", width=10, height=1, command=lambda: home_page())
    home_button.pack( side = tk.RIGHT, padx=5)

    signin_button = HoverButton(topframe, activebackground='green', text="Sign in", fg="black", width=10, height=1, command=lambda: login_page())
    signin_button.pack( side = tk.RIGHT, padx=5)
    
    global sut; global email_entry; global spt; global age_entry; global slogged_in; global signup; global spl; global sul; global captcha_entry
    
    sut = tk.Entry()
    email_entry = tk.Entry()
    spt = tk.Entry(show = "*")
    age_entry = tk.Entry()
    
    sut.pack()
    email_entry.pack()
    spt.pack()
    age_entry.pack()

    sut.place(x = 101, y = 1, height = 20, width = 175)
    email_entry.place(x = 101, y = 30, height = 20, width = 175)
    spt.place(x = 101, y = 60, height = 20, width = 175)
    age_entry.place(x = 101, y = 90, height = 20, width = 175)

    
    loginMessage = ""
    sul = tk.Label(          #Label to show user which entry is for username/password
        text = "Name:",
        font=("Arial", 10),
        fg = "black",
        anchor = "e"
    )
    spl = tk.Label(          #Label to show user which entry is for username/password
        text = "Password:",
        font=("Arial", 10),
        fg = "black",
        anchor = "e"
    )
    email_label = tk.Label(          #Label to show user which entry is for username/password
        text = "Email:",
        font=("Arial", 10),
        fg = "black",
        anchor = "e"
    )
    age_label = tk.Label(          #Label to show user which entry is for username/password
        text = "Age:",
        font=("Arial", 10),
        fg = "black",
        anchor = "e"
    )
    age_label.pack()
    email_label.pack()
    sul.pack()
    spl.pack()
    sul.place(x = 1, y = 1, height = 20, width = 100)
    spl.place(x = 1, y = 60, height = 20, width = 100)
    email_label.place(x = 1, y = 30, height = 20, width = 100)
    age_label.place(x = 1, y = 90, height = 20, width = 100)

    captcha_entry = tk.Entry()
    captcha_entry.pack()
    captcha_entry.place(x = 101, y = 190, height = 20, width = 175)
    
    captcha_label = tk.Label(
        text = "CAPTCHA:",
        font=("Arial", 10),
        fg = "black",
        anchor = "e"
    )
    captcha_label.pack()
    captcha_label.place(x = 1, y = 190, height = 20, width = 100)
    captcha()

    signup = tk.Button(     #signin button
        text = "Sign up",
        width = 10,
        height = 1,
        bg = "green",
        fg = "black",
        command=lambda: sign_up()
    )
    signup.pack()
    signup.place(x = 145.5, y = 225)

###################################################################################

def home_page():
    global failed_captcha; global failed_login; global captcha_on
    captcha_on = False
    failed_captcha = 0
    failed_login = 0
    delete_screen()
    root.config(bg = "#a8a8a8")
    s = ttk.Style()
    s.theme_use('clam')
    frame = tk.Frame(root)
    frame.pack()
    topframe = tk.Frame(root)
    topframe.pack(anchor="ne")
    topleftframe = tk.Frame(root)
    topframe.config( bg = "#a8a8a8")

    try:
        os.remove('captcha.jpg')
    except:
        pass
    if logged_in == True:
        global logout_button
        topleftframe.pack(anchor="nw")
        testlabel = tk.Label(
            text = logged_username,
            bg = "#a8a8a8",
            fg = "black",
            anchor = "nw",
            font = ("Ariel", 10)
        )
        testlabel.pack()
        testlabel.place(x = 5, y = 5)
        root.configure(bg = "#a8a8a8")
        logout_button = HoverButton(topframe, activebackground='green', text="Logout", fg="black", width=10, height=1, bg = "white", anchor = "c", command=lambda: logout())
        logout_button.pack( side = tk.RIGHT, padx=10) 

    else:
        signin_button = HoverButton(topframe, text="Sign in", fg="black", bg = "white", width=10, height=1, activebackground='green', command=lambda: login_page())
        signin_button.pack( side = tk.RIGHT, padx=10)

        signup_button = HoverButton(topframe, text="Sign up", fg="black",  bg = "white", width=10, height=1, activebackground='green', command=lambda: signup_page())
        signup_button.pack( side = tk.RIGHT )

###################################################################################

class HoverButton(tk.Button):
    def __init__(self, master, **kw):
        tk.Button.__init__(self,master=master,**kw)
        self.defaultBackground = self["background"]
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self['background'] = self['activebackground']

    def on_leave(self, e):
        self['background'] = self.defaultBackground

###################################################################################
def delete_screen() :
    s = root.winfo_children()

    for i in s :
        try:
            i.destroy()
        except:
            i.delete()
    root.config(bg = "SystemButtonFace")

def logout():
    global logged_in
    logged_in = False
    print("logged out")
    home_page()


def captcha():
    letters = string.ascii_uppercase
    length = random.randint(4,5)
    global captcha_text; global captcha_img
    captcha_text = ''.join(random.choice(letters) for i in range(length))
        
    img = ImageCaptcha(width=160, height=60, fonts=None, font_sizes=None)
    image = img.generate_image(captcha_text)
    image.save('captcha.jpg')
    open_image = Image.open("captcha.jpg")
    photo = ImageTk.PhotoImage(open_image)
    captcha_img = tk.Label(image=photo)
    captcha_img.image = photo
    captcha_img.pack()
    captcha_img.place(y = 120, x = 100)

def captcha_show():
    global captcha_entry
    captcha_entry = tk.Entry()

    captcha_label = tk.Label(
        text = "CAPTCHA:",
        font=("Arial", 10),
        fg = "black",
        anchor = "e"
    )
    
    captcha()
    captcha_entry.pack()
    captcha_label.pack()

    captcha_img.place(y = 60, x = 100)
    captcha_entry.place(x = 101, y = 130, height = 20, width = 175)         #####################################
    captcha_label.place(x = 1, y = 130, height = 20, width = 100)
    signin.place(x = 145.5, y = 160)

def encrypting(password):
    result = hashlib.sha384(password.encode())
    global key
    key = result.hexdigest()

def delete_key():
    global key
    del key
try:
    connection = mysql.connector.connect(host='host', #Use localhost or an online host such as sql7.freesqldatabase.com
                                         database='database name',  #Database name
                                         user='username',           #Username
                                         password='Password')     #Password (with localhost standard is '' or 'root')
except mysql.connector.Error as error:
    print("Failed to insert record into table {}".format(error))

home_page()
root.mainloop()
