from tkinter import *
from tkinter import messagebox

from cryptography import exceptions

from random import SystemRandom

from crypto import *
from utils import *
from pm import *

GEOMETRY = "300x350"
W = 300
H = 1
BUTTON_W = 30
TITLE_H = 3

SCREEN_TITLE_SIZE = 15
SCREEN_TEXT_SIZE = 11

def centerWindow(wind):
    mainScreen.eval('tk::PlaceWindow %s center' % wind.winfo_pathname(wind.winfo_id()))



def register():
    global registerScreen
    registerScreen = Toplevel(mainScreen)
    registerScreen.title("Register")
    registerScreen.geometry(GEOMETRY)
    centerWindow(registerScreen)

    Label(registerScreen, text="Register", bg="grey", width=W, height=TITLE_H, font=("Consolas", SCREEN_TITLE_SIZE)).pack()

    leaveBlank(registerScreen)

    user = StringVar()
    pswrd = StringVar()

    Label(registerScreen, text="username*", width=W, height=H, font=("Consolas", SCREEN_TEXT_SIZE)).pack()
    Entry(registerScreen, width=int(W/2), justify="center", textvariable=user).pack()

    Label(registerScreen, text="password*", width=W, height=H, font=("Consolas", SCREEN_TEXT_SIZE)).pack()
    Entry(registerScreen, width=int(W/2), justify="center", textvariable=pswrd).pack()

    leaveBlank(registerScreen)

    def register_user():
        username = user.get()
        password = pswrd.get()

        encrypted_pass  = encrypt(password,getKey(username, password))

        fileName = username+".key"

        writeHidden(fileName, encrypted_pass)

        registerScreen.destroy()

    Button(registerScreen, bg="gray", text="Register", width=BUTTON_W, height = H, command=register_user).pack()





def passwordManager():
    global passwordManagerScreen
    passwordManagerScreen = Toplevel(mainScreen)
    passwordManagerScreen.title("Login")
    passwordManagerScreen.geometry("500x600")
    centerWindow(passwordManagerScreen)

    Label(passwordManagerScreen, text="Password Manager", bg="grey", width=500, height=TITLE_H, font=("Consolas", SCREEN_TITLE_SIZE)).pack()
    
    leaveBlank(passwordManagerScreen)

    passm = PassManager.loadPM(currentUser)
    l1 = Listbox(passwordManagerScreen)
    l1.insert(END, *passm.getlinks())
    l1.pack()
    # -----------  -----------  ----------- Start of inner function addPassword -----------  -----------  ----------- 
    def addPassword():
        global addPasswordScreen
        addPasswordScreen = Toplevel(passwordManagerScreen)
        addPasswordScreen.title("add password")
        addPasswordScreen.geometry(GEOMETRY)
        centerWindow(addPasswordScreen)

        Label(addPasswordScreen, text="Add Password", bg="grey", width=500, height=TITLE_H, font=("Consolas", SCREEN_TITLE_SIZE)).pack()
        
        leaveBlank(addPasswordScreen)

        link = StringVar()
        username = StringVar()
        passwrd = StringVar()

        Label(addPasswordScreen, text="URL/website*", width=W, height=H, font=("Consolas", SCREEN_TEXT_SIZE)).pack()
        Entry(addPasswordScreen, width=int(W/2), justify="center", textvariable=link).pack()

        Label(addPasswordScreen, text="username*", width=W, height=H, font=("Consolas", SCREEN_TEXT_SIZE)).pack()
        Entry(addPasswordScreen, width=int(W/2), justify="center", textvariable=username).pack()

        Label(addPasswordScreen, text="password*", width=W, height=H, font=("Consolas", SCREEN_TEXT_SIZE)).pack()
        Entry(addPasswordScreen, width=int(W/2), justify="center", textvariable=passwrd).pack()

        def generatePass():
            rand = SystemRandom()
            minu = "abcdefghijklmnopqrstuvwxyz"
            uppe = minu.upper()
            numbers = "0123456789"
            special = "&~#'{([-_\`@^=+*$%§])}"
            passw = str()
            while len(passw) < 16:
                for _ in range(rand.randint(1, 2)):
                    passw += rand.choice(minu)
                for _ in range(rand.randint(1, 2)):
                    passw += rand.choice(uppe)
                for _ in range(rand.randint(1, 2)):
                    passw += rand.choice(numbers)
                for _ in range(rand.randint(1, 2)):
                    passw += rand.choice(special)

            passwrd.set(passw)
        
        Button(addPasswordScreen, bg="gray", text="Generate random password", width=BUTTON_W, height = H, command=generatePass).pack()

        leaveBlank(addPasswordScreen)

        def saveInfos():

            
            passm.append(link.get(), username.get(), passwrd.get())
            passm.dump()

            addPasswordScreen.destroy()

            l1.delete(0, END)
            l1.insert(END, *passm.getlinks())

        Button(addPasswordScreen, bg="gray", text="Save", width=BUTTON_W, height = H, command=saveInfos).pack()


        # -----------  -----------  ----------- end of inner function addPassword -----------  -----------  ----------- 

    Button(passwordManagerScreen, bg="gray", text="Add New Password", width=BUTTON_W, height = H, command=addPassword).pack()

    leaveBlank(passwordManagerScreen)

    def openLink():
        try:
            selected_link = l1.get(l1.curselection()[0])
        except IndexError:
            messagebox.showinfo("Error", "Choose a link or submit one")
            return

        global openLinkScreen
        openLinkScreen = Toplevel(passwordManagerScreen)
        openLinkScreen.title(selected_link)
        openLinkScreen.geometry(GEOMETRY)
        centerWindow(openLinkScreen)

        Label(openLinkScreen, text=selected_link, bg="grey", width=500, height=TITLE_H, font=("Consolas", SCREEN_TITLE_SIZE)).pack()
        
        leaveBlank(openLinkScreen)
        


        
    Button(passwordManagerScreen, bg="gray", text="Open", width=BUTTON_W, height = H, command=openLink).pack()

    


