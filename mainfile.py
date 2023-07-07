
from tkinter import *
from mysql.connector import *

def login():
    print("Start Logs:")
    mainwindow = Tk()
    mainwindow.title("Login Page")
    label = Label(mainwindow, text = "MySQL GUI using Python").grid(row = 0, column = 0, columnspan = 2)

    userlabel = Label(mainwindow, text = "Enter MySQL UserName: ").grid(row = 1, column = 0)
    username = Entry(mainwindow)
    username.grid(row = 1, column = 1)
    passlabel = Label(mainwindow, text = "Enter MySQL Password: ").grid(row = 2, column = 0)
    password = Entry(mainwindow)

    password.grid(row = 2, column = 1)
    def get_details():
        name = str(username.get())
        pswd = str(password.get())
        print("UserName = ",name," ","Password = ",pswd," Received")
        print("Authenticating with MySQL")
        conn = connect(host = "localhost", user = name, password = pswd)
        if conn.is_connected():
            print("Login Successful. Launching DataBase selector.")
            mainwindow.destroy()
            import homepage
            homepage.home(name,pswd)
                 
    button = Button(mainwindow, text = "login", command = get_details).grid(row = 3, column = 0, columnspan = 2)
    mainwindow.mainloop()

if __name__ == "__main__": 
    login() 








