from gui import *

def main():
    # main window
    mainWindow = newWindow(title="Password Register")
    mainWindow.center()
    mainWindow.leaveBlank(size=5)
    def bLoginSelect():
        loginSelect= newWindow(parent=mainWindow, title="Login")
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
            loginInto = newWindow(mainWindow, title="welcome, "+selected_username+" !")
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
                enterAccount = newWindow(mainWindow, title="My account")
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

                    linkSelected = newWindow(mainWindow, title=selected_link)
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

                        userPass = newWindow(mainWindow, title=selected_info_username)
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

    mainWindow.addButton(text="Login", command=bLoginSelect)
    # start of bRegister
    def bRegister():
        RegisterScreen= newWindow(parent=mainWindow, title="Register")
        RegisterScreen.center()
        RegisterScreen.leaveBlank()
        RegisterScreen.addLabel(text="Username*")
        rUsername = RegisterScreen.addEntry()
        RegisterScreen.addLabel(text="Password*")
        rPassword = RegisterScreen.addEntry()
        RegisterScreen.leaveBlank()
        # start of bRegisterUser
        def bRegisterUser():
            
            given_username = rUsername.get()
            given_password = rPassword.get()

            encrypted_pass  = encrypt(given_password,getKey(given_username, given_password))

            writeHidden(given_username, encrypted_pass)

            RegisterScreen.destroy()
            # end of bRegisterUser
        RegisterScreen.addButton(text="Register", command=bRegisterUser)
        # end of bRegister
    mainWindow.addButton(text="Register", command=bRegister)
    mainWindow.leaveBlank(7)
    mainWindow.addLabel(text="🐱‍👤github.com/T-Shai/PasswordManager🐱‍👤", font=(DEFAULT_FONT, 8), bg="SlateGray2")
    mainWindow.mainloop()

if __name__ == "__main__":
    main()