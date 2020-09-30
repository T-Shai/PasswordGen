from tkinter import *
from tkinter import messagebox

from cryptography import exceptions

from random import SystemRandom

from crypto import *
from utils import *
from pm import *

# CONSTANTS 
DEFAULT_GEOMETRY = "300x350"
DEFAULT_TITLE = "new window"
DEFAULT_BG_COLOUR = "slate gray"

DEFAULT_LABEL_TITLE = "new label"
DEFAULT_LABEL_WIDTH = 200
DEFAULT_LABEL_HEIGHT = 1
DEFAULT_LABEL_BG = "light slate gray"

DEFAULT_ENTRY_TITLE = "new entry"
DEFAULT_ENTRY_WIDTH = 200
DEFAULT_ENTRY_HEIGHT = 1
DEFAULT_LABEL_BG = "light grey"

DEFAULT_BUTTON_TITLE = "new button"
DEFAULT_BUTTON_WIDTH = 30
DEFAULT_BUTTON_HEIGHT = 1
DEFAULT_BUTTON_BG = "dark slate gray"

DEFAULT_FONT = "Consolas"
DEFAULT_FONT_SIZE = 12

class newWindow:
    
    

    def __init__(self, parent = None, title = DEFAULT_TITLE, geometry = DEFAULT_GEOMETRY, bg=DEFAULT_BG_COLOUR):
        
        if parent == None:
            # root
            self.window = Tk()
            self.parent = None
            
        else:
            self.window = Toplevel(parent.window)
            self.parent = parent.window
        
        self.window.title(title)
        self.window.geometry(geometry)
        self.window.configure(bg=bg)

        self.buttons = list()
        self.labels = list()
        self.entries = list()

        self.addLabel(text=title, font_size=15)

    def isRoot(self):
        return self.parent == None

    def addButton(self, bg=DEFAULT_BUTTON_BG,text=DEFAULT_BUTTON_TITLE, width=DEFAULT_BUTTON_WIDTH, height=DEFAULT_BUTTON_HEIGHT, command=None):
        b = Button(self.window, bg=bg, text=text, width=width, height =height, command=command)
        b.pack()
        self.buttons.append(b)
        return b
    
    def addLabel(self, bg=DEFAULT_LABEL_BG,text=DEFAULT_LABEL_TITLE, width=DEFAULT_LABEL_WIDTH, height=DEFAULT_LABEL_HEIGHT, font=DEFAULT_FONT, font_size=DEFAULT_FONT_SIZE):
        l = Label(self.window, text=text, bg=bg, width=width, height=height, font=(font, font_size))
        l.pack()
        self.labels.append(l)
        return l

    def addListbox(self, *data : list):
        l = Listbox(self.window)
        l.insert(END, *data)
        l.pack()
        return l
    
    def addEntry(self, text="", hidden=False, width=DEFAULT_ENTRY_WIDTH):
        if hidden:
            show = "*"
        else:
            show = ""

        e = Entry(self.window, show=show, width = width,justify=CENTER)
        e.insert(0, text)
        e.pack()
        
        return e


    def leaveBlank(self, size=1):
        self.addLabel(text="", height=size, bg=self.window["bg"])
    
    def destroy(self):
        self.window.destroy()

    def center(self):
        #root.window.eval('tk::PlaceWindow %s center' % self.window.winfo_pathname(self.window.winfo_id()))

        positionRight = int(self.window.winfo_screenwidth()/2 - self.window.winfo_reqwidth()/2)
        positionDown = int(self.window.winfo_screenheight()/2 - self.window.winfo_reqheight()/2)
        
        self.window.geometry("+{}+{}".format(positionRight, positionDown))
    
    def mainloop(self):
        if self.isRoot():
            self.window.mainloop()
        else:
            raise RuntimeError("trying to mainloop a topLevel").with_traceback()
    
