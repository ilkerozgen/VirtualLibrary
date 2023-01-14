from tkinter import messagebox
import tkinter as tk
import tkinter.font as font
from PIL import ImageTk, Image
import os

if __name__ == '__main__':

    largeFont = ("Verdana", 35)
    mediumFont = ("Verdana", 22)
    smallFont = ("Verdana", 12,)
    background = "#2C3333"
    foreground = "#E7F6F2"
    buttonBackground = "#395B64"
    loggedUser = [""]

    class TkinterApp(tk.Tk):
        # Constructor
        def __init__(self, *args, **kwargs):
            tk.Tk.__init__(self, *args, **kwargs)

            # Create and configure the container
            container = tk.Frame(self)
            container.pack(side="top", fill="both", expand=True)
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)

            # Initialize frames in an empty array
            self.frames = {}

            # Iterate through a tuple consisting of the different frames
            for F in (LoginPage, SignUpPage, ForgotPasswordPage, MainPage, SearchPage, AddPage, RemovePage, SettingsPage
                      , ChangePasswordPage):
                frame = F(container, self)

                # Initialize the frame
                self.frames[F] = frame
                frame.grid(row=0, column=0, sticky="nsew")

            # Start the application with LoginPage
            self.show_frame(LoginPage)

        # Function to show a frame.
        def show_frame(self, cont):
            frame = self.frames[cont]
            frame.tkraise()

        # Function for sign in operation
        def sign_in(self, username, password):
            # Get the user data
            file = open('database/userInfo.txt', 'r')
            userInfo = file.readlines()
            file.close()

            usernames = []
            passwords = []

            for i in range(0, len(userInfo)):
                info = userInfo[i].split()
                currentUsername = info[0]
                currentPassword = info[1]
                usernames.append(currentUsername)
                passwords.append(currentPassword)

            # Search for username and password
            userFound = False
            for i in range(0, len(userInfo)):
                if username == usernames[i]:
                    userFound = True

                    if password == passwords[i]:
                        loggedUser[0] = username
                        self.show_frame(MainPage)
                        break
                    else:
                        tk.messagebox.showerror(title="Error", message="Incorrect Password!")

            if not userFound:
                tk.messagebox.showerror(title="Error", message="Username not Found!")

        # Function for sign up operation
        def sign_up(self, username, password, passwordAgain, securityHint):
            # Get the user data
            file1 = open('database/userInfo.txt', 'r')
            userInfo = file1.readlines()
            file1.close()

            usernames = []

            for i in range(0, len(userInfo)):
                info = userInfo[i].split()
                currentUsername = info[0]
                usernames.append(currentUsername)

            # Search for the username
            userFound = False
            for i in range(0, len(userInfo)):
                if username == usernames[i]:
                    userFound = True
                    break

            # Check the requirements
            if not userFound:
                tk.messagebox.showwarning(title="Warning", message="Username already exists!")
            elif username == "":
                tk.messagebox.showwarning(title="Warning", message="Please enter a username!")
            elif ' ' in username:
                tk.messagebox.showwarning(title="Warning", message="Username cannot contain white space!")
            elif ' ' in password:
                tk.messagebox.showwarning(title="Warning", message="Password cannot contain white space!")
            elif password != passwordAgain:
                tk.messagebox.showwarning(title="Warning", message="Passwords are not the same!")
            elif len(password) < 6:
                tk.messagebox.showwarning(title="Warning", message="Password should be at least 6 characters!")
            elif securityHint == "" or securityHint == "Hint":
                tk.messagebox.showwarning(title="Warning", message="Please enter a security hint!")
            elif ' ' in securityHint:
                tk.messagebox.showwarning(title="Warning", message="Security hint cannot contain white space!")
            else:
                # Sign up the user if all requirements are satisfied
                file2 = open('database/userInfo.txt', 'a')
                file2.write("\n" + username + " " + password + " " + securityHint)
                file2.close()
                file3 = open("database/bookAuthors_" + username + ".txt", "w")
                file3.write("defaultAuthor")
                file3.close()
                file4 = open("database/bookLocations_" + username + ".txt", "w")
                file4.write("defaultLocation")
                file4.close()
                file5 = open("database/bookNames_" + username + ".txt", "w")
                file5.write("defaultName")
                file5.close()
                file6 = open("database/bookPages_" + username + ".txt", "w")
                file6.write("defaultPages")
                file6.close()
                tk.messagebox.showinfo(title="Info", message="Sign Up Successful!")
                self.show_frame(LoginPage)

        # Function to get hint
        @staticmethod
        def get_hint(username):
            # Get the user data
            file = open('database/userInfo.txt', 'r')
            userInfo = file.readlines()
            file.close()

            usernames = []
            hints = []

            for i in range(0, len(userInfo)):
                info = userInfo[i].split()
                currentUsername = info[0]
                currentHint = info[2]
                usernames.append(currentUsername)
                hints.append(currentHint)

            userFound = False

            # Search for the username
            for i in range(0, len(userInfo)):
                if username == usernames[i]:
                    userFound = True
                    hint = hints[i]
                    tk.messagebox.showinfo(title="Info", message="Your security hint is: " + hint)
                    break

            if not userFound:
                tk.messagebox.showerror(title="Error", message="Username not Found!")

        # Function for search operation
        @staticmethod
        def search(bookName):
            # Get the data
            file1 = open('database/bookNames_' + loggedUser[0] + '.txt', 'r')
            books = file1.readlines()
            file1.close()

            # Reformat the data to use
            for x in range(0, len(books) - 1):
                books[x] = books[x][:-1]

            # Search for the specified book
            index = -1
            for i in range(0, len(books)):
                if books[i] == bookName:
                    index = i
                    break

            if index == -1:
                tk.messagebox.showwarning(title="Warning", message="'" + bookName + "'" + " is not in your library!")
            else:
                file2 = open('database/bookAuthors_' + loggedUser[0] + '.txt', 'r')
                authors = file2.readlines()
                file2.close()
                file3 = open('database/bookPages_' + loggedUser[0] + '.txt', 'r')
                pages = file3.readlines()
                file3.close()
                file4 = open('database/bookLocations_' + loggedUser[0] + '.txt', 'r')
                locations = file4.readlines()
                file4.close()

                # Reformat the data
                for x in range(0, len(books) - 1):
                    authors[x] = authors[x][:-1]
                    pages[x] = pages[x][:-1]
                    locations[x] = locations[x][:-1]

                tk.messagebox.showinfo(title="Info", message="'" + bookName + "'" + " is found!" + "\n" +
                                                             "Name: " + books[index] + "\n" +
                                                             "Author: " + authors[index] + "\n" +
                                                             "Pages: " + pages[index] + "\n" +
                                                             "Location: " + locations[index])

        # Function for add book operation
        @staticmethod
        def add(bookName, author, pages, location):
            # Get the data
            file = open('database/bookNames_' + loggedUser[0] + '.txt', 'r')
            books = file.readlines()
            file.close()

            # Reformat the data
            for x in range(0, len(books) - 1):
                books[x] = books[x][:-1]

            # Search for the specified book
            bookFound = False
            for i in range(0, len(books)):
                if books[i] == bookName:
                    bookFound = True
                    tk.messagebox.showwarning(title="Warning", message="'" + bookName + "'" + " already exists!")
                    break

            # Check the requirements
            if not bookFound:
                if bookName == "":
                    tk.messagebox.showwarning(title="Warning", message="Please enter a book name!")
                elif author == "":
                    tk.messagebox.showwarning(title="Warning", message="Please enter an author!")
                elif pages == "":
                    tk.messagebox.showwarning(title="Warning", message="Please enter a page number!")
                elif location == "":
                    tk.messagebox.showwarning(title="Warning", message="Please enter a location!")
                else:
                    # Add the book if all requirements are satisfied
                    file1 = open("database/bookAuthors_" + loggedUser[0] + ".txt", "a")
                    file1.write("\n" + author)
                    file1.close()
                    file2 = open("database/bookLocations_" + loggedUser[0] + ".txt", "a")
                    file2.write("\n" + location)
                    file2.close()
                    file3 = open("database/bookNames_" + loggedUser[0] + ".txt", "a")
                    file3.write("\n" + bookName)
                    file3.close()
                    file4 = open("database/bookPages_" + loggedUser[0] + ".txt", "a")
                    file4.write("\n" + pages)
                    file4.close()
                    tk.messagebox.showinfo(title="Info", message="Book Added Successfully!")

        # Function for remove book operation
        @staticmethod
        def remove(bookName):
            # Get the data
            file1 = open('database/bookNames_' + loggedUser[0] + '.txt', 'r')
            books = file1.readlines()
            booksTemp = books
            file1.close()

            # Reformat the data
            for x in range(0, len(booksTemp) - 1):
                booksTemp[x] = booksTemp[x][:-1]

            # Search for the specified book
            index = -1
            for i in range(0, len(booksTemp)):
                print(booksTemp[i])
                if booksTemp[i] == bookName:
                    index = i
                    break

            if index == -1:
                tk.messagebox.showwarning(title="Warning", message="'" + bookName + "'" + " is not in your library!")
            else:
                # Get the data
                file2 = open('database/bookAuthors_' + loggedUser[0] + '.txt', 'r')
                authors = file2.readlines()
                file2.close()
                file3 = open('database/bookPages_' + loggedUser[0] + '.txt', 'r')
                pages = file3.readlines()
                file3.close()
                file4 = open('database/bookLocations_' + loggedUser[0] + '.txt', 'r')
                locations = file4.readlines()
                file4.close()

                # Delete the data in the database
                file5 = open("database/bookAuthors_" + loggedUser[0] + ".txt", "w")
                file5.write("")
                file5.close()
                file6 = open("database/bookLocations_" + loggedUser[0] + ".txt", "w")
                file6.write("")
                file6.close()
                file7 = open("database/bookNames_" + loggedUser[0] + ".txt", "w")
                file7.write("")
                file7.close()
                file8 = open("database/bookPages_" + loggedUser[0] + ".txt", "w")
                file8.write("")
                file8.close()

                # Remove the book
                books.pop(index)
                authors.pop(index)
                pages.pop(index)
                locations.pop(index)

                # Rewrite the data
                file9 = open("database/bookAuthors_" + loggedUser[0] + ".txt", "a")
                file10 = open("database/bookLocations_" + loggedUser[0] + ".txt", "a")
                file11 = open("database/bookNames_" + loggedUser[0] + ".txt", "a")
                file12 = open("database/bookPages_" + loggedUser[0] + ".txt", "a")

                for i in range(0, len(books)):
                    if i == len(books) - 1 and index == len(books):
                        file9.write(authors[i][:-1])
                        file10.write(locations[i][:-1])
                        file12.write(pages[i][:-1])
                    else:
                        file9.write(authors[i])
                        file10.write(locations[i])
                        file12.write(pages[i])

                    if i != 0:
                        file11.write("\n" + books[i])
                    else:
                        file11.write(books[i])

                file9.close()
                file10.close()
                file11.close()
                file12.close()

                tk.messagebox.showinfo(title="Info", message="Book Removed Successfully!")

        # Function for log out operation
        def log_out(self):
            answer = tk.messagebox.askquestion(title="Form", message="Are you sure you want to log out?")
            if answer == "yes":
                loggedUser[0] = ""
                self.show_frame(LoginPage)

        # Function for change password operation
        def change_password(self, oldPassword, newPassword, newPasswordAgain):
            # Get the data
            file = open('database/userInfo.txt', 'r')
            userInfo = file.readlines()
            file.close()

            usernames = []
            passwords = []

            for i in range(0, len(userInfo)):
                info = userInfo[i].split()
                currentUsername = info[0]
                currentPassword = info[1]
                usernames.append(currentUsername)
                passwords.append(currentPassword)

            # Search for the old password
            correctPassword = False
            for i in range(0, len(userInfo)):
                if loggedUser[0] == usernames[i]:
                    if oldPassword == passwords[i]:
                        correctPassword = True
                        break

            # Check the requirements
            if not correctPassword:
                tk.messagebox.showerror(title="Error", message="Incorrect Password!")
            elif newPassword != newPasswordAgain:
                tk.messagebox.showwarning(title="Warning", message="Passwords are not the same!")
            elif len(newPassword) < 6:
                tk.messagebox.showwarning(title="Warning", message="Password should be at least 6 characters!")
            elif ' ' in newPassword:
                tk.messagebox.showwarning(title="Warning", message="Password cannot contain white space!")
            elif oldPassword == newPassword:
                tk.messagebox.showwarning(title="Warning", message="New password cannot be the same as old password!")
            else:
                # Change the password if all requirements are satisfied
                for i in range(0, len(userInfo)):
                    if loggedUser[0] == usernames[i]:
                        with open(r'database/userInfo.txt', 'r') as file:
                            data = file.readlines()
                            data[i] = data[i].replace(oldPassword, newPassword)

                        with open(r'database/userInfo.txt', 'w') as file:
                            file.write("")

                        for j in range(0, len(data)):
                            with open(r'database/userInfo.txt', 'a') as file:
                                file.write(data[j])
                        break

                tk.messagebox.showinfo(title="Info", message="Password Changed Successfully!")
                self.show_frame(SettingsPage)

        # Function for delete account operation
        def delete_account(self):
            answer = tk.messagebox.askquestion(title="Form", message="Are you sure you want to delete your account?")

            if answer == "yes":
                username = loggedUser[0]

                # Get the data
                file1 = open('database/userInfo.txt', 'r')
                userInfo = file1.readlines()
                file1.close()

                usernames = []
                passwords = []

                for i in range(0, len(userInfo)):
                    info = userInfo[i].split()
                    currentUsername = info[0]
                    currentPassword = info[1]
                    usernames.append(currentUsername)
                    passwords.append(currentPassword)

                # Search for the username
                index = -1
                for i in range(0, len(userInfo)):
                    if username == usernames[i]:
                        index = i

                # Delete the account files
                os.remove("database/bookAuthors_" + username + ".txt")
                os.remove("database/bookPages_" + username + ".txt")
                os.remove("database/bookNames_" + username + ".txt")
                os.remove("database/bookLocations_" + username + ".txt")

                file2 = open('database/userInfo.txt', "w")
                file2.write("")

                userInfo.pop(index)

                if index == len(userInfo):
                    userInfo[index - 1] = userInfo[index - 1][:-1]

                for i in range(0, len(userInfo)):
                    file2.write(userInfo[i])

                tk.messagebox.showinfo(title="Info", message="Account Deleted Successfully!")
                self.show_frame(LoginPage)

    # Frame - Login Page
    class LoginPage(tk.Frame):
        # Constructor
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent, bg=background)

            # Button Fonts
            buttonFont1 = font.Font(size=18)
            buttonFont2 = font.Font(size=14)

            # Heading
            label = tk.Label(self, text="Welcome to", font=mediumFont, bg=background, fg=foreground)
            label.grid(row=0, column=4, padx=10, pady=10)
            label.place(x=444, y=105, anchor="center")
            label1 = tk.Label(self, text="Virtual Library", font=largeFont, bg=background, fg=foreground)
            label1.grid(row=0, column=4, padx=10, pady=10)
            label1.place(x=444, y=165, anchor="center")

            # User Image
            userImg = ImageTk.PhotoImage(Image.open("images/username.png"))
            label2 = tk.Label(self, image=userImg, bg=background)
            label2.image = userImg
            label2.place(x=294, y=246, anchor="center")

            # Username Entry
            usernameEntry = tk.Entry(self, fg=background, bg=foreground, width=15, font='Verdana 20')
            usernameEntry.place(x=444, y=246, anchor="center")

            # Password Image
            passwordImg = ImageTk.PhotoImage(Image.open("images/password.png"))
            label3 = tk.Label(self, image=passwordImg, bg=background)
            label3.image = passwordImg
            label3.place(x=295, y=299, anchor="center")

            # Password Entry
            passwordEntry = tk.Entry(self, fg=background, bg=foreground, width=15, font='Verdana 20', show="•")
            passwordEntry.place(x=444, y=300, anchor="center")

            # Sign In Button
            signInButton = tk.Button(self, text="Sign In",
                                     command=lambda: [controller.sign_in(usernameEntry.get(), passwordEntry.get()),
                                                      usernameEntry.delete(0, "end"), passwordEntry.delete(0, "end")],
                                     bg=buttonBackground, fg=foreground, height=1, width=10, cursor="hand2")
            signInButton['font'] = buttonFont1
            signInButton.place(x=444, y=365, anchor="center")

            # Sign Up Button
            signUpButton = tk.Button(self, text="Sign Up",
                                     command=lambda: controller.show_frame(SignUpPage), bg=buttonBackground,
                                     fg=foreground, height=1, width=10, cursor="hand2")
            signUpButton['font'] = buttonFont2
            signUpButton.place(x=446, y=430, anchor="center")

            # Forgot Password Link
            label4 = tk.Label(self, text="Forgot Password?", cursor="hand2",
                              fg=foreground, bg=background, font="Verdana 11 underline")
            label4.place(x=444, y=475, anchor="center")
            label4.bind("<Button-1>", lambda e: controller.show_frame(ForgotPasswordPage))

    class SignUpPage(tk.Frame):
        # Constructor
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent, bg=background)

            # Button Fonts
            buttonFont1 = font.Font(size=18)
            buttonFont2 = font.Font(size=14)

            # Heading
            label = tk.Label(self, text="Sign Up Now!", font=largeFont, bg=background, fg=foreground)
            label.grid(row=0, column=4, padx=10, pady=10)
            label.place(x=444, y=130, anchor="center")

            # User Image
            userImg = ImageTk.PhotoImage(Image.open("images/username.png"))
            label2 = tk.Label(self, image=userImg, bg=background)
            label2.image = userImg
            label2.place(x=294, y=200, anchor="center")

            # Username Entry
            usernameEntry = tk.Entry(self, fg=background, bg=foreground, width=15, font='Verdana 20')
            usernameEntry.place(x=444, y=200, anchor="center")

            # Password Image
            passwordImg = ImageTk.PhotoImage(Image.open("images/password.png"))
            label3 = tk.Label(self, image=passwordImg, bg=background)
            label3.image = passwordImg
            label3.place(x=295, y=254, anchor="center")

            # Password Entry
            passwordEntry1 = tk.Entry(self, fg=background, bg=foreground, width=15, font='Verdana 20', show="•")
            passwordEntry1.place(x=444, y=255, anchor="center")

            # Password Image
            passwordImg2 = ImageTk.PhotoImage(Image.open("images/password.png"))
            label4 = tk.Label(self, image=passwordImg2, bg=background)
            label4.image = passwordImg2
            label4.place(x=295, y=309, anchor="center")

            # Password Entry
            passwordEntry2 = tk.Entry(self, fg=background, bg=foreground, width=15, font='Verdana 20', show="•")
            passwordEntry2.place(x=444, y=310, anchor="center")

            # Hint Image
            hintImg = ImageTk.PhotoImage(Image.open("images/hint.png"))
            label5 = tk.Label(self, image=hintImg, bg=background)
            label5.image = hintImg
            label5.place(x=294, y=365, anchor="center")

            # Hint Entry
            hintEntry = tk.Entry(self, fg=background, bg=foreground, width=15, font='Verdana 20')
            hintEntry.place(x=444, y=365, anchor="center")
            hintEntry.insert(0, "Hint")

            # Sign Up Button
            signUpButton = tk.Button(self, text="Sign Up",
                                command=lambda: [controller.sign_up(usernameEntry.get(), passwordEntry1.get(),
                                                                   passwordEntry2.get(), hintEntry.get()),
                                                 usernameEntry.delete(0, "end"), passwordEntry1.delete(0, "end"),
                                                 passwordEntry2.delete(0, "end"), hintEntry.delete(0, "end"),
                                                 hintEntry.insert(0, "Hint")],
                                bg=buttonBackground, fg=foreground, height=1, width=10,
                                cursor="hand2", font=buttonFont1)
            signUpButton.place(x=444, y=425, anchor="center")

            #  Back Button
            backButton = tk.Button(self, text="◄ ",
                                     command=lambda: controller.show_frame(LoginPage),
                                     bg=buttonBackground, fg=foreground, height=1, width=4,
                                     cursor="hand2", font=buttonFont2)
            backButton.place(x=10, y=10)

    class ForgotPasswordPage(tk.Frame):
        # Constructor
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent, bg=background)

            # Button Fonts
            buttonFont1 = font.Font(size=18)
            buttonFont2 = font.Font(size=14)

            # Heading
            label = tk.Label(self, text="Please enter your username:" , font=largeFont, bg=background, fg=foreground)
            label.grid(row=0, column=4, padx=10, pady=10)
            label.place(x=444, y=200, anchor="center")

            # Username Image
            userImg = ImageTk.PhotoImage(Image.open("images/username.png"))
            label2 = tk.Label(self, image=userImg, bg=background)
            label2.image = userImg
            label2.place(x=294, y=285, anchor="center")

            # Username Entry
            usernameEntry = tk.Entry(self, fg=background, bg=foreground, width=15, font='Verdana 20')
            usernameEntry.place(x=444, y=285, anchor="center")

            # Get Hint Button
            getHintButton = tk.Button(self, text="Get Hint",
                                     command=lambda: [controller.get_hint(usernameEntry.get()),
                                                      usernameEntry.delete(0, "end")],
                                     bg=buttonBackground, fg=foreground, height=1, width=10,
                                     cursor="hand2", font=buttonFont1)
            getHintButton.place(x=444, y=365, anchor="center")

            # Back Button
            backButton = tk.Button(self, text="◄ ",
                                   command=lambda: controller.show_frame(LoginPage),
                                   bg=buttonBackground, fg=foreground, height=1, width=4,
                                   cursor="hand2", font=buttonFont2)
            backButton.place(x=10, y=10)

    class MainPage(tk.Frame):
        # Constructor
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent, bg=background)

            # Button Font
            buttonFont1 = font.Font(size=18)

            # Heading
            label = tk.Label(self, text="Main Menu", font=largeFont, bg=background, fg=foreground)
            label.place(x=444, y=140, anchor="center")

            # Search Button
            searchButton = tk.Button(self, text="Search a Book",
                                     command=lambda: controller.show_frame(SearchPage),
                                     bg=buttonBackground, fg=foreground, height=1, width=12, cursor="hand2")
            searchButton['font'] = buttonFont1
            searchButton.place(x=444, y=215, anchor="center")

            # Add Book Button
            addButton = tk.Button(self, text="Add a Book",
                                     command=lambda: controller.show_frame(AddPage),
                                     bg=buttonBackground, fg=foreground, height=1, width=12, cursor="hand2")
            addButton['font'] = buttonFont1
            addButton.place(x=444, y=275, anchor="center")

            # Remove Book Button
            removeButton = tk.Button(self, text="Remove a Book",
                                  command=lambda: controller.show_frame(RemovePage),
                                  bg=buttonBackground, fg=foreground, height=1, width=12, cursor="hand2")
            removeButton['font'] = buttonFont1
            removeButton.place(x=444, y=335, anchor="center")

            # Settings Button
            settingsButton = tk.Button(self, text="Settings",
                                  command=lambda: controller.show_frame(SettingsPage),
                                  bg=buttonBackground, fg=foreground, height=1, width=12, cursor="hand2")
            settingsButton['font'] = buttonFont1
            settingsButton.place(x=444, y=395, anchor="center")

            # Log Out Button
            logOutButton = tk.Button(self, text="Log Out",
                                       command=lambda: controller.log_out(),
                                       bg=buttonBackground, fg=foreground, height=1, width=12, cursor="hand2")
            logOutButton['font'] = buttonFont1
            logOutButton.place(x=444, y=455, anchor="center")

    class SearchPage(tk.Frame):
        # Constructor
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent, bg=background)

            # Button Fonts
            buttonFont1 = font.Font(size=18)
            buttonFont2 = font.Font(size=14)

            # Heading
            label = tk.Label(self, text="Search a book by name:", font=largeFont, bg=background, fg=foreground)
            label.place(x=444, y=200, anchor="center")

            # Book Image
            bookImg = ImageTk.PhotoImage(Image.open("images/book.png"))
            label2 = tk.Label(self, image=bookImg, bg=background)
            label2.image = bookImg
            label2.place(x=205, y=286, anchor="center")

            # Book Name Entry
            bookEntry = tk.Entry(self, fg=background, bg=foreground, width=25, font='Verdana 20')
            bookEntry.place(x=444, y=285, anchor="center")

            # Search Button
            searchButton = tk.Button(self, text="Search",
                                      command=lambda: [controller.search(bookEntry.get()), bookEntry.delete(0, "end")],
                                      bg=buttonBackground, fg=foreground, height=1, width=10,
                                      cursor="hand2", font=buttonFont1)
            searchButton.place(x=444, y=360, anchor="center")

            # Back Button
            backButton = tk.Button(self, text="◄ ",
                                   command=lambda: controller.show_frame(MainPage),
                                   bg=buttonBackground, fg=foreground, height=1, width=4,
                                   cursor="hand2", font=buttonFont2)
            backButton.place(x=10, y=10)

    class AddPage(tk.Frame):
        # Constructor
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent, bg=background)

            # Button Fonts
            buttonFont1 = font.Font(size=18)
            buttonFont2 = font.Font(size=14)

            # Heading
            label = tk.Label(self, text="Please enter the book information:", font=largeFont,
                             bg=background, fg=foreground)
            label.grid(row=0, column=4, padx=10, pady=10)
            label.place(x=444, y=130, anchor="center")

            # Book Image
            bookImg = ImageTk.PhotoImage(Image.open("images/book.png"))
            label2 = tk.Label(self, image=bookImg, bg=background)
            label2.image = bookImg
            label2.place(x=294, y=201, anchor="center")

            # Book Name Entry
            nameEntry = tk.Entry(self, fg=background, bg=foreground, width=15, font='Verdana 20')
            nameEntry.place(x=444, y=200, anchor="center")

            # Author Image
            authorImg = ImageTk.PhotoImage(Image.open("images/author.png"))
            label3 = tk.Label(self, image=authorImg, bg=background)
            label3.image = authorImg
            label3.place(x=295, y=254, anchor="center")

            # Author Entry
            authorEntry = tk.Entry(self, fg=background, bg=foreground, width=15, font='Verdana 20')
            authorEntry.place(x=444, y=255, anchor="center")

            # Number of Pages Image
            pagesImg = ImageTk.PhotoImage(Image.open("images/pages.png"))
            label4 = tk.Label(self, image=pagesImg, bg=background)
            label4.image = pagesImg
            label4.place(x=295, y=309, anchor="center")

            # Number of Pages Entry
            pagesEntry = tk.Entry(self, fg=background, bg=foreground, width=15, font='Verdana 20')
            pagesEntry.place(x=444, y=310, anchor="center")

            # Location Image
            locationImg = ImageTk.PhotoImage(Image.open("images/location.png"))
            label5 = tk.Label(self, image=locationImg, bg=background)
            label5.image = locationImg
            label5.place(x=294, y=365, anchor="center")

            # Location Entry
            locationEntry = tk.Entry(self, fg=background, bg=foreground, width=15, font='Verdana 20')
            locationEntry.place(x=444, y=365, anchor="center")

            # Add Book Button
            addButton = tk.Button(self, text="Add",
                                     command=lambda: [controller.add(nameEntry.get(), authorEntry.get(),
                                                                    pagesEntry.get(), locationEntry.get()),
                                                      nameEntry.delete(0, "end"), authorEntry.delete(0, "end"),
                                                      pagesEntry.delete(0, "end"), locationEntry.delete(0, "end")],
                                     bg=buttonBackground, fg=foreground, height=1, width=10,
                                     cursor="hand2", font=buttonFont1)
            addButton.place(x=444, y=425, anchor="center")

            # Back Button
            backButton = tk.Button(self, text="◄ ",
                                   command=lambda: controller.show_frame(MainPage),
                                   bg=buttonBackground, fg=foreground, height=1, width=4,
                                   cursor="hand2", font=buttonFont2)
            backButton.place(x=10, y=10)

    class RemovePage(tk.Frame):
        # Constructor
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent, bg=background)

            # Button Fonts
            buttonFont1 = font.Font(size=18)
            buttonFont2 = font.Font(size=14)

            # Heading
            label = tk.Label(self, text="Please enter the name of", font=largeFont, bg=background, fg=foreground)
            label.place(x=444, y=135, anchor="center")
            label1 = tk.Label(self, text="the book you want to remove:", font=largeFont, bg=background, fg=foreground)
            label1.place(x=444, y=200, anchor="center")

            # Book Image
            bookImg = ImageTk.PhotoImage(Image.open("images/book.png"))
            label2 = tk.Label(self, image=bookImg, bg=background)
            label2.image = bookImg
            label2.place(x=205, y=286, anchor="center")

            # Book Name Entry
            bookEntry = tk.Entry(self, fg=background, bg=foreground, width=25, font='Verdana 20')
            bookEntry.place(x=444, y=285, anchor="center")

            # Search Button
            searchButton = tk.Button(self, text="Remove",
                                     command=lambda: [controller.remove(bookEntry.get()), bookEntry.delete(0, "end")],
                                     bg=buttonBackground, fg=foreground, height=1, width=10,
                                     cursor="hand2", font=buttonFont1)
            searchButton.place(x=444, y=360, anchor="center")

            # Back Button
            backButton = tk.Button(self, text="◄ ",
                                   command=lambda: controller.show_frame(MainPage),
                                   bg=buttonBackground, fg=foreground, height=1, width=4,
                                   cursor="hand2", font=buttonFont2)
            backButton.place(x=10, y=10)

    class SettingsPage(tk.Frame):
        # Constructors
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent, bg=background)

            # Button Fonts
            buttonFont1 = font.Font(size=18)
            buttonFont2 = font.Font(size=14)

            # Heading
            label = tk.Label(self, text="Settings", font=largeFont, bg=background, fg=foreground)
            label.place(x=444, y=190, anchor="center")

            # Change Password Button
            changePasswordButton = tk.Button(self, text="Change Password",
                                     command=lambda: controller.show_frame(ChangePasswordPage),
                                     bg=buttonBackground, fg=foreground, height=1, width=14, cursor="hand2")
            changePasswordButton['font'] = buttonFont1
            changePasswordButton.place(x=444, y=265, anchor="center")

            # Delete Account Button
            deleteAccountButton = tk.Button(self, text="Delete Account",
                                  command=lambda: controller.delete_account(),
                                  bg=buttonBackground, fg=foreground, height=1, width=14, cursor="hand2")
            deleteAccountButton['font'] = buttonFont1
            deleteAccountButton.place(x=444, y=330, anchor="center")

            # Back Button
            backButton = tk.Button(self, text="◄ ",
                                   command=lambda: controller.show_frame(MainPage),
                                   bg=buttonBackground, fg=foreground, height=1, width=4,
                                   cursor="hand2", font=buttonFont2)
            backButton.place(x=10, y=10)

    class ChangePasswordPage(tk.Frame):
        # Constructor
        def __init__(self, parent, controller):
            tk.Frame.__init__(self, parent, bg=background)

            # Button Fonts
            buttonFont1 = font.Font(size=18)
            buttonFont2 = font.Font(size=14)

            # Heading
            label = tk.Label(self, text="Please enter your password", font=largeFont, bg=background, fg=foreground)
            label.place(x=444, y=125, anchor="center")
            label2 = tk.Label(self, text=" and new password (twice):", font=largeFont, bg=background, fg=foreground)
            label2.place(x=444, y=185, anchor="center")

            # Password Image
            passwordImg = ImageTk.PhotoImage(Image.open("images/password.png"))
            label3 = tk.Label(self, image=passwordImg, bg=background)
            label3.image = passwordImg
            label3.place(x=295, y=254, anchor="center")

            # Password Entry
            passwordEntry1 = tk.Entry(self, fg=background, bg=foreground, width=15, font='Verdana 20', show="•")
            passwordEntry1.place(x=444, y=255, anchor="center")

            # New Password Image
            passwordImg2 = ImageTk.PhotoImage(Image.open("images/resetPassword.png"))
            label4 = tk.Label(self, image=passwordImg2, bg=background)
            label4.image = passwordImg2
            label4.place(x=295, y=311, anchor="center")

            # New Password Entry
            passwordEntry2 = tk.Entry(self, fg=background, bg=foreground, width=15, font='Verdana 20', show="•")
            passwordEntry2.place(x=444, y=310, anchor="center")

            # New Password Image
            passwordImg3 = ImageTk.PhotoImage(Image.open("images/resetPassword.png"))
            label5 = tk.Label(self, image=passwordImg3, bg=background)
            label5.image = passwordImg3
            label5.place(x=295, y=366, anchor="center")

            # New Password Entry
            passwordEntry3 = tk.Entry(self, fg=background, bg=foreground, width=15, font='Verdana 20', show="•")
            passwordEntry3.place(x=444, y=365, anchor="center")

            # Change Password Button
            changePasswordButton = tk.Button(self, text="Change Password",
                                     command=lambda: [controller.change_password(passwordEntry1.get(),
                                                      passwordEntry2.get(), passwordEntry3.get()),
                                                      passwordEntry1.delete(0, "end"), passwordEntry2.delete(0, "end"),
                                                      passwordEntry3.delete(0, "end")],
                                     bg=buttonBackground, fg=foreground, height=1, width=14, cursor="hand2")
            changePasswordButton['font'] = buttonFont1
            changePasswordButton.place(x=444, y=435, anchor="center")

            # Back Button
            backButton = tk.Button(self, text="◄ ",
                                   command=lambda: controller.show_frame(SettingsPage),
                                   bg=buttonBackground, fg=foreground, height=1, width=4,
                                   cursor="hand2", font=buttonFont2)
            backButton.place(x=10, y=10)

    # Driver Code
    app = TkinterApp()
    app.geometry("900x600")
    app.title("Virtual Library")
    app.minsize(900, 600)
    app.maxsize(900, 600)
    app.mainloop()
