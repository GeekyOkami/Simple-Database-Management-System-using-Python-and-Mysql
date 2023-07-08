from tkinter import *
import mysql.connector
#Creating a list of available data types in MySQL to be used later
datatype_options = ["smallint",
                    "bigint",
                    "int",
                    "decimal",     
                    "numeric",
                    "tinytext",
                    "mediumtext",
                    "longtext",
                    "text",
                    "date",
                    "time"]

#This function returns a list of databases available to the current user.
def database_list(name,pswd): 
    conn = mysql.connector.connect(host = "localhost", user = name, password = pswd)
    cursh = conn.cursor()
    cursh.execute("show databases")
    list1 = list(cursh)
    for i in range(len(list1)):
        list1.append(list1[0][0])
        list1.pop(0)
    return list1

#This home function will act as a window to select a database to work on
def home(name, pswd):
    window1 = Tk()#creating window
    window1.title("Select Database")
    
    #creating cursor for a program to use
    conn = mysql.connector.connect(host = "localhost", user = name, password = pswd)
    cursh = conn.cursor()

    label1 = Label(window1, text = "Enter Database to Access from the given list: ").grid(column = 0, row = 0)

    #This section is used to generate a Drop Down Menu
    #using the database_list() function
    database = StringVar()
    database.set("")
    options = database_list(name, pswd)
    database1 = OptionMenu(window1, database, *options)
    database1.grid(row = 0, column = 1)

    #This function will open the new window with options to
    #work on the database
    def access_database():
        x = database.get()
        if x == "":
            print("Please choose a Database from the Drop Down Menu.")
            label__ = Label(window1, text = "Error: Please Select a Database from the Drop Down Menu.").grid(row = 8, columnspan = 2)
        else:
            print("Database Name Recieved: ", x)
            window1.destroy()
            home2(name,pswd,x)
    #Button to trigger access_database()
    mybutton = Button(window1, text = "Access Database", command = access_database)
    mybutton.grid(row = 1, column = 0)
    
    #This fucntion will open a new window to create a database
    def create_database():
        print("Accepting Name for New database.")
        window1.destroy()
        window2 = Tk()
        window2.title("Create Database")

        #Asking for an alphanumeric name to the database.
        label1 = Label(window2, text = "Enter New Database Name(Only Alphanumeric characters): ")
        label1.grid(row = 0, column = 0)
        database1 = Entry(window2)
        database1.grid(row = 0,column = 1)

        #This function will check whether the name can be a valid database
        #then creates the database and opens it immediately
        def create():
            x = str(database1.get())

            #Creating a tkinter variable to display text in case of inavlid name
            f = StringVar()
            f.set("")
            label7 = Label(window2, textvariable = f).grid(row = 2, columnspan = 2)
            print("Database Name Recieved: ", x)
            
            if x.isalnum():
                if x not in options:
                    print("Alphanumeric character check complete.")
                    cursh.execute("Create database " + x)
                    print("Database Created.")
                    window2.destroy()
                    home2(name, pswd, x)
                    
                else:
                    print("Database already exists.")
                    f.set("Database already exists. Please choose another name.")                   
                
            else:
                print("Inavild Database Name. Try again.")
                f.set("Only Alphanumeric characters allowed!")
        #Button to triger the create() function        
        mybutton = Button(window2, text = "Create", command = create).grid(row = 1,column = 0)

        #This fucntion brings up the login screen again
        #if the user needs to exit
        def logout():
            print("Logging out.")
            print()
            window2.destroy()
            import mainfile
            mainfile.login()
        button3 = Button(window2, text = "Logout", command = logout).grid(row = 2, column = 1)

        def cancel():
            print("Creating Database Cancelled.")
            print()
            window2.destroy()
            home(name, pswd)
        button3 = Button(window2, text = "Cancel", command = cancel).grid(row = 7, column = 0)
        window2.mainloop()
    
    #Button to trigger the Create_database() and open a window
    newbutton1 = Button(window1, text = "Create New Database", command = create_database)
    newbutton1.grid(row = 2, column = 0)


    #This function will open a new window to delete any pre-existing database
    #after deletion, it will open the Database Selection window. See home() function
    def del_database():
        print("Accepting Name for deleting database.")
        window1.destroy()
        window2 = Tk()
        window2.title("Delete Database")
        label1 = Label(window2, text = "Enter Database Name(Only Alphanumeric characters): ").grid(row = 0, column = 0)

        #Creating a Drop Down Menu for deleting a database
        database1 = StringVar()
        database1.set("")
        database = OptionMenu(window2, database1, *options).grid(row = 0, column = 1)
        
        def delete():
            x = str(database1.get())
            print("Database Name Recieved: ", x)
            
            conn = mysql.connector.connect(host = "localhost", user = name, password = pswd)
            cursh = conn.cursor()
            cursh.execute("Drop database " + x)
            print("Database Deleted.")
            window2.destroy()
            home(name, pswd)
            
        #Button to trigger delete fucntion
        mybutton = Button(window2, text = "Delete", command = delete).grid(row = 1,column = 0, columnspan = 2)
        
        def logout():
            print("Logging out.")
            print()
            window2.destroy()
            import mainfile
            mainfile.login()
        def cancel():
            print("Deleting Table Cancelled.")
            print()
            window2.destroy()
            home(name, pswd)
        button3 = Button(window2, text = "Cancel", command = cancel).grid(row = 7, columnspan = 2)
        button3 = Button(window2, text = "Logout", command = logout).grid(row = 7, sticky = E)
        window2.mainloop()

    #button to trigger del_database fucntion and open the deletion window
    newbutton2 = Button(window1, text = "Delete Database", command = del_database)
    newbutton2.grid(row = 2, column = 1)

    
    #This line displays the current user.    
    label4 = Label(window1, text = ("Login as "+name+" with password "+pswd)).grid(row = 5)
    
    def logout():
            print("Logging out.")
            print()
            window1.destroy()
            import mainfile
            mainfile.login()
    button3 = Button(window1, text = "Logout", command = logout).grid(row = 7, columnspan = 2)
    window1.mainloop()
    
    