if __name__ == "__main__":
    main = newWindow(title="Password Register")
    main.center()
    main.leaveBlank(size=5)
    def bLoginSelect():
        loginSelect= newWindow(parent=main, title="Login")
        loginSelect.center()
        loginSelect.leaveBlank()
        loginSelect.addLabel(text="Registered users")
        loginSelect.leaveBlank()
        # get users
        listOfUsers = getFileNameByExt("key")
        lbUsers = loginSelect.addListbox(*listOfUsers)
        loginSelect.leaveBlank()

        # start of bLoginInto 
        def bLoginInto():
            try:
                selected_username = lbUsers.get(lbUsers.curselection()[0])
            except IndexError:
                messagebox.showinfo("Error", "Choose an account or register")
                return
            
            loginSelect.destroy()
            loginInto = newWindow(main, title="welcome, "+selected_username+" !")
            loginInto.center()
            loginInto.leaveBlank()

            loginInto.addLabel(text="password*")
            given_password_var = loginInto.addEntry(hidden=True)
            loginInto.leaveBlank()

            # start of benterAccount
            def benterAccount():
                given_password = given_password_var.get()

                key = getKey(selected_username, given_password)
                data = readData(selected_username)

                try:
                    decrypt(data[0], key)
                except:
                    messagebox.showwarning(title="Login Error", message="Username and password don't match ! (maybe check capslock) ")
                    return
                
                loginInto.destroy()
                enterAccount = newWindow(main, title="My account")
                enterAccount.center()
                enterAccount.leaveBlank()

                passM = PassManager.loadPM(selected_username)

                lblink = enterAccount.addListbox(*passM.getlinks())
                lblink.pack()
                enterAccount.leaveBlank()
                
                # start of baddPassword
                def baddPassword():
                    addPassword = newWindow(title="Add Password")
                    addPassword.center()
                    addPassword.leaveBlank()
                    
                    addPassword.addLabel(text="URL/WEBSITE*")
                    newLink_var = addPassword.addEntry()

                    addPassword.addLabel(text="Username*")
                    newUsername_var = addPassword.addEntry()
                    
                    addPassword.addLabel(text="Password*")
                    newPass_var = addPassword.addEntry()
                    addPassword.leaveBlank()

                    # start of bsaveNewPass
                    def bsaveNewPass():
                        newLink = newLink_var.get()
                        newUsername = newUsername_var.get()
                        newPass = newPass_var.get()
                        if newLink == "" or newUsername == "" or newPass == "":
                            return
                        
                        encrypted_pass = encrypt(newPass, key).decode()
                        passM.append(newLink, newUsername, encrypted_pass)
                        lblink.insert(END, newLink)
                        addPassword.destroy()
                        # end of bsaveNewPass
                    addPassword.addButton(text="Save", command=bsaveNewPass)

                    # start of bgeneratePass
                    def bgeneratePass():
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
                        newPass_var.delete(0, END)
                        newPass_var.insert(0, passw)
                        # end of bgeneratePass
                    addPassword.addButton(text="Generate Password", command=bgeneratePass)
                    addPassword.leaveBlank()
                    
                enterAccount.addButton(text="New Password", command=baddPassword)
                enterAccount.leaveBlank()

                # start of bselectedLink
                def bselectedLink():
                    try:
                        selected_link = lblink.get(lblink.curselection()[0])
                    except IndexError:
                        return

                    linkSelected = newWindow(main, title=selected_link)
                    linkSelected.center()
                    linkSelected.leaveBlank()
                    linfos = passM.getInfos(selected_link)
                    lusers = [user for user,_ in linfos]
                    lpasswords = [passw for _,passw in linfos]

                    lbusers = linkSelected.addListbox(*lusers)
                    linkSelected.leaveBlank()

                    # start of bopenUsername
                    def bopenUsername():
                        try:
                            selected_info_username = lbusers.get(lbusers.curselection()[0])
                        except IndexError:
                            return
                        
                        selected_passw = passM.getPass(selected_link, selected_info_username)
                        decrypted_pass = decrypt(selected_passw, key)

                        userPass = newWindow(main, title=selected_info_username)
                        userPass.center()
                        userPass.leaveBlank()
                        userPass.addLabel(text="Your Password")
                        userPass.leaveBlank()
                        preview_pass = userPass.addEntry(decrypted_pass)
                        userPass.leaveBlank()

                        # start of bmodifyPass
                        def bmodifyPass():
                            curr_pass = preview_pass.get()
                            if curr_pass == "":
                                return
                            encrypted_curr_pass = encrypt(curr_pass, key).decode()
                            passM.append(selected_link, selected_info_username, encrypted_curr_pass)
                            preview_pass.delete(0, END)

                            selected_passw = passM.getPass(selected_link, selected_info_username)
                            decrypted_pass = decrypt(selected_passw, key)
                            
                            preview_pass.insert(END, decrypted_pass)
                            userPass.destroy()
                            # end of bmodifyPass
                        userPass.addButton(text="Modify", command=bmodifyPass)
                        userPass.leaveBlank()

                        # start of bdeletePass
                        def bdeletePass():
                            passM.delete(selected_link, selected_info_username)
                            users = passM.getUsers(selected_link)
                            lblink.delete(0, END)
                            links = passM.getlinks()
                            lblink.insert(END , *links)
                            userPass.destroy()
                            
                            # end of bdeletePass
                        userPass.addButton(text="Delete", command=bdeletePass)
                        # end of bopenUsername
                    linkSelected.addButton(text="Select", command=bopenUsername)
                    # end of bselectedLink
                enterAccount.addButton(text="Select", command=bselectedLink)
                # end of benterAccount
            loginInto.addButton(text="Login", command=benterAccount)
            # end of bloginInto
        loginSelect.addButton(text="Select", command=bLoginInto)

    main.addButton(text="Login", command=bLoginSelect)
    def bRegister():
        RegisterScreen= newWindow(parent=main, title="Register")
        RegisterScreen.center()
        RegisterScreen.leaveBlank()
        RegisterScreen.addLabel(text="Username*")
        rUsername = RegisterScreen.addEntry()
        RegisterScreen.addLabel(text="Password*")
        rPassword = RegisterScreen.addEntry()
        # TODO validation est enregistrement du compte
        RegisterScreen.leaveBlank()

    main.addButton(text="Register", command=bRegister)
    main.mainloop()