def loginInto(username):
    
    global loginScreen
    loginScreen = Toplevel(mainScreen)
    loginScreen.title("Login")
    loginScreen.geometry(GEOMETRY)
    centerWindow(loginScreen)

    Label(loginScreen, text="Login", bg="grey", width=W, height=TITLE_H, font=("Consolas", SCREEN_TITLE_SIZE)).pack()

    leaveBlank(loginScreen)

    Label(loginScreen, text="username*", width=W, height=H, font=("Consolas", SCREEN_TEXT_SIZE)).pack()
    Label(loginScreen, text=username, bg="white", width=W, height=H, font=("Consolas", SCREEN_TEXT_SIZE - 2)).pack()

    leaveBlank(loginScreen)

    given_password = StringVar()
    Label(loginScreen, text="password*", width=W, height=H, font=("Consolas", SCREEN_TEXT_SIZE)).pack()
    Entry(loginScreen, show="*", width=int(W/2), justify="center", textvariable=given_password).pack()

    leaveBlank(loginScreen)

    def login_user():
        passwrd = given_password.get()

        key = getKey(username, passwrd)
        data = readData(username)

        try:
            decrypt(data[0], key)
        except :
            messagebox.showwarning(title="wrong password", message="you have entered the wrong password check capslock")
            return
        
        loginScreen.destroy()
        global currentUser
        currentUser = username
        passwordManager()
        

    Button(loginScreen, bg="gray", text="login", width=BUTTON_W, height = H, command=login_user).pack()


def login():
    global loginSelection
    loginSelection = Toplevel(mainScreen)
    loginSelection.title("Login")
    loginSelection.geometry(GEOMETRY)
    centerWindow(loginSelection)

    Label(loginSelection, text="Login", bg="grey", width=W, height=TITLE_H, font=("Consolas", SCREEN_TITLE_SIZE)).pack()
    
    leaveBlank(loginSelection)
    
    l = Listbox(loginSelection)
    l.pack()

    listOfUsers = getFileNameByExt("key")

    for user in listOfUsers:
        l.insert(END, user)
    
    def validateSelection():
        try:
            selected_username = l.get(l.curselection()[0])

        except IndexError:
            messagebox.showinfo("Error", "Choose an account or register")
            return

        loginSelection.destroy()
        loginInto(selected_username)

    Button(loginSelection, bg="gray", text="login", width=BUTTON_W, height = H, command=validateSelection).pack()



def createLoginScreen(title : str, geometry : str):
    global mainScreen
    mainScreen = Tk()
    mainScreen.title(title)
    mainScreen.geometry(geometry)
    centerWindow(mainScreen)
    Label(text=title, bg="grey", width=W, height=TITLE_H, font=("Consolas", 13)).pack()

    leaveBlank(mainScreen)

    Button(text="Login", width=BUTTON_W, height=4, command=login).pack()
    Label(text="").pack()
    Button(text="Register", width=BUTTON_W, height=4, command=register).pack()
    mainScreen.mainloop()

if __name__ == "__main__":
    createLoginScreen("Password Manager", GEOMETRY)