#This fucntions maintains the real work area for each database.
def home2(name, pswd, datb):
    print("Using Database: ", datb)
    window = Tk()
    window.title("Database Selected: "+datb)
    

    conn = mysql.connector.connect(host = "localhost", user = name, password = pswd, database = datb)
    cursh = conn.cursor()
    cursh.execute("show tables")
    table_list = []
    for i in list(cursh):
        table_list.append(i[0])

    #Heading displays the current database being worked on
    heading = Label(window, text = "Using Database: "+datb).grid(row = 0, column = 0)

    #This chng() functions opena Database Selector to change the current database, if needed
    def chng():
        window.destroy()
        print("Launching Database Selector")
        home(name, pswd)
    #Button to trigger the chng() function
    change = Button(window, text = "Change", command = chng).grid(row = 0, column = 1)

    #These statements describes the instructions.
    heading = Label(window, text = "You can perfom any one of the following operations at a time.")
    heading.grid(pady = 5, row = 1, columnspan = 2)
    heading2 = Label(window, text = "Results will appear on the Python interpreter.")
    heading2.grid(pady = 10, row = 2, columnspan = 2)

    #This will create a window which will ask the no of Fields in the Table
    def create_table():
        print("You selected to create a table.")
        window.destroy()
        window1 = Tk()
        window1.title("Create Table")
        label1 = Label(window1, text = "Enter the no. of fields in the Table: ")
        label1.grid(row = 0, column = 0)
        col = Entry(window1)
        col.grid(row = 0, column = 1)
            
            

        #Checking if the entry is numerical 
        def check_input():
            if col.get().isdigit():
                col_count()
            else:
                print("No of Fields must be a number.")
                label_ = Label(window1, text = "No of Fields must be a number.").grid(row = 2, columnspan = 2)

                
        #This is the Table Creator window
        #This provides a much user friendly UI to desgin the table
        #In this new window, it is intended to create as many Entry varaiables
        #as there are no. of fields required. So, exec() method is used to
        #generate varaiables by first generation a dictionart of size = cols
        def col_count():
            global move
            move = False
            
            var_dict = {}#For all the Entry Boxes              
            var_dict2 = {}#For all the Fiels Names 
            
            #Displaying some info and asking for the name of the table
            count = int(col.get())
            print("No of Fields in the table: ", count)
            window1.destroy()
            window2 = Tk()
            window2.title("Create Table")
            heading = Label(window2, text = "Creating Table in Database: "+datb).grid(columnspan = 2)
            label1 = Label(window2, text = "Enter Name of Table: ").grid(row = 1, column = 0)
            table_name = Entry(window2)
            table_name.grid(row = 1,column = 2)
            
            
            

            
            #This piece of code creates as many variables as required to store the table data
            for r in range(count):
                var_dict["a"+str(r)+"0"] = "Entry(window2)"
                var_dict["a"+str(r)+"1"] = "OptionMenu(window2, datatype"+str(r)+", *datatype_options)"
                var_dict["a"+str(r)+"2"] = "Entry(window2)"

                var_dict2["b"+str(r)] = "Label(window2, text ='Field"+str(r+1)+"').grid(row = "+str(r+3)+", column = 0)"
                
                exec("datatype"+str(r)+" = StringVar()")


            
            for k,v in var_dict2.items():
                exec("%s=%s"%(k,v))
        
            #Referenced exec example from www.stackoverflow.com
            for k,v in var_dict.items():
                exec("%s=%s"%(k,v))
                
            for r in range(count):
                for j in range(3):
                   exec("a"+str(r)+str(j)+".grid(row = "+str(r+3)+",column = "+str(j+1)+")")
            #Sending over the dictionary of locals variables so that exec command can use them in the next section
            entry_var = locals()
           

           
            
           
            #This function contains code that will validate the inputs by the user
            #Creates the table if all conditions are met
            def create_comm(entry_variables):
                Error = []
                print()
                print()
                name1 = table_name.get()
                print("Name of Table Recieved: ", name1)
                    
                #These list will store all the table details
                fields = []
                datatype_list = []
                datatype_info_list = []

                #This code will fetch all the details when the button is clicked
                #and append them to the list
                for r in range(count):
                    fields.append(eval("a"+str(r)+"0.get()", entry_variables))
                    datatype_list.append(eval("datatype"+str(r)+".get()", entry_variables))
                    datatype_info_list.append(eval("a"+str(r)+"2.get()", entry_variables))
                        

                #This function is proegrammed to check whether the input length for mentioned datatypes is correct
                def check_numeric(index, limit, name):#can be used for numeric and decimal
                    if datatype_info_list[index] != "":
                        if datatype_info_list[index][0] == "(" and datatype_info_list[index][-1] == ")":
                            input_ = list(datatype_info_list[index][1:-1].split(","))
                            if len(input_) == 2:
                                if int(input_[0]) < limit and int(input_[0]) > int(input_[1]) + 1:
                                    return (True, '' )
                                else:
                                    return (False, "Enter an integer value between 1 and "+str(limit - 1)+" for "+str(name)+" Datatype. (Field "+str(index+1)+")")
                                
                            else:
                                return (False, "Only 2 numerical values required in the tuple. (Field "+str(index+1)+")")
                        else:
                            return (False, "Use Brackets with the Syntax of "+str(name)+" Data Type. (Field "+str(index+1)+")")
                    else:
                        return (False, "Please enter data to support "+str(name)+" datatype. (Field "+str(index+1)+")")

               #Checking whether all the Field Names are alphanumeric 
                for i in fields:
                    index = 0
                    if i.isalnum() and not i.isdigit():
                        pass
                    else:
                        Error.append("Field Names can only be alphanumeric. (Field"+str(index+1)+")")
                    index += 1
                    count_ = 0
                    for j in fields:
                        if i == j:
                            count_ += 1
                    if count_ > 1:
                        Error.append("Duplicate Field Names cannot exist in same Table. Duplicate Name: "+i)
                        break
                        
                
                    
                #This list will contain whether the input for each datatype is correct or not
                #in the form of tuples containing either True or False
                correct_data = []
                for i in range(count):
                    if datatype_list[i] == "":
                        #This list will contain all the Errors made by user in his input
                        Error = []
                        Error.append("Every column must have a datatype.")
                        break
                    else:
                        if datatype_list[i] == "numeric":
                            correct_data.append(check_numeric(i, 19, "Numeric"))
                        elif datatype_list[i] == "decimal":
                            correct_data.append(check_numeric(i, 20, "Decimal"))
                        else:
                            correct_data.append((True, ""))
                        if correct_data[-1][0] == False:
                            Error.append(correct_data[-1][1])

                #This conditions will give check the table name and create the table
                #only if the Error list is empty
                if name1.isalnum() and not name1.isdigit():
                    if name1 in table_list:
                        Error.insert(0, "Table with the Name "+name1+" already exists. Please choose another name.")
                    else:
                        if Error == []:
                            #Create the table in MySql
                            print("All parameters checked. Expecting no errors.")
                            sql_statement = "create table " + name1 + "("
                            for i in range(count):
                                sql_statement += fields[i] + " " + datatype_list[i]
                                if datatype_list[i] in ("numeric", "decimal"):
                                    sql_statement += datatype_info_list[i]
                                else:
                                    pass
                                if  i == count-1:
                                    sql_statement += ")"
                                else:
                                    sql_statement += ", "
                            conn = mysql.connector.connect(host = "localhost", user = name, password = pswd, database = datb)
                            cursor_ = conn.cursor()
                            cursor_.execute(sql_statement)
                            window2.destroy()
                            home2(name, pswd, datb)
                else:
                    Error.insert(0, "Name of the Table must be alphanumeric.")
                if Error != []:
                    error_label = Label(window2, text = "Please check the Errors being mentioned in the Interpretor.")
                    error_label.grid(row = count+11, columnspan = 4)
                    
                    print("Please Check these detected Errors.")
                    for i in Error:
                        print(str(Error.index(i)+1)+"-->"+i)
                        
            #Button to trigger the create_com function which fetches all the data and creates the table
            Comm = Button(window2, text = "Create", command = lambda:create_comm(entry_var))
            Comm.grid(row = count+3, columnspan = 2)

            #Button to go back to main menu if no table is to be created
            def cancel():
                print("Deleting Table Cancelled.")
                print()
                window2.destroy()
                home2(name, pswd, datb)
            button3 = Button(window2, text = "Cancel", command = cancel).grid(row = count+3, columnspan = 2, column = 2)

            #These label give heading to the various inputs
            field = Label(window2, text = "Field Name").grid(row = 2, column = 1)
            data_type_label = Label(window2, text = "Data type").grid(row = 2, column = 2)
            data_input_label = Label(window2, text ="Input for Data Type if neccesary").grid(row = 2 ,column = 3)
            

            #These Labels print out the guidelines to the window
            help1 = Label(window2, text = "Refer to the guidelines for entering any data:")
            help1.grid(row = count+4, columnspan = 4)
            help2 = Label(window2, text = "1. Table Name and Field Names must be alphanumeric.")
            help2.grid(row = count+5, columnspan = 4)
            help5 = Label(window2, text = "2. Only Numeric and Decimal require extra input in the form of '(Total Length,Precision)'.")
            help5.grid(row = count+8, columnspan = 4)
            help3 = Label(window2, text = "3.There should be no spaces in the input '(Total_length,Precision). Eg: (8,4)'")
            help3.grid(row = count+9, columnspan = 4)
            help6 = Label(window2, text = "4. Input for Numeric and Decimal data type must be in the form: (Total_length,Precision) eg: (8,2)")
            help6.grid(row = count+10, columnspan = 4)
            
            
            window2.mainloop()
        #This button wil start the function the check the no of fields in the table
        create = Button(window1, text = "Create Table", command = check_input).grid(row = 1)
        #Button to go back to main menu
        def cancel():
            print("Creating Table Cancelled.")
            print()
            window1.destroy()
            home2(name, pswd, datb)
        cancel = Button(window1, text= "Cancel", command = cancel).grid(row = 1, column = 1)
    #This function wil check if there are any table in the database
    #if there are no tables, it will put an message on the screen
    def check_delete():
            if table_list == []:
                print("There are no tables to delete in the database.")
                error = Label(window, text = "   There are no tables to delete in the database.   ")
                error.grid(row = 13, columnspan = 2)
            else:
                delete_table()

    #After checking for the table,
    #this function will prompt the user to select a table to delete           
    def delete_table():
        print("You selected to delete a table from database: ", datb)
        print("Accepting Name for deleting Table.")
        window.destroy()
        window2 = Tk()
        window2.title("Delete Table")
        label1 = Label(window2, text = "Enter Table Name: ").grid(row = 0, column = 0)

        #Creating a Drop Down Menu for deleting a table
        table1 = StringVar()
        table1.set("")
        table = OptionMenu(window2, table1, *table_list).grid(row = 0, column = 1)
        #This fucntion check if the user has selected a window or not once the button is clicked
        def check():
            if table1.get() == "":
                print("Please select a Table from the menu.")
                labelx = Label(window2, text = "Please select a Table from the menu.").grid(row = 8, columnspan = 2)
            else:
                delete()
        
        #This function recieves the table name and deletes it
        def delete():
            x = str(table1.get())
            print("Table Name Recieved: ", x)
            
            conn = mysql.connector.connect(host = "localhost", user = name, password = pswd, database = datb)
            cursh = conn.cursor()
            cursh.execute("drop table " + x)
            print("Table Deleted.")
            window2.destroy()
            home2(name, pswd, datb)
            
        #Button to trigger delete fucntion
        mybutton = Button(window2, text = "Delete", command = check).grid(row = 1,column = 0, columnspan = 2)
        #Button to go back to main menu
        def cancel():
            print("Deleting Table Cancelled.")
            print()
            window2.destroy()
            home2(name, pswd, datb)
        button3 = Button(window2, text = "Cancel", command = cancel).grid(row = 7, columnspan = 2)
        window2.mainloop()


    #This function will check if there are any tables in the database
    def check_desc():
            if table_list == []:
                print("There are no tables to delete in the database.")
                error = Label(window, text = "   There are no tables to describe in the database.   ")
                error.grid(row = 13, columnspan = 2)
            else:
                desc_table()
    #This function will open a new window and ask for the table name to describe
    def desc_table():
        window.destroy()
        window1 = Tk()
        window1.title("Describe Table")
        print("You selected to descirbe a Table.")
        print("Select Table to Descibe.")
        Heading = Label(window1, text = "Select a Table to describe:").grid()
        sel_table = StringVar()
        menu = OptionMenu(window1, sel_table, *table_list)
        menu.grid(row = 0, column = 1)
        #This function used a frame to display the description of the tabe
        #in the form of a table
        #if any other frames are present, it deletes them and create a new frame
        def check():
            try:
                frame1.destroy()
            except Exception:
                pass
            #Here it checks whether the user has selected a table
            if sel_table.get() == "":
                print("Please select a Table from the menu.")
                labelx = Label(window1, text = "Please select a Table from the menu.").grid(row = 8, columnspan = 2)
            else:
                desc()
        #This function will gather all the details of the table
        #an display the contents in the form of a table
        def desc():
            global frame1
            frame1 = Frame(window1)
            table_name = sel_table.get()
            conn = mysql.connector.connect(host = "localhost", user = name, password = pswd, database = datb)
            cursh = conn.cursor()
            cursh.execute("desc "+table_name)
            data = list(cursh)
            Frame_Head = Label(frame1, text = "Table Name = "+table_name).grid(row = 0, column = 0, columnspan = 6)
            head1 = Label(frame1, text = "Field").grid(row = 1, column = 0)
            head2 = Label(frame1, text = "Type").grid(row = 1, column = 1)
            head3 = Label(frame1, text = "NULL").grid(row = 1, column = 2)
            head4 = Label(frame1, text = "Key").grid(row = 1, column = 3)
            head5 = Label(frame1, text = "Default").grid(row = 1, column = 4)
            head6 = Label(frame1, text = "Extra").grid(row = 1, column = 5)
            #All the table properties are displayes as Entry Boxes with data fed into them
            entry_boxes = {}
            for i in range(len(data)):
                for j in range(6):
                    entry_boxes["E"+str(i)+str(j)] = "Entry(frame1)"
            for k,v in entry_boxes.items():
                exec("%s=%s"%(k,v))

            for i in range(len(data)):
                for j in range(6):
                    exec('E'+str(i)+str(j)+'.insert(0, "'+str(data[i][j])+'")')
                    exec('E'+str(i)+str(j)+'.grid(row = i+2, column = j)')

            frame1.grid(row = 2, columnspan = 6)
                    
            
        #Button to go back to main menu
        def back():
            print("Returning to Main Menu.")
            print()
            window1.destroy()
            home2(name, pswd, datb)
        button3 = Button(window1, text = "Back", command = back).grid(row = 1, columnspan = 3, column = 2)
        button1 = Button(window1, text = "Describe", command = check).grid(row = 1, columnspan = 3, pady = 10)
    #This function will check if there are any tables in the database to insert data to   
    def check_insert():
            if table_list == []:
                print("There are no tables to insert data in the database.")
                error = Label(window, text = "   There are no tables to insert data in the database.   ")
                error.grid(row = 13, columnspan = 2)
            else:
                insert() 
    #This function will create new window to prompt the user to select a table
    def insert():
        window.destroy()
        window1 = Tk()
        window1.title("Insert Data")
        print("You selected to insert data into a Table.")
        print("Select Table to insert data.")
        Heading = Label(window1, text = "Select a Table to insert data:").grid()
        sel_table = StringVar()
        menu = OptionMenu(window1, sel_table, *table_list)
        menu.grid(row = 0, column = 1)
        table_row1 = Label(window1, text = "Enter No of Rows to be Added: ").grid(row = 1)
        table_row2 = Entry(window1)
        table_row2.grid(row = 1, column = 1)
        global label_text
        label_text = StringVar()
        label_text.set("")
        #This function checks whether the user has selected a table
        def check1():
            if sel_table.get() == "":
                print("Please select a Table from the menu.")
                label_text.set("Please select a Table from the menu.")
                try:
                    labelx = Label(window1, textvariable = label_text).grid(row = 2, columnspan = 2)
                except Exception:
                    pass
            else:
                check2()
        #This function checks whether the no of rows entered by the user is a numeral
        def check2():
            if table_row2.get() != "":
                if table_row2.get().isdigit():
                    if int(table_row2.get()) > 10 or int(table_row2.get()) == 0:
                        print("No of rows ahould be a numeral between 1 and 10.")
                        label_text.set("No of rows ahould be a numeral between 1 and 10.")
                    else:
                        print("No of Rows received: ", table_row2.get())
                        insert_data()
                else:
                    print("No of rows must be a numeral.")
                    label_text.set("No of rows must be a numeral.")
                
            else:
                print("Please enter the no of rows to be added.")
                label_text.set("Please enter the no of rows to be added")
            try:
                labelx = Label(window1, textvariable = label_text).grid(row = 2, columnspan = 2)
            except Exception:
                pass
 
        #This function is triggered when all checks are done
        #and creates a window with the no of row entered by the user where data can be entered
        def insert_data():
            #getting the no of rows and table name
            rows = table_row2.get()
            table1 = sel_table.get()
            window1.destroy()
            window2 = Tk()
            window2.title("Insert Data")
            conn = mysql.connector.connect(host = "localhost", user = name, password = pswd, database = datb)
            cursh = conn.cursor()
            #Reading all the details of the table to impose checks
            cursh.execute("desc "+table1)
            data = list(cursh)
            #Lists to store Field Names and Datatypes
            fields = []
            datatypes = []
            for i in data:
                fields.append(i[0])
                #This list contain commands to fetch the details of each datatype
                datatypes.append(i[1])
            
            Heading = Label(window2, text = "Adding Data to Table: " + table1).grid(columnspan = len(data)+1)
            #Creating headings for each Field
            labels = {}
            for i in range(len(data)):
                labels["h1"+str(i)] = "Label(window2, text = '"+str(fields[i])+"').grid(row = 1, column = "+str(i+1)+")"
                labels["h2"+str(i)] = 'Label(window2, text = "'+str(datatypes[i])+'").grid(row = 2, column = '+str(i+1)+')'
            #Creating RECORD Numbers and displaying them 
            labels2 = {}
            
            for i in range(int(rows)):
                labels2["h3"+str(i)] = "Label(window2, text = 'Record "+str(i+1)+"').grid(row = "+str(i+3)+", padx = 5)"
            #Creating all the necessaaaaary variables
            for k,v in labels.items():
                exec("%s=%s"%(k,v))
            for k,v in labels2.items():
                exec("%s=%s"%(k,v))
            #Creating all the Entry Boxes
            row_dict = {}
            for i in range(int(rows)):
                for j in range(len(data)):
                    row_dict["r"+str(i)+str(j)] = "Entry(window2)"

            for k,v in row_dict.items():
                exec("%s=%s"%(k,v))
            #Placing all the Entry Boxes
            for i in range(int(rows)):
                for j in range(len(data)):
                    exec("r"+str(i)+str(j)+".grid(row = "+str(i+3)+", column = "+str(j+1)+")")
            #This dictionary will be used by eval to fetch the data entered in the Entry Boxes
            local_names = locals()
            print("Table Created. Please enter Table Data.")
            help1 = Label(window2, text = "Refer to the guidelines for entering any data:")
            help1.grid(row = int(rows)+5, columnspan = 666)
            help2 = Label(window2, text = "1. All Input Errors will appear in Python Interpreter.")
            help2.grid(row = int(rows)+6, columnspan = 666)
            help5 = Label(window2, text = "2. For Date datatype use 8 digit strings. eg: 20200410 for 2020-April-10.")
            help5.grid(row = int(rows)+7, columnspan = 666)
            help3 = Label(window2, text = "3.There should be no spaces in the input '(Total_length,Precision). Eg: (8,4)'")
            help3.grid(row = int(rows)+8, columnspan = 666)
            help6 = Label(window2, text = "4. Input for Numeric and Decimal data type must be in the form: (Total_length,Precision) eg: (8,2)")
            help6.grid(row = int(rows)+9, columnspan = 666)

            

            
            def final_insert(local_names):
                
                table_entries = []
                for i in range(int(rows)):
                    curr_row = []
                    for j in range(len(data)):
                        curr_row.append(eval("r"+str(i)+str(j)+".get()", local_names))
                    table_entries.append(curr_row)

                print("Checking User Inputs...")

                Errors = []
                
                for j in range(len(data)):
                    if str(datatypes[j]) in ("bigint", "smallint", "int","b'int'","b'smallint'","b'bigint'"):
                        x = str(datatypes[j])
                        ref_dict = {"int":10, "bigint":20, "smallint":5,"b'int'":10,"b'smallint'":5,"b'bigint'":20}
                        for i in range(int(rows)):
                            if table_entries[i][j] == "":
                                Errors.append("No Data Entered in Field: "+fields[j]+" Record: "+str(i+1))
                            else:
                                if table_entries[i][j].isdigit() or table_entries[i][j][1:].isdigit() and table_entries[i][j][0] == "-":
                                    if len(table_entries[i][j]) in range(ref_dict[x]+1) or len(table_entries[i][j]) in range(ref_dict[x]+2) and table_entries[0] == "-":
                                        pass
                                    else:
                                        Errors.append(x+" datatype accepts input of length from 1 to "+str(ref_dict[x])+". Field: "+fields[j]+" Record: "+str(i+1))
                                else:
                                    Errors.append(x+" datatype only accepts integers. Field: "+fields[j]+" Record: "+str(i+1))

                    elif str(datatypes[j]) in ("tinytext'", "longtext", "mediumtext", "text","b'tinytext'","b'longtext'","b'mediumtext'","b'text'"):
                        x = str(datatypes[j])
                        ref_dict = {"tinytext":255, "text":65535, "mediumtext":16777215, "longtext":4294967295,"b'tinytext'":255,"b'longtext'":4294967295,"b'mediumtext'":16777215,"b'text'":65535}
                        for i in range(int(rows)):
                            if table_entries[i][j] == "":
                                Errors.append("No Data Entered in Field: "+fields[j]+" Record: "+str(i+1))
                            else:
                                if len(table_entries[i][j]) > ref_dict[x]:
                                    Errors.append(x+" datatype only accepts strings upto "+str(ref_dict[x])+" characters. Fields = "+fields[j]+" Row = "+str(i+1))
                
                                
                    elif "numeric" in str(datatypes[j]) or "decimal" in str(datatypes[j]):
                        x = str(datatypes[j])
                        for i in range(int(rows)):
                            if table_entries[i][j] == "":
                                Errors.append("No Data Entered in Field: "+fields[j]+" Record: "+str(i+1))
                            else:
                                if "." in table_entries[i][j]:
                                    input_ = list(table_entries[i][j].split("."))
                                    for k in input_:
                                        if not k.isdigit():
                                            Errors.append("Invalid Input. Alphabets not allowed in "+x+" datatype. Fields = "+fields[j]+" Row = "+str(i+1))
                                    
                                    len_num1 = int(str(datatypes[j])[str(datatypes[j]).index("(")+1:str(datatypes[j]).index(",")])
                                    len_num2 = int(str(datatypes[j])[str(datatypes[j]).index(",")+1:str(datatypes[j]).index(")")])
                                    if len(input_[0]) > len_num1 - len_num2:
                                        Errors.append("Check your Input according to the "+x+"datatype precision and total length attributes. Fields = "+fields[j]+" Row = "+str(i+1))
                                else:
                                    Errors.append("Input does not conatin decimal. Fields = "+fields[j]+" Row = "+str(i+1))
                                                
                    elif str(datatypes[j]) in ("date","b'date'"):
                        for i in range(int(rows)):
                            if table_entries[i][j] == "":
                                Errors.append("No Data Entered in Field: "+fields[j]+" Record: "+str(i+1))
                            else:
                                if table_entries[i][j].isdigit() and len(table_entries[i][j]) == 8:
                                    if int(table_entries[i][j][4:6]) <= 12:
                                        leap_year = False
                                        if int(table_entries[i][j][0:4]) % 4 == 0:
                                            if int(table_entries[i][j][0:4]) % 100 != 0:
                                                leap_year = False
                                            elif int(table_entries[i][j][0:4]) % 400 == 0:
                                                leap_year = True
                                        if leap_year == True:
                                            days = [31,29,31,30,31,30,31,31,30,31,30,31]
                                        else:
                                            days = [31,28,31,30,31,30,31,31,30,31,30,31]

                                        if int(table_entries[i][j][6:]) > days[int(table_entries[i][j][4:6])-1]:
                                            Errors.append("Invalid Date in Field: "+fields[j]+" Record: "+str(i+1))
                                    else:
                                        Errors.append("Incorrect Month in Field: "+fields[j]+" Record: "+str(i+1))
                                else:
                                    Errors.append("Only 8 digits numbers allowed for date. Field: "+fields[j]+" Record: "+str(i+1))

                    elif str(datatypes[j]) in ("time","b'time'"):
                        for i in range(int(rows)):
                            if table_entries[i][j] == "":
                                Errors.append("No Data Entered in Field: "+fields[j]+" Record: "+str(i+1))
                            else:
                                if table_entries[i][j].isdigit() and len(table_entries[i][j]) == 6:
                                    if int(table_entries[i][j][:2]) > 24:
                                        Errors.append("Invalid No of Hours in Field: "+fields[j]+" Record: "+str(i+1))
                                    else:
                                        if int(table_entries[i][j][2:4]) > 59:
                                            Errors.append("Invalid No of Minutes in Field: "+fields[j]+" Record: "+str(i+1))
                                        else:
                                            if int(table_entries[i][j][2:4]) > 59:
                                                Errors.append("Invalid No of Seconds in Field: "+fields[j]+" Record: "+str(i+1))

                    else:
                        for i in range(int(rows)):
                            if table_entries[i][j] == "":
                                Errors.append("No Data Entered in Field: "+fields[j]+" Record: "+str(i+1))
                    
                        
                    
                if Errors != []:
                    print()
                    print("Please check these detcted errors in your input:")
                    labelx = Label(window2, text = "Please check the errors detected in your input from the Python Interpretor.")
                    labelx.grid(row = int(rows)+5, columnspan = len(datatypes)+1)
                    var = 1
                    for i in Errors:
                        print(str(var)+"-->"+i)
                        var += 1
                else:
                    print("All values checked. Expecting no errors.")
                    sql_statement = "insert into " + table1 + " values"
                    for i in range(int(rows)):
                        if len(table_entries[i]) == 1:
                            sql_statement += str(tuple(table_entries[i]))[:-2] + "),"
                        else:
                            sql_statement += str(tuple(table_entries[i])) + ","
                        
                    sql_statement2 = sql_statement[:-1]
                    print("Inserting Values into MySQL table.")
                    conn = mysql.connector.connect(host = "localhost", user = name, password = pswd, database = datb)
                    cursh = conn.cursor()
                    cursh.execute(sql_statement2)
                    conn.commit()
                    print("Adding values successfull.Returning to Main Menu.")
                    window2.destroy()
                    home2(name, pswd, datb)
            final_button = Button(window2, text = "Insert Data", command = lambda:final_insert(local_names))
            final_button.grid(row = int(rows)+3, columnspan = len(data)+1)

            def back():
                    print("Returning to Main Menu.")
                    print()
                    window2.destroy()
                    home2(name, pswd, datb)
            button3 = Button(window2, text = "Back", command = back).grid(row = int(rows)+4, columnspan = len(data)+1)
                
        def back():
            print("Returning to Main Menu.")
            print()
            window1.destroy()
            home2(name, pswd, datb)
        button3 = Button(window1, text = "Cancel", command = back).grid(row = 3, column = 1)
        button_ = Button(window1, text = "Insert", command = check1).grid(row = 3)
        

        
    def check_retreive():
        if table_list == []:
            print("There are no tables to retreive data in the database.")
            error = Label(window, text = "   There are no tables to reteive data in the database.   ")
            error.grid(row = 13, columnspan = 2)
        else:
            retreive()   
    def retreive():
        print("You selected to retreive a table from database: ", datb)
        print("Accepting Name for Target Table.")
        window.destroy()
        window2 = Tk()
        window2.title("Retreive Data")
        label1 = Label(window2, text = "Enter Table Name: ").grid(row = 0, column = 0)

        #Creating a Drop Down Menu 
        table1 = StringVar()
        table1.set("")
        table = OptionMenu(window2, table1, *table_list).grid(row = 0, column = 1)

        def final_retreive():
            table2 = table1.get()
            window2.destroy()
            window1 = Tk()
            window1.title("Data from " + table2)
            conn = mysql.connector.connect(host = "localhost", user = name, password = pswd, database = datb)
            cursh = conn.cursor()
            cursh.execute("desc "+table2)
            data_ = list(cursh)
            fields = []
            for i in data_:
                fields.append(i[0])
            cursh.execute("select * from "+table2)
            data_ = list(cursh)

            print("Content from "+table2)
            heading = Label(window1, text = "Showing Content from Table: "+table2+" Database: "+datb).grid(columnspan = len(fields))
            #Displaying all the Fields as Heads
            head_dict = {}
            for i in range(len(fields)):
                head_dict["head"+str(i)] = "Label(window1, text = '"+fields[i]+"').grid(row = 1, column = "+str(i)+")"
            for k,v in head_dict.items():
                exec("%s=%s"%(k,v))

            #Displaying all Elements of the table
            elements = {}
            for i in range(len(data_)):
                for j in range(len(data_[0])):
                    elements["var"+str(i)+str(j)] = "Entry(window1)"
            for k,v in elements.items():
                exec("%s=%s"%(k,v))

            for i in range(len(data_)):
                for j in range(len(data_[0])):
                    exec("var"+str(i)+str(j)+".insert(0, data_[i][j])")
                    exec("var"+str(i)+str(j)+".grid(row = i+2, column = j)")
            def back():
                print("Returning to Main Menu.")
                print()
                window1.destroy()
                home2(name, pswd, datb)
            button3 = Button(window1, text = "Back", command = back).grid(row = len(data_)+3, columnspan = len(fields))

            
              
                

            
            

        def check():
            if table1.get() == "":
                print("Please select a Table from the menu.")
                labelx = Label(window2, text = "Please select a Table from the menu.").grid(row = 3, columnspan = 2)
            else:
                final_retreive()

        #Button to trigger check fucntion
        mybutton = Button(window2, text = "Retreive Data", command = check).grid(row = 1,column = 0, columnspan = 2)
        
        def cancel():
            print("Retreiving Data from Table Cancelled.")
            print()
            window2.destroy()
            home2(name, pswd, datb)
        button3 = Button(window2, text = "Cancel", command = cancel).grid(row = 2, columnspan = 2)


        
    def check_delete_data():
        if table_list == []:
            print("There are no tables to delete data in the database.")
            error = Label(window, text = "   There are no tables to delete data in the database.   ")
            error.grid(row = 13, columnspan = 2)
        else:
            delete_data()   
    def delete_data():
        print("You selected to delete rows from a table in database: ", datb)
        print("Accepting Name for Target Table.")
        window.destroy()
        window2 = Tk()
        window2.title("Delete Data")
        label1 = Label(window2, text = "Enter Table Name: ").grid(row = 0, column = 0)

        #Creating a Drop Down Menu 
        table1 = StringVar()
        table1.set("")
        table = OptionMenu(window2, table1, *table_list).grid(row = 0, column = 1)
        Error_text = StringVar()
        Error_label = Label(window2, textvariable = Error_text).grid(row = 3, columnspan = 2)
        Error_text.set("")
        
        def check1():
            table2 = str(table1.get())
            if table2 == "":
                print("Please select a table from the menu.")
                Error_text.set("Please select a Table from the Menu.")
            else:
                conn = mysql.connector.connect(host = "localhost", user = name, password = pswd, database = datb)
                cursh = conn.cursor()
                cursh.execute("Select * from "+table2)
                if len(list(cursh)) == 0:
                    print("There are no records in this table to delete.")
                    Error_text.set("There are no records in this table to delete.")
                else:
                    delete1()
                
                
                

        def delete1():
            table2 = str(table1.get())
            window2.destroy()
            window1 = Tk()
            window1.title("Data from " + table2)
            conn = mysql.connector.connect(host = "localhost", user = name, password = pswd, database = datb)
            cursh = conn.cursor()
            cursh.execute("desc "+table2)
            data_ = list(cursh)
            fields = []
            for i in data_:
                fields.append(i[0])
            cursh.execute("select * from "+table2)
            data_ = list(cursh)

            print("Content from "+table2)
            heading = Label(window1, text = "Showing Content from Table: "+table2+" Database: "+datb).grid(columnspan = 1+len(fields))
            #Displaying all the Fields as Heads
            head_dict = {}
            for i in range(len(fields)):
                head_dict["head"+str(i)] = "Label(window1, text = '"+fields[i]+"').grid(row = 1, column = "+str(i+1)+")"
            for k,v in head_dict.items():
                exec("%s=%s"%(k,v))

            #Displaying all Elements of the table and creating checkboxes
            elements = {}
            checkboxes = {}
            checkboxes_var = {}
            for i in range(len(data_)):
                checkboxes["c"+str(i)] = "IntVar()"
                checkboxes["check"+str(i)] = "Checkbutton(window1, text = '', variable = c"+str(i)+").grid(row = "+str(i)+"+2)"
                for j in range(len(data_[0])):
                    elements["var"+str(i)+str(j)] = "Entry(window1)"
            for k,v in elements.items():
                exec("%s=%s"%(k,v))
            for k,v in checkboxes.items():
                exec("%s=%s"%(k,v))
                

            for i in range(len(data_)):
                for j in range(len(data_[0])):
                    exec("var"+str(i)+str(j)+".insert(0, data_[i][j])")
                    exec("var"+str(i)+str(j)+".grid(row = i+2, column = j+1)")
            local_var = locals()
            
            def final_delete(local_var):
                sel_rows = []
                for i in range(len(data_)):
                    if eval("c"+str(i)+".get()", local_var) == 1:
                        sel_rows.append(i)
                sel_rows2 = []
                for i in sel_rows:
                    sel_rows2.append(i+1)
                print("Rows Recieved: ", sel_rows2)
                conn = mysql.connector.connect(host = "localhost", user = name , password = pswd, database = datb)
                cursh = conn.cursor()
                for i in sel_rows:
                    sql_statement = "delete from "+table2+" where "+str(fields[0])+" = '"+str(data_[i][0])+"'"
                    cursh.execute(sql_statement)
                conn.commit()
                print("All selected rows deleted successfully.")
                print("Returning to Main Menu.")
                window1.destroy()
                home2(name, pswd, datb)
    
            button4 = Button(window1, text = "Delete Selected Records", command = lambda:final_delete(local_var))
            button4.grid(row = len(data_)+3, columnspan = 1+len(fields))

            
            
            def back():
                print("Returning to Main Menu.")
                print()
                window1.destroy()
                home2(name, pswd, datb)
            button3 = Button(window1, text = "Back", command = back).grid(row = len(data_)+4, columnspan = 1+len(fields))
            
        def back():
            print("Returning to Main Menu.")
            print()
            window2.destroy()
            home2(name, pswd, datb)
        button3 = Button(window2, text = "Back", command = back).grid(row = 2, columnspan = 2)
        button2 = Button(window2, text = "Delete", command = check1).grid(row = 1, columnspan = 2)
        
        
        



    
    def check_export():
        if table_list == []:
            print("There are no tables to export data in the database.")
            error = Label(window, text = "   There are no tables to export data in the database.   ")
            error.grid(row = 13, columnspan = 2)
        else:
            export()
    def export():
        print("You selected to retreive a table from database: ", datb)
        print("Accepting Name for Target Table.")
        window.destroy()
        window2 = Tk()
        window2.title("Export Data")
        label1 = Label(window2, text = "Enter Table Name: ").grid(row = 0, column = 0)

        #Creating a Drop Down Menu 
        table1 = StringVar()
        table1.set("")
        table = OptionMenu(window2, table1, *table_list).grid(row = 0, column = 1)

        def final_export():
            print()
            table2 = table1.get()
            conn = mysql.connector.connect(host = "localhost", user = name, password = pswd, database = datb)
            cursh = conn.cursor()
            cursh.execute("desc "+table2)
            data_ = list(cursh)
            fields = []
            for i in data_:
                fields.append(i[0])
            cursh.execute("select * from "+table2)
            data_ = list(cursh)
            data_.insert(0, tuple(fields))
            import csv
            with open(datb+'.'+table2+'.csv','w',newline='') as f:
                obj=csv.writer(f)
                obj.writerow(data_[0])
                s=[]
                for i in range(1,len(data_)):
                    s.append(data_[i])
        
                
                for row in s:
                    obj.writerow(row)
                
            print("Export Sucessfull. File Created: "+datb+"."+table2+'.csv' )
            print()
            
        def check():
            if table1.get() == "":
                print("Please select a Table from the menu.")
                labelx = Label(window2, text = "Please select a Table from the menu.").grid(row = 3, columnspan = 2)
            else:
                final_export()

        #Button to trigger check fucntion
        mybutton = Button(window2, text = "Export Data", command = check).grid(row = 1,column = 0, columnspan = 2)
        
        def cancel():
            print("Exporting Table Cancelled.")
            print()
            window2.destroy()
            home2(name, pswd, datb)
        button3 = Button(window2, text = "Cancel", command = cancel).grid(row = 2, columnspan = 2)
    
        
    #Buttons and Statements used to trigger any of the above functions
    Button1 = Button(window, text = "Create Table", command = create_table).grid(row = 3, column = 1)
    Label1 = Label(window, text = "Create a new empty Table: ").grid(row = 3, column = 0)
    
    Button3 = Button(window, text = "Delete Table", command = check_delete).grid(row = 5, column = 1)
    Label3 = Label(window, text = "Delete existing table: ").grid(row = 5, column = 0)

    Button4 = Button(window, text = "Describe Table", command = check_desc).grid(row = 6, column = 1)
    Label4 = Label(window, text = "Describe existing table: ").grid(row = 6, column = 0)

    Button5 = Button(window, text = "Add Data", command = check_insert).grid(row = 7, column = 1)
    Label5 = Label(window, text = "Insert multiple Rows in a Table: ").grid(row = 7, column = 0)
    
    Button6 = Button(window, text = "Retreive Data", command = check_retreive).grid(row = 8, column = 1)
    Label6 = Label(window, text = "Retreive Data using SELECT: ").grid(row = 8, column = 0)

    Button7 = Button(window, text = "Delete Data", command = check_delete_data).grid(row = 9, column = 1)
    Label7 = Label(window, text = "Delete Rows in a Table: ").grid(row = 9, column = 0)

    Button8 = Button(window, text = "Export Data", command = check_export).grid(row = 10, column = 1)
    Label8 = Label(window, text = "Export data using File Handling: ").grid(row = 10, column = 0)
    

    Label9 = Label(window, text = "Available Tables: ").grid(row = 11, column = 0)
    #Create a listbox to display all available tables
    Frame1 = Frame(window)
    scroll = Scrollbar(Frame1, orient = VERTICAL)
    table_listbox = Listbox(Frame1, width = 50, yscrollcommand = scroll.set)
    table_listbox.insert(END, *table_list)
    table_listbox.pack(side = LEFT)
    scroll.config(command = table_listbox.yview)
    scroll.pack(side = RIGHT, fill = Y)

    Frame1.grid(row = 12, columnspan = 2)
    
    
    
        
    

