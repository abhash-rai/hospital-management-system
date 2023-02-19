# Imports
from Admin import Admin
from Doctor import Doctor
from Patient import Patient
from tkinter import END
import tkinter as tk

class Main:

    def __init__(self):
        # Initialising the actors

        # admin = Admin('admin','123','B1 1AB') # username is 'admin', password is '123'
        self.admin = self.database_to_model("./data/admin.txt", 'admin')

        # doctors = [Doctor('John','Smith','Internal Med.'), Doctor('Jone','Smith','Pediatrics'), Doctor('Jone','Carlos','Cardiology')]
        self.doctors = self.database_to_model("./data/doctors.txt", 'doctor')

        # patients = [Patient('Sara','Smith', 20, '07012345678','B1 234'), Patient('Mike','Jones', 37,'07555551234','L2 2AB'), Patient('Daivd','Smith', 15, '07123456789','C1 ABC')]
        self.patients = self.database_to_model("./data/patients.txt", 'patient')
        self.patients = self.admin.group_patients_by_family(self.patients) # Patients of the same family are grouped together 
        
        self.discharged_patients = []

        self.__intermediate_variable = None #This variable will be used by methods to store value temporarily while managing GUIs

        self.window = tk.Tk()
        self.window.geometry("350x350")

        self.on_start_show_admin_log_in()

    def database_to_model(self, person_database_file, person_type):
        """
        This function reads a given path file (person_database_file) and according to the passed type (person_type) of the file, creates and returns list of that type of objects.
        Args:
            person_database_file (str): path of database file 
            person_type (str): type of "person_database_file"; could be either "admin" or "doctor" or "patient" only
        returns:
            list: A list of objects
        """
        person_database = open(person_database_file, 'r')

        parameter_list = [] # Each element in this list is a list of object's parameters
        for index, line in enumerate(person_database):
            if index != 0: # skipping first line as it is just indicator of the columns
                if line != "\n" or line != "":
                    parameters = line.split(",")
                    parameters = [parameter.strip() for parameter in parameters]
                    parameter_list.append(parameters)
        
        # if the given file is of admin
        if person_type.lower() == "admin" or person_type.lower() == "admin":
            try: # trying to create list of a admin object and returning
                parameter_list = parameter_list[0]
                return Admin(parameter_list[0], parameter_list[1], parameter_list[2])
            except: # incase creation of object fails, throwing error and giving error context
                print(f"'{person_database_file}' has invalid structure!")
                print('Structure should follow "username, password, address"')
                exit()

        # if the given file is of doctor
        elif person_type.lower() == "doctor" or person_type.lower() == "doctor":
            try: # trying to create list of object and returning
                object_list = []
                for each in parameter_list:
                    doctor = Doctor(each[0], each[1], each[2])
                    object_list.append(doctor)
                return object_list
            except: # incase creation of object fails, throwing error and giving error context
                print(f"'{person_database_file}' has invalid structure!")
                print('Structure should follow "first_name, surname, speciality" seperated by new line for every object')
                exit()

        # if the given file is of patient
        elif person_type.lower() == "patient" or person_type.lower() == "patient":
            try: # trying to create list of object and returning
                object_list = []
                for each in parameter_list:
                    symptoms = each[-1].split("+")
                    symptoms = [each.strip() for each in symptoms]
                    patient = Patient(each[0], each[1], int(each[2]), each[3], each[4], symptoms)
                    object_list.append(patient)

                return object_list

            except: # incase creation of object fails, throwing error and giving error context
                print(f"'{person_database_file}' has invalid structure!")
                print('Structure should follow "first_name, surname, age, mobile, postcode, symptoms" seperated by new line for every object')
                exit()
        
        else:
            print("Passed 'person_type' is invalid! ")
            
    def make_window_responsive(self, no_of_rows, no_of_cols):
        # configure all given rows and columns to be responsive
        for i in range(no_of_rows):
            self.window.grid_rowconfigure(i, weight=1)
        if no_of_cols == 1:
            self.window.grid_columnconfigure(0, weight=1)
        else:
            for i in range(no_of_cols):
                self.window.grid_columnconfigure(i, weight=1)

    def clear_previous_widgets(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    # def center_widgets(self):
    #     for widget in self.window.winfo_children():
    #         widget.pack_configure(anchor="center")

    def add_multiple_widgets(self, row_index_gui, options_list, options_button_actions_list):
        for index, (button, action) in enumerate(zip(options_list, options_button_actions_list)):
            self.add_button = tk.Button(self.window, text=button, command=action)
            self.add_button.grid(row=index+row_index_gui, column=0)









    def on_start_show_admin_log_in(self):
        self.window.title("Admin Log In")

        self.total_text_label = tk.Label(self.window, text="-----Login-----")
        self.total_text_label.grid(row=0, column=0, columnspan=3)

        self.username_label = tk.Label(self.window, text="Enter the username:")
        self.username_label.grid(row=1, column=0)

        self.username_entry = tk.Entry(self.window)
        self.username_entry.grid(row=1, column=1)

        self.password_label = tk.Label(self.window, text="Enter the password:")
        self.password_label.grid(row=2, column=0)

        self.password_entry = tk.Entry(self.window)
        self.password_entry.grid(row=2, column=1)

        self.logIn_button = tk.Button(self.window, text="Log In", command=self.admin_logIn_action)
        self.logIn_button.grid(row=3, column=0, columnspan=3)

        self.alert_variable = tk.StringVar()
        self.alert_variable.set("")
        self.alert_label = tk.Label(self.window, textvariable=self.alert_variable)
        self.alert_label.grid(row=4, column=0, columnspan=3)

        self.make_window_responsive(5,2)

    def admin_logIn_action(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.admin.login_for_GUI(username, password):
            self.home_window()
        else:
            self.username_entry.delete(0, "end") # Clearing userinput entry field
            self.password_entry.delete(0, "end") # Clearing userinput entry field

            self.alert_label.config(fg= "red")
            self.alert_variable.set("Incorrect username or password.")











    def home_window(self):
        self.clear_previous_widgets()
        self.window.geometry("320x350")

        self.window.title("Hospital Management System")

        index_options = [
            "Register/view/update/delete doctor",
            "Add patients",
            "View/Discharge patients",
            "View discharged patient",
            "Book appointment/check appointment status",
            "Assign doctor to a patient",
            "Relocate a patient from one doctor to another",
            "Update admin detais",
            "Request management report",
            "Quit"
        ]
        index_button_actions = [
            self.doctor_management_action,
            self.add_patient_action,
            self.view_or_discharge_patient_action,
            self.view_discharged_patient,
            self.appointment_management_action,
            self.assign_doctor_to_patient_action,
            self.relocate_patient_to_another_doctor_action,
            self.update_admin_details_action,
            self.request_management_report_action,
            self.stop,
        ]

        self.text_label = tk.Label(self.window, text="Choose the operation:")
        self.text_label.grid(row=0, column=0)

        self.add_multiple_widgets(1, index_options, index_button_actions)

        self.make_window_responsive(11,1)














    def doctor_management_action(self):

        self.clear_previous_widgets()
        self.window.title("Doctors Management")

        doctor_management_options = [
            "Register Doctor",
            "View Doctors",
            "Update Doctor Detail",
            "Delete Doctor",
            "Go to Home"
        ]
        doctor_management_button_actions = [
            self.register_doctor_action,
            self.view_doctor_action,
            self.update_doctor_action,
            self.delete_doctor_action,
            self.home_window,
        ]

        self.text_label = tk.Label(self.window, text="-----Doctor Management-----")
        self.text_label.grid(row=0, column=0)

        self.add_multiple_widgets(1, doctor_management_options, doctor_management_button_actions)

        self.make_window_responsive(6,1)
    
    def register_doctor_action(self):
        self.clear_previous_widgets()
        self.window.title("Register Doctor")

        self.text_label = tk.Label(self.window, text="-----Register-----")
        self.text_label.grid(row=0, column=0, columnspan=3)

        self.fname_label = tk.Label(self.window, text="Enter firstname:")
        self.fname_label.grid(row=1, column=0)

        self.fname_entry = tk.Entry(self.window)
        self.fname_entry.grid(row=1, column=1)

        self.lname_label = tk.Label(self.window, text="Enter surname:")
        self.lname_label.grid(row=2, column=0)

        self.lname_entry = tk.Entry(self.window)
        self.lname_entry.grid(row=2, column=1)

        self.speciality_label = tk.Label(self.window, text="Enter speciality:")
        self.speciality_label.grid(row=3, column=0)

        self.speciality_entry = tk.Entry(self.window)
        self.speciality_entry.grid(row=3, column=1)

        self.register_doctor_button = tk.Button(self.window, text="Register", command=self.register_doctor_button_action)
        self.register_doctor_button.grid(row=4, column=0, columnspan=3)

        self.go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
        self.go_home_button.grid(row=5, column=0, columnspan=3)

        self.alert_variable = tk.StringVar()
        self.alert_variable.set("")
        self.alert_label = tk.Label(self.window, textvariable=self.alert_variable)
        self.alert_label.grid(row=6, column=0, columnspan=3)

        self.make_window_responsive(7,1)
        
    def register_doctor_button_action(self):
        new_doctor_f_name = self.fname_entry.get()
        new_doctor_l_name = self.lname_entry.get()
        new_doctor_speciality = self.speciality_entry.get()

        # Checking for invalid input
        user_valid_input_counter = 0
        if new_doctor_f_name.isspace() == True or new_doctor_f_name == '' or new_doctor_l_name.isspace() == True or new_doctor_l_name == '' or new_doctor_speciality.isspace() == True or new_doctor_l_name == '':
            self.fname_entry.delete(0, "end") # Clearing userinput entry field
            self.lname_entry.delete(0, "end") # Clearing userinput entry field
            self.speciality_entry.delete(0, "end") # Clearing userinput entry field

            self.alert_label.config(fg= "red")
            self.alert_variable.set("Please give a valid input - Not empty strings or spaces.")
        # if valid input
        else:
            # check if the name is already registered
            name_exists = False
            for doctor in self.doctors:
                if new_doctor_f_name == doctor.get_first_name() and new_doctor_l_name == doctor.get_surname():
                    self.fname_entry.delete(0, "end") # Clearing userinput entry field
                    self.lname_entry.delete(0, "end") # Clearing userinput entry field
                    self.speciality_entry.delete(0, "end") # Clearing userinput entry field

                    self.alert_label.config(fg= "red")
                    self.alert_variable.set("Doctor name already exists.")

                    name_exists = True
                    break # save time and end the loop

            if name_exists == False:
                new_doc = Doctor(new_doctor_f_name, new_doctor_l_name, new_doctor_speciality) 
                self.doctors.append(new_doc) # add the doctor ...
                                                         # ... to the list of doctors
                self.admin.add_entry_to_database("./data/doctors.txt", f"{new_doctor_f_name}, {new_doctor_l_name}, {new_doctor_speciality}")

                self.clear_previous_widgets()

                self.text_label = tk.Label(self.window, text=f"Doctor registered.")
                self.text_label.grid(row=0, column=0)
                self.text_label.config(fg= "green")

                self.new_go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
                self.new_go_home_button.grid(row=1, column=0)

    def view_doctor_action(self):
        self.clear_previous_widgets()
        self.window.title("View Doctors")
        self.window.geometry("415x400")

        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.text_label = tk.Label(self.frame, text="-----View Doctors-----")
        self.text_label.grid(row=0, column=0, columnspan=4)

        self.id_label = tk.Label(self.frame, text="ID")
        self.id_label.grid(row=1, column=0)

        self.fullname_label = tk.Label(self.frame, text="Full Name")
        self.fullname_label.grid(row=1, column=1)

        self.speciality_label = tk.Label(self.frame, text="Speciality")
        self.speciality_label.grid(row=1, column=2)

        for index, doctor in enumerate(self.doctors):
            id_entry = tk.Entry(self.frame, fg='blue')
            id_entry.grid(row=index+2, column=0)
            id_entry.insert(tk.END, index+1)

            fullname_entry = tk.Entry(self.frame, fg='blue')
            fullname_entry.grid(row=index+2, column=1)
            fullname_entry.insert(tk.END, doctor.full_name())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=2)
            speciality_entry.insert(tk.END, doctor.get_speciality())

        self.go_home_button = tk.Button(self.frame, text="Go To Home", command=self.home_window)
        self.go_home_button.grid(row=len(self.doctors)+2, column=0, columnspan=4)

        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def update_doctor_action(self):
        self.clear_previous_widgets()
        self.window.title("Update Doctors")
        self.window.geometry("600x400")

        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.text_label = tk.Label(self.frame, text="-----Update Doctors-----")
        self.text_label.grid(row=0, column=0, columnspan=4)

        self.id_label = tk.Label(self.frame, text="ID")
        self.id_label.grid(row=1, column=0)

        self.fullname_label = tk.Label(self.frame, text="Full Name")
        self.fullname_label.grid(row=1, column=1)

        self.speciality_label = tk.Label(self.frame, text="Speciality")
        self.speciality_label.grid(row=1, column=2)

        for index, doctor in enumerate(self.doctors):
            id_entry = tk.Entry(self.frame, fg='blue')
            id_entry.grid(row=index+2, column=0)
            id_entry.insert(tk.END, index+1)

            fullname_entry = tk.Entry(self.frame, fg='blue')
            fullname_entry.grid(row=index+2, column=1)
            fullname_entry.insert(tk.END, doctor.full_name())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=2)
            speciality_entry.insert(tk.END, doctor.get_speciality())

        self.user_given_doctor_id_label = tk.Label(self.frame, text="Enter the ID of the doctor:")
        self.user_given_doctor_id_label.grid(row=len(self.doctors)+2, column=0)

        self.user_given_doctor_id_entry = tk.Entry(self.frame, fg='black')
        self.user_given_doctor_id_entry.grid(row=len(self.doctors)+2, column=1, columnspan=3)

        self.go_home_button = tk.Button(self.frame, text="Enter", command=self.update_doctor_continue_button_action)
        self.go_home_button.grid(row=len(self.doctors)+3, column=0, columnspan=4)

        self.go_home_button = tk.Button(self.frame, text="Go To Home", command=self.home_window)
        self.go_home_button.grid(row=len(self.doctors)+4, column=0, columnspan=4)

        self.alert_variable = tk.StringVar()
        self.alert_variable.set("")
        self.alert_label = tk.Label(self.frame, textvariable=self.alert_variable)
        self.alert_label.grid(row=len(self.doctors)+5, column=0, columnspan=4)

        # self.make_window_responsive(5,2)

        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
        
    def update_doctor_continue_button_action(self):
        
        to_continue = False
        try:
            target_doctor_id = int(self.user_given_doctor_id_entry.get())-1
            doctor_index=self.admin.find_index(target_doctor_id,self.doctors)
            if doctor_index==False:
                self.alert_label.config(fg= "red")
                self.alert_variable.set("Doctor not found.")
            else:
                to_continue = True
        except:
            self.alert_label.config(fg= "red")
            self.alert_variable.set("The ID entered is incorrect.")

        if to_continue == True:
            self.clear_previous_widgets()
            self.window.title("Update Doctors")

            self.canvas = tk.Canvas(self.window)
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            self.frame = tk.Frame(self.canvas)
            self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

            self.text_label = tk.Label(self.frame, text="-----Update Doctors-----")
            self.text_label.grid(row=0, column=0, columnspan=4)

            self.id_label = tk.Label(self.frame, text="ID")
            self.id_label.grid(row=1, column=0)

            self.fullname_label = tk.Label(self.frame, text="Full Name")
            self.fullname_label.grid(row=1, column=1)

            self.speciality_label = tk.Label(self.frame, text="Speciality")
            self.speciality_label.grid(row=1, column=2)

            for index, doctor in enumerate(self.doctors):
                id_entry = tk.Entry(self.frame, fg='blue')
                id_entry.grid(row=index+2, column=0)
                id_entry.insert(tk.END, index+1)

                fullname_entry = tk.Entry(self.frame, fg='blue')
                fullname_entry.grid(row=index+2, column=1)
                fullname_entry.insert(tk.END, doctor.full_name())

                speciality_entry = tk.Entry(self.frame, fg='blue')
                speciality_entry.grid(row=index+2, column=2)
                speciality_entry.insert(tk.END, doctor.get_speciality())

            self.user_given_doctor_id_label = tk.Label(self.frame, text="Enter the ID of the doctor:")
            self.user_given_doctor_id_label.grid(row=len(self.doctors)+2, column=0)

            self.user_given_doctor_id_entry = tk.Entry(self.frame, fg='black')
            self.user_given_doctor_id_entry.grid(row=len(self.doctors)+2, column=1, columnspan=3)
            self.user_given_doctor_id_entry.insert(tk.END, str(target_doctor_id+1))

            self.user_direction_label = tk.Label(self.frame, text="Give new values to the field to be updated else leave it:")
            self.user_direction_label.grid(row=len(self.doctors)+3, column=0, columnspan=4)

            self.new_fname_label = tk.Label(self.frame, text="Enter new firstname:")
            self.new_fname_label.grid(row=len(self.doctors)+4, column=0)

            self.new_fname_entry = tk.Entry(self.frame)
            self.new_fname_entry.grid(row=len(self.doctors)+4, column=1, columnspan=3)

            self.new_lname_label = tk.Label(self.frame, text="Enter new surname:")
            self.new_lname_label.grid(row=len(self.doctors)+5, column=0)

            self.new_lname_entry = tk.Entry(self.frame)
            self.new_lname_entry.grid(row=len(self.doctors)+5, column=1, columnspan=3)

            self.new_speciality_label = tk.Label(self.frame, text="Enter new speciality:")
            self.new_speciality_label.grid(row=len(self.doctors)+6, column=0)

            self.new_speciality_entry = tk.Entry(self.frame)
            self.new_speciality_entry.grid(row=len(self.doctors)+6, column=1, columnspan=3)

            self.go_home_button = tk.Button(self.frame, text="Submit", command=self.update_doctor_detail_final_submit_button_action)
            self.go_home_button.grid(row=len(self.doctors)+7, column=0, columnspan=4)

            self.new_go_home_button = tk.Button(self.frame, text="Go To Home", command=self.home_window)
            self.new_go_home_button.grid(row=len(self.doctors)+8, column=0, columnspan=4)

            self.update_doctor_final_alert_variable = tk.StringVar()
            self.update_doctor_final_alert_variable.set("")
            self.update_doctor_final_alert_label = tk.Label(self.frame, textvariable=self.update_doctor_final_alert_variable)
            self.update_doctor_final_alert_label.grid(row=len(self.doctors)+9, column=0, columnspan=4)

            self.frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def update_doctor_detail_final_submit_button_action(self):
        target_doc_id = int(self.user_given_doctor_id_entry.get()) - 1

        new_doc_fname = self.new_fname_entry.get()
        new_doc_fname = new_doc_fname.title()

        new_doc_lname = self.new_lname_entry.get()
        new_doc_lname = new_doc_lname.title()

        new_doc_speciality = self.new_speciality_entry.get()
        new_doc_speciality = new_doc_speciality.title()

        if new_doc_fname == '' and new_doc_lname == '' and new_doc_speciality == '':
            self.clear_previous_widgets()

            self.text_label = tk.Label(self.window, text="No changes made.")
            self.text_label.grid(row=0, column=0)
            self.text_label.config(fg= "green")

            self.new_go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
            self.new_go_home_button.grid(row=1, column=0)
        
        else:
            if new_doc_fname != '':
                previous_name = self.doctors[target_doc_id].full_name()
                self.admin.modify_database_content("./data/doctors.txt", f"{self.doctors[target_doc_id].get_first_name()}, {self.doctors[target_doc_id].get_surname()}", f"{new_doc_fname}, {self.doctors[target_doc_id].get_surname()}") # Changing in the database
                self.doctors[target_doc_id].set_first_name(new_doc_fname) # Updating the last name in the object

            if new_doc_lname != '':
                previous_name = self.doctors[target_doc_id].full_name()
                self.admin.modify_database_content("./data/doctors.txt", f"{self.doctors[target_doc_id].get_first_name()}, {self.doctors[target_doc_id].get_surname()}", f"{self.doctors[target_doc_id].get_first_name()}, {new_doc_lname}") # Changing in the database
                self.doctors[target_doc_id].set_surname(new_doc_lname) # Updating the last name in the object

            if new_doc_speciality:
                previous_speciality = self.doctors[target_doc_id].get_speciality()
                self.admin.modify_database_content("./data/doctors.txt", f"{self.doctors[target_doc_id].get_surname()}, {self.doctors[target_doc_id].get_speciality()}", f"{self.doctors[target_doc_id].get_surname()}, {new_doc_speciality}") # Changing in the database
                self.doctors[target_doc_id].set_speciality(new_doc_speciality) # Updating the first name in the object


            self.clear_previous_widgets()

            self.text_label = tk.Label(self.window, text=f"Changes Made.")
            self.text_label.grid(row=0, column=0)
            self.text_label.config(fg= "green")

            self.new_go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
            self.new_go_home_button.grid(row=1, column=0)

    def delete_doctor_action(self):
        self.clear_previous_widgets()
        self.window.title("Delete Doctors")
        self.window.geometry("400x400")

        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.text_label = tk.Label(self.frame, text="-----Delete Doctors-----")
        self.text_label.grid(row=0, column=0, columnspan=4)

        self.id_label = tk.Label(self.frame, text="ID")
        self.id_label.grid(row=1, column=0)

        self.fullname_label = tk.Label(self.frame, text="Full Name")
        self.fullname_label.grid(row=1, column=1)

        self.speciality_label = tk.Label(self.frame, text="Speciality")
        self.speciality_label.grid(row=1, column=2)

        for index, doctor in enumerate(self.doctors):
            id_entry = tk.Entry(self.frame, fg='blue')
            id_entry.grid(row=index+2, column=0)
            id_entry.insert(tk.END, index+1)

            fullname_entry = tk.Entry(self.frame, fg='blue')
            fullname_entry.grid(row=index+2, column=1)
            fullname_entry.insert(tk.END, doctor.full_name())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=2)
            speciality_entry.insert(tk.END, doctor.get_speciality())

        self.user_given_doctor_id_label = tk.Label(self.frame, text="Enter the ID of the doctor to remove:")
        self.user_given_doctor_id_label.grid(row=len(self.doctors)+2, column=0, columnspan=2)

        self.user_given_doctor_id_entry = tk.Entry(self.frame, fg='black')
        self.user_given_doctor_id_entry.grid(row=len(self.doctors)+2, column=2)

        self.go_home_button = tk.Button(self.frame, text="Delete", command=self.delete_doctor_button_final_action)
        self.go_home_button.grid(row=len(self.doctors)+3, column=0, columnspan=4)

        self.go_home_button = tk.Button(self.frame, text="Go To Home", command=self.home_window)
        self.go_home_button.grid(row=len(self.doctors)+4, column=0, columnspan=4)

        self.alert_variable = tk.StringVar()
        self.alert_variable.set("")
        self.alert_label = tk.Label(self.frame, textvariable=self.alert_variable)
        self.alert_label.grid(row=len(self.doctors)+5, column=0, columnspan=4)

        self.make_window_responsive(5,2)

        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def delete_doctor_button_final_action(self):
        to_continue = False
        try:
            target_doctor_id = int(self.user_given_doctor_id_entry.get())-1
            doctor_index=self.admin.find_index(target_doctor_id,self.doctors)
            if doctor_index==False:
                self.alert_label.config(fg= "red")
                self.alert_variable.set("Doctor not found.")
            else:
                to_continue = True
        except:
            self.alert_label.config(fg= "red")
            self.alert_variable.set("The ID entered is incorrect.")

        if to_continue == True:
            to_removed_doctor = self.doctors[target_doctor_id]
            doctor_file = open("./data/doctors.txt", 'r')
            modified_lines = []
            for line in doctor_file:
                if f"{to_removed_doctor.get_first_name()}, {to_removed_doctor.get_surname()}, {to_removed_doctor.get_speciality()}" in line:
                    pass
                else:
                    modified_lines.append(line)
            doctor_file.close()

            doctor_file = open("./data/doctors.txt", 'w')
            for line in modified_lines:
                doctor_file.write(line)
            doctor_file.close()

            removed_doc = self.doctors.pop(target_doctor_id)
            
            self.clear_previous_widgets()

            self.text_label = tk.Label(self.window, text=f"Doctor {removed_doc.full_name()} deleted.")
            self.text_label.grid(row=0, column=0)
            self.text_label.config(fg= "green")

            self.new_go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
            self.new_go_home_button.grid(row=1, column=0)
    



















    def add_patient_action(self):
        self.clear_previous_widgets()
        self.window.title("Add a patient")

        self.text_label = tk.Label(self.window, text="-----Add a patient-----")
        self.text_label.grid(row=0, column=0, columnspan=3)

        self.fname_label = tk.Label(self.window, text="Enter the first name:")
        self.fname_label.grid(row=1, column=0)

        self.fname_entry = tk.Entry(self.window)
        self.fname_entry.grid(row=1, column=1)

        self.lname_label = tk.Label(self.window, text="Enter the surname:")
        self.lname_label.grid(row=2, column=0)

        self.lname_entry = tk.Entry(self.window)
        self.lname_entry.grid(row=2, column=1)

        self.age_label = tk.Label(self.window, text="Enter age:")
        self.age_label.grid(row=3, column=0)

        self.age_entry = tk.Entry(self.window)
        self.age_entry.grid(row=3, column=1)

        self.phone_number_label = tk.Label(self.window, text="Enter phone number:")
        self.phone_number_label.grid(row=4, column=0)

        self.phone_number_entry = tk.Entry(self.window)
        self.phone_number_entry.grid(row=4, column=1)

        self.address_label = tk.Label(self.window, text="Enter postcode (Address):")
        self.address_label.grid(row=5, column=0)

        self.address_entry = tk.Entry(self.window)
        self.address_entry.grid(row=5, column=1)

        self.symptoms_label = tk.Label(self.window, text="Enter symptoms seperated by commas ',':")
        self.symptoms_label.grid(row=6, column=0)

        self.symptoms_entry = tk.Entry(self.window)
        self.symptoms_entry.grid(row=6, column=1)

        self.submit_add_patient_details_button = tk.Button(self.window, text="Submit", command=self.submit_add_patient_details_button_action)
        self.submit_add_patient_details_button.grid(row=7, column=0, columnspan=3)

        self.go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
        self.go_home_button.grid(row=8, column=0, columnspan=3)

        self.alert_variable = tk.StringVar()
        self.alert_variable.set("")
        self.alert_label = tk.Label(self.window, textvariable=self.alert_variable)
        self.alert_label.grid(row=9, column=0, columnspan=3)

        self.make_window_responsive(10,2)

    def submit_add_patient_details_button_action(self):
        new_patient_f_name = self.fname_entry.get()
        new_patient_l_name = self.lname_entry.get()
        new_patient_age = self.age_entry.get()
        new_patient_pone_number = self.phone_number_entry.get()
        new_patient_postcode = self.address_entry.get()

        new_patient_symptoms = self.symptoms_entry.get()

        try:
            new_patient_symptoms = new_patient_symptoms.split(",")
            new_patient_symptoms = [each.strip() for each in new_patient_symptoms]
            new_patient_symptoms = [each.title() for each in new_patient_symptoms if each.isspace() == False]

            new_patient_symptoms_in_str_form = ""
            for n, i in enumerate(new_patient_symptoms):
                if n == 0:
                    new_patient_symptoms_in_str_form += i
                else:
                    new_patient_symptoms_in_str_form += f"+{i}"
        except:
            new_patient_symptoms = new_patient_symptoms.strip()

        # Checking for invalid input
        if new_patient_f_name.isspace() == True or new_patient_f_name == '' or new_patient_l_name.isspace() == True or new_patient_l_name == '' or new_patient_age.isspace() == True or new_patient_age == '' or new_patient_pone_number.isspace() == True or new_patient_pone_number == ''  or new_patient_postcode.isspace() == True or new_patient_postcode == '':
            self.alert_label.config(fg= "red")
            self.alert_variable.set("Please give a valid input - Not empty strings or spaces.")
        # if valid input
        else:
            new_patient_object = Patient(new_patient_f_name, new_patient_l_name, new_patient_age, new_patient_pone_number, new_patient_postcode, new_patient_symptoms)
            self.patients.append(new_patient_object)

            self.admin.add_entry_to_database("./data/patients.txt", f"{new_patient_f_name}, {new_patient_l_name}, {new_patient_age}, {new_patient_pone_number}, {new_patient_postcode}, {new_patient_symptoms_in_str_form}")

            self.clear_previous_widgets()

            self.text_label = tk.Label(self.window, text=f"Patient {new_patient_f_name} {new_patient_l_name} added successfully.")
            self.text_label.grid(row=0, column=0)
            self.text_label.config(fg= "green")

            self.new_go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
            self.new_go_home_button.grid(row=1, column=0)














    def view_or_discharge_patient_action(self):
        self.clear_previous_widgets()
        self.window.title("View and Discharge Patients")
        self.window.geometry("800x600")

        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.text_label = tk.Label(self.frame, text="-----View Patients-----")
        self.text_label.grid(row=0, column=0, columnspan=4)

        self.id_label = tk.Label(self.frame, text="ID")
        self.id_label.grid(row=1, column=0)

        self.fullname_label = tk.Label(self.frame, text="Full Name")
        self.fullname_label.grid(row=1, column=1)

        self.speciality_label = tk.Label(self.frame, text="Doctor's Full Name")
        self.speciality_label.grid(row=1, column=2)

        self.speciality_label = tk.Label(self.frame, text="Age")
        self.speciality_label.grid(row=1, column=3)

        self.speciality_label = tk.Label(self.frame, text="Mobile")
        self.speciality_label.grid(row=1, column=4)

        self.speciality_label = tk.Label(self.frame, text="Postcode")
        self.speciality_label.grid(row=1, column=5)

        for index, patient in enumerate(self.patients):
            id_entry = tk.Entry(self.frame, fg='blue')
            id_entry.grid(row=index+2, column=0)
            id_entry.insert(tk.END, index+1)

            fullname_entry = tk.Entry(self.frame, fg='blue')
            fullname_entry.grid(row=index+2, column=1)
            fullname_entry.insert(tk.END, patient.full_name())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=2)
            speciality_entry.insert(tk.END, patient.get_doctor())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=3)
            speciality_entry.insert(tk.END, patient.get_age())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=4)
            speciality_entry.insert(tk.END, patient.get_mobile())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=5)
            speciality_entry.insert(tk.END, patient.get_postcode())

        self.user_given_patient_id_label = tk.Label(self.frame, text="Enter the ID of the patient:")
        self.user_given_patient_id_label.grid(row=len(self.patients)+2, column=0, columnspan=2)

        self.user_given_patient_id_entry = tk.Entry(self.frame, fg='black')
        self.user_given_patient_id_entry.grid(row=len(self.patients)+2, column=2, columnspan=4)

        self.discharge_patient_continue_button = tk.Button(self.frame, text="Enter", command=self.discharge_patient_continue_button_action)
        self.discharge_patient_continue_button.grid(row=len(self.patients)+3, column=0, columnspan=7)

        self.go_home_button = tk.Button(self.frame, text="Go To Home", command=self.home_window)
        self.go_home_button.grid(row=len(self.patients)+4, column=0, columnspan=7)

        self.alert_variable = tk.StringVar()
        self.alert_variable.set("")
        self.alert_label = tk.Label(self.frame, textvariable=self.alert_variable)
        self.alert_label.grid(row=len(self.patients)+5, column=0, columnspan=7)

        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))
    

    def discharge_patient_continue_button_action(self):
        to_continue = False
        try:
            target_patient_id = int(self.user_given_patient_id_entry.get())-1
            doctor_index=self.admin.find_index(target_patient_id,self.patients)
            if doctor_index==False:
                self.alert_label.config(fg= "red")
                self.alert_variable.set("Patient not found.")
            else:
                to_continue = True
        except:
            self.alert_label.config(fg= "red")
            self.alert_variable.set("The ID entered is incorrect.")

        if to_continue == True:
            discharged_patient = self.patients[target_patient_id]

            self.discharged_patients.append(discharged_patient)

            self.patients.pop(target_patient_id)

            self.clear_previous_widgets()

            self.text_label = tk.Label(self.window, text=f"Patient {discharged_patient.full_name()} is discharged.")
            self.text_label.grid(row=0, column=0)
            self.text_label.config(fg= "green")

            self.new_go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
            self.new_go_home_button.grid(row=1, column=0)
            















    def view_discharged_patient(self):
        self.clear_previous_widgets()
        self.window.title("Discharged Patients")
        self.window.geometry("600x400")

        if len(self.discharged_patients) == 0:
            self.text_label = tk.Label(self.window, text=f"No patient is discharged yet.")
            self.text_label.grid(row=0, column=0)
            self.text_label.config(fg= "green")

            self.new_go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
            self.new_go_home_button.grid(row=1, column=0)
        else:
            self.canvas = tk.Canvas(self.window)
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            self.frame = tk.Frame(self.canvas)
            self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

            self.text_label = tk.Label(self.frame, text="-----View Discharged Patients-----")
            self.text_label.grid(row=0, column=0, columnspan=4)

            self.id_label = tk.Label(self.frame, text="ID")
            self.id_label.grid(row=1, column=0)

            self.fullname_label = tk.Label(self.frame, text="Full Name")
            self.fullname_label.grid(row=1, column=1)

            self.speciality_label = tk.Label(self.frame, text="Doctor's Full Name")
            self.speciality_label.grid(row=1, column=2)

            self.speciality_label = tk.Label(self.frame, text="Age")
            self.speciality_label.grid(row=1, column=3)

            self.speciality_label = tk.Label(self.frame, text="Mobile")
            self.speciality_label.grid(row=1, column=4)

            self.speciality_label = tk.Label(self.frame, text="Postcode")
            self.speciality_label.grid(row=1, column=5)

            for index, patient in enumerate(self.discharged_patients):
                id_entry = tk.Entry(self.frame, fg='blue')
                id_entry.grid(row=index+2, column=0)
                id_entry.insert(tk.END, index+1)

                fullname_entry = tk.Entry(self.frame, fg='blue')
                fullname_entry.grid(row=index+2, column=1)
                fullname_entry.insert(tk.END, patient.full_name())

                speciality_entry = tk.Entry(self.frame, fg='blue')
                speciality_entry.grid(row=index+2, column=2)
                speciality_entry.insert(tk.END, patient.get_doctor())

                speciality_entry = tk.Entry(self.frame, fg='blue')
                speciality_entry.grid(row=index+2, column=3)
                speciality_entry.insert(tk.END, patient.get_age())

                speciality_entry = tk.Entry(self.frame, fg='blue')
                speciality_entry.grid(row=index+2, column=4)
                speciality_entry.insert(tk.END, patient.get_mobile())

                speciality_entry = tk.Entry(self.frame, fg='blue')
                speciality_entry.grid(row=index+2, column=5)
                speciality_entry.insert(tk.END, patient.get_postcode())

            self.go_home_button = tk.Button(self.frame, text="Go To Home", command=self.home_window)
            self.go_home_button.grid(row=len(self.patients)+2, column=0, columnspan=7)

            self.frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))











    def appointment_management_action(self):
        self.clear_previous_widgets()
        self.window.title("Appointment Management")
        self.window.geometry("300x300")

        self.text_label = tk.Label(self.window, text="-----Appointment Management-----")
        self.text_label.grid(row=0, column=0)

        self.book_appointment_button = tk.Button(self.window, text="Book an appointment", command=self.book_appointment_button_action)
        self.book_appointment_button.grid(row=1, column=0)

        self.check_appointment_status_button = tk.Button(self.window, text="Check appointment status", command=self.check_appointment_status_button)
        self.check_appointment_status_button.grid(row=2, column=0)

        self.make_window_responsive(3,1)
    
    def book_appointment_button_action(self):
        self.clear_previous_widgets()
        self.window.title("Book an appointment")
        self.window.geometry("800x600")

        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.text_label = tk.Label(self.frame, text="-----Choose Patient-----")
        self.text_label.grid(row=0, column=0, columnspan=4)

        self.id_label = tk.Label(self.frame, text="ID")
        self.id_label.grid(row=1, column=0)

        self.fullname_label = tk.Label(self.frame, text="Full Name")
        self.fullname_label.grid(row=1, column=1)

        self.speciality_label = tk.Label(self.frame, text="Doctor's Full Name")
        self.speciality_label.grid(row=1, column=2)

        self.speciality_label = tk.Label(self.frame, text="Age")
        self.speciality_label.grid(row=1, column=3)

        self.speciality_label = tk.Label(self.frame, text="Mobile")
        self.speciality_label.grid(row=1, column=4)

        self.speciality_label = tk.Label(self.frame, text="Postcode")
        self.speciality_label.grid(row=1, column=5)

        for index, patient in enumerate(self.patients):
            id_entry = tk.Entry(self.frame, fg='blue')
            id_entry.grid(row=index+2, column=0)
            id_entry.insert(tk.END, index+1)

            fullname_entry = tk.Entry(self.frame, fg='blue')
            fullname_entry.grid(row=index+2, column=1)
            fullname_entry.insert(tk.END, patient.full_name())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=2)
            speciality_entry.insert(tk.END, patient.get_doctor())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=3)
            speciality_entry.insert(tk.END, patient.get_age())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=4)
            speciality_entry.insert(tk.END, patient.get_mobile())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=5)
            speciality_entry.insert(tk.END, patient.get_postcode())

        self.user_given_patient_id_label = tk.Label(self.frame, text="Enter the ID of the patient:")
        self.user_given_patient_id_label.grid(row=len(self.patients)+2, column=0, columnspan=2)

        self.user_given_patient_id_entry = tk.Entry(self.frame, fg='black')
        self.user_given_patient_id_entry.grid(row=len(self.patients)+2, column=2, columnspan=4)

        self.give_patient_continue_button = tk.Button(self.frame, text="Enter", command=self.give_patient_continue_button_action)
        self.give_patient_continue_button.grid(row=len(self.patients)+3, column=0, columnspan=7)

        self.go_home_button = tk.Button(self.frame, text="Go To Home", command=self.home_window)
        self.go_home_button.grid(row=len(self.patients)+4, column=0, columnspan=7)

        self.alert_variable = tk.StringVar()
        self.alert_variable.set("")
        self.alert_label = tk.Label(self.frame, textvariable=self.alert_variable)
        self.alert_label.grid(row=len(self.patients)+5, column=0, columnspan=7)

        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def give_patient_continue_button_action(self):
        to_continue = False
        try:
            target_patient_id = int(self.user_given_patient_id_entry.get())-1
            doctor_index=self.admin.find_index(target_patient_id,self.patients)
            if doctor_index==False:
                self.alert_label.config(fg= "red")
                self.alert_variable.set("Patient not found.")
            else:
                to_continue = True
                self.__intermediate_variable = target_patient_id
        except:
            self.alert_label.config(fg= "red")
            self.alert_variable.set("The ID entered is incorrect.")

        if to_continue == True:
            target_patient_object = self.patients[target_patient_id]

            self.clear_previous_widgets()
            self.window.title("Book an appointment")
            self.window.geometry("400x400")

            self.canvas = tk.Canvas(self.window)
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            self.frame = tk.Frame(self.canvas)
            self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

            self.text_label = tk.Label(self.frame, text="-----Choose Doctor-----")
            self.text_label.grid(row=0, column=0, columnspan=4)

            self.id_label = tk.Label(self.frame, text="ID")
            self.id_label.grid(row=1, column=0)

            self.fullname_label = tk.Label(self.frame, text="Full Name")
            self.fullname_label.grid(row=1, column=1)

            self.speciality_label = tk.Label(self.frame, text="Speciality")
            self.speciality_label.grid(row=1, column=2)

            for index, doctor in enumerate(self.doctors):
                id_entry = tk.Entry(self.frame, fg='blue')
                id_entry.grid(row=index+2, column=0)
                id_entry.insert(tk.END, index+1)

                fullname_entry = tk.Entry(self.frame, fg='blue')
                fullname_entry.grid(row=index+2, column=1)
                fullname_entry.insert(tk.END, doctor.full_name())

                speciality_entry = tk.Entry(self.frame, fg='blue')
                speciality_entry.grid(row=index+2, column=2)
                speciality_entry.insert(tk.END, doctor.get_speciality())

            self.user_given_doctor_id_label = tk.Label(self.frame, text="Enter the ID of the doctor:")
            self.user_given_doctor_id_label.grid(row=len(self.doctors)+2, column=0)

            self.user_given_doctor_id_entry = tk.Entry(self.frame, fg='black')
            self.user_given_doctor_id_entry.grid(row=len(self.doctors)+2, column=1, columnspan=3)

            self.doctor_id_submit_button = tk.Button(self.frame, text="Enter", command=self.given_doctor_id_submit_button_action)
            self.doctor_id_submit_button.grid(row=len(self.doctors)+3, column=0, columnspan=4)

            self.go_home_button = tk.Button(self.frame, text="Go To Home", command=self.home_window)
            self.go_home_button.grid(row=len(self.doctors)+4, column=0, columnspan=4)

            self.alert_variable = tk.StringVar()
            self.alert_variable.set("")
            self.alert_label = tk.Label(self.frame, textvariable=self.alert_variable)
            self.alert_label.grid(row=len(self.doctors)+5, column=0, columnspan=4)

            self.frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def given_doctor_id_submit_button_action(self):
        to_continue = False
        try:
            target_doctor_id = int(self.user_given_doctor_id_entry.get())-1
            doctor_index=self.admin.find_index(target_doctor_id,self.doctors)
            if doctor_index==False:
                self.alert_label.config(fg= "red")
                self.alert_variable.set("Doctor not found.")
            else:
                to_continue = True
        except:
            self.alert_label.config(fg= "red")
            self.alert_variable.set("The ID entered is incorrect.")

        if to_continue == True:
            target_patient_object = self.patients[self.__intermediate_variable]
            target_doctor_object = self.doctors[target_doctor_id]
            
            target_patient_object.add_to_appointments_made(target_doctor_object)
            target_doctor_object.add_appointment(target_patient_object)

            self.clear_previous_widgets()

            self.text_label = tk.Label(self.window, text=f"Appointment booked. You can check your appointment status.")
            self.text_label.grid(row=0, column=0)
            self.text_label.config(fg= "green")

            self.new_go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
            self.new_go_home_button.grid(row=1, column=0)

    def check_appointment_status_button(self):
        self.clear_previous_widgets()
        self.window.title("Check an appointment")
        self.window.geometry("800x600")

        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.text_label = tk.Label(self.frame, text="-----Choose Patient-----")
        self.text_label.grid(row=0, column=0, columnspan=4)

        self.id_label = tk.Label(self.frame, text="ID")
        self.id_label.grid(row=1, column=0)

        self.fullname_label = tk.Label(self.frame, text="Full Name")
        self.fullname_label.grid(row=1, column=1)

        self.speciality_label = tk.Label(self.frame, text="Doctor's Full Name")
        self.speciality_label.grid(row=1, column=2)

        self.speciality_label = tk.Label(self.frame, text="Age")
        self.speciality_label.grid(row=1, column=3)

        self.speciality_label = tk.Label(self.frame, text="Mobile")
        self.speciality_label.grid(row=1, column=4)

        self.speciality_label = tk.Label(self.frame, text="Postcode")
        self.speciality_label.grid(row=1, column=5)

        for index, patient in enumerate(self.patients):
            id_entry = tk.Entry(self.frame, fg='blue')
            id_entry.grid(row=index+2, column=0)
            id_entry.insert(tk.END, index+1)

            fullname_entry = tk.Entry(self.frame, fg='blue')
            fullname_entry.grid(row=index+2, column=1)
            fullname_entry.insert(tk.END, patient.full_name())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=2)
            speciality_entry.insert(tk.END, patient.get_doctor())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=3)
            speciality_entry.insert(tk.END, patient.get_age())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=4)
            speciality_entry.insert(tk.END, patient.get_mobile())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=5)
            speciality_entry.insert(tk.END, patient.get_postcode())

        self.user_given_patient_id_label = tk.Label(self.frame, text="Enter the ID of the patient:")
        self.user_given_patient_id_label.grid(row=len(self.patients)+2, column=0, columnspan=2)

        self.user_given_patient_id_entry = tk.Entry(self.frame, fg='black')
        self.user_given_patient_id_entry.grid(row=len(self.patients)+2, column=2, columnspan=4)

        self.give_patient_continue_button = tk.Button(self.frame, text="Enter", command=self.given_check_appointment_patient_continue_button_action)
        self.give_patient_continue_button.grid(row=len(self.patients)+3, column=0, columnspan=7)

        self.go_home_button = tk.Button(self.frame, text="Go To Home", command=self.home_window)
        self.go_home_button.grid(row=len(self.patients)+4, column=0, columnspan=7)

        self.alert_variable = tk.StringVar()
        self.alert_variable.set("")
        self.alert_label = tk.Label(self.frame, textvariable=self.alert_variable)
        self.alert_label.grid(row=len(self.patients)+5, column=0, columnspan=7)

        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def given_check_appointment_patient_continue_button_action(self):
        to_continue = False
        try:
            target_patient_id = int(self.user_given_patient_id_entry.get())-1
            doctor_index=self.admin.find_index(target_patient_id,self.patients)
            if doctor_index==False:
                self.alert_label.config(fg= "red")
                self.alert_variable.set("Patient not found.")
            else:
                to_continue = True
                self.__intermediate_variable = target_patient_id
        except:
            self.alert_label.config(fg= "red")
            self.alert_variable.set("The ID entered is incorrect.")

        if to_continue == True:
            target_patient_object = self.patients[target_patient_id]

            appointments_made = target_patient_object.get_appointments_made()

            if len(appointments_made) == 0:
                self.clear_previous_widgets()

                self.text_label = tk.Label(self.window, text=f"{target_patient_object.full_name()} hasn't booked any appointments. Book an appointment first.")
                self.text_label.grid(row=0, column=0)
                self.text_label.config(fg= "red")

                self.new_go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
                self.new_go_home_button.grid(row=1, column=0)
            else:
                self.clear_previous_widgets()
                self.window.title("Appointment Status")

                self.canvas = tk.Canvas(self.window)
                self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

                self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
                self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

                self.canvas.configure(yscrollcommand=self.scrollbar.set)

                self.frame = tk.Frame(self.canvas)
                self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

                self.text_label = tk.Label(self.frame, text="-----Appointment Status-----")
                self.text_label.grid(row=0, column=0, columnspan=4)

                self.id_label = tk.Label(self.frame, text="S.No.")
                self.id_label.grid(row=1, column=0)

                self.fullname_label = tk.Label(self.frame, text="Appointments")
                self.fullname_label.grid(row=1, column=1)

                self.speciality_label = tk.Label(self.frame, text="Status")
                self.speciality_label.grid(row=1, column=2)
                
                for index, doctor in enumerate(appointments_made):
                    if selected_patient.get_doctor() == 'None':
                        id_entry = tk.Entry(self.frame, fg='blue')
                        id_entry.grid(row=index+2, column=0)
                        id_entry.insert(tk.END, index+1)

                        fullname_entry = tk.Entry(self.frame, fg='blue')
                        fullname_entry.grid(row=index+2, column=1)
                        fullname_entry.insert(tk.END, f"Appointment with {doctor.full_name()}")

                        speciality_entry = tk.Entry(self.frame, fg='blue')
                        speciality_entry.grid(row=index+2, column=2)
                        speciality_entry.insert(tk.END, "Pending")

                    elif selected_patient.get_doctor() == doctor.full_name():
                        id_entry = tk.Entry(self.frame, fg='blue')
                        id_entry.grid(row=index+2, column=0)
                        id_entry.insert(tk.END, index+1)

                        fullname_entry = tk.Entry(self.frame, fg='blue')
                        fullname_entry.grid(row=index+2, column=1)
                        fullname_entry.insert(tk.END, f"Appointment with {doctor.full_name()}")

                        speciality_entry = tk.Entry(self.frame, fg='blue')
                        speciality_entry.grid(row=index+2, column=2)
                        speciality_entry.insert(tk.END, "Approved")
                    else:
                        id_entry = tk.Entry(self.frame, fg='blue')
                        id_entry.grid(row=index+2, column=0)
                        id_entry.insert(tk.END, index+1)

                        fullname_entry = tk.Entry(self.frame, fg='blue')
                        fullname_entry.grid(row=index+2, column=1)
                        fullname_entry.insert(tk.END, f"Appointment with {doctor.full_name()}")

                        speciality_entry = tk.Entry(self.frame, fg='blue')
                        speciality_entry.grid(row=index+2, column=2)
                        speciality_entry.insert(tk.END, "Pending")




    def assign_doctor_to_patient_action(self):
        self.clear_previous_widgets()
        self.window.title("Assign Patient to a doctor")
        self.window.geometry("800x600")

        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

        self.text_label = tk.Label(self.frame, text="-----View Patients-----")
        self.text_label.grid(row=0, column=0, columnspan=4)

        self.id_label = tk.Label(self.frame, text="ID")
        self.id_label.grid(row=1, column=0)

        self.fullname_label = tk.Label(self.frame, text="Full Name")
        self.fullname_label.grid(row=1, column=1)

        self.speciality_label = tk.Label(self.frame, text="Doctor's Full Name")
        self.speciality_label.grid(row=1, column=2)

        self.speciality_label = tk.Label(self.frame, text="Age")
        self.speciality_label.grid(row=1, column=3)

        self.speciality_label = tk.Label(self.frame, text="Mobile")
        self.speciality_label.grid(row=1, column=4)

        self.speciality_label = tk.Label(self.frame, text="Postcode")
        self.speciality_label.grid(row=1, column=5)

        for index, patient in enumerate(self.patients):
            id_entry = tk.Entry(self.frame, fg='blue')
            id_entry.grid(row=index+2, column=0)
            id_entry.insert(tk.END, index+1)

            fullname_entry = tk.Entry(self.frame, fg='blue')
            fullname_entry.grid(row=index+2, column=1)
            fullname_entry.insert(tk.END, patient.full_name())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=2)
            speciality_entry.insert(tk.END, patient.get_doctor())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=3)
            speciality_entry.insert(tk.END, patient.get_age())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=4)
            speciality_entry.insert(tk.END, patient.get_mobile())

            speciality_entry = tk.Entry(self.frame, fg='blue')
            speciality_entry.grid(row=index+2, column=5)
            speciality_entry.insert(tk.END, patient.get_postcode())

        self.user_given_patient_id_label = tk.Label(self.frame, text="Enter the ID of the patient:")
        self.user_given_patient_id_label.grid(row=len(self.patients)+2, column=0, columnspan=2)

        self.user_given_patient_id_entry = tk.Entry(self.frame, fg='black')
        self.user_given_patient_id_entry.grid(row=len(self.patients)+2, column=2, columnspan=4)

        self.target_patient_continue_button = tk.Button(self.frame, text="Enter", command=self.target_patient_continue_button_action)
        self.target_patient_continue_button.grid(row=len(self.patients)+3, column=0, columnspan=7)

        self.go_home_button = tk.Button(self.frame, text="Go To Home", command=self.home_window)
        self.go_home_button.grid(row=len(self.patients)+4, column=0, columnspan=7)

        self.alert_variable = tk.StringVar()
        self.alert_variable.set("")
        self.alert_label = tk.Label(self.frame, textvariable=self.alert_variable)
        self.alert_label.grid(row=len(self.patients)+5, column=0, columnspan=7)

        self.frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def target_patient_continue_button_action(self):
        to_continue = False
        try:
            target_patient_id = int(self.user_given_patient_id_entry.get())-1
            doctor_index=self.admin.find_index(target_patient_id,self.patients)
            if doctor_index==False:
                self.alert_label.config(fg= "red")
                self.alert_variable.set("Patient not found.")
            else:
                to_continue = True
                self.__intermediate_variable = target_patient_id
        except:
            self.alert_label.config(fg= "red")
            self.alert_variable.set("The ID entered is incorrect.")

        if to_continue == True:
            target_patient_object = self.patients[target_patient_id]

            self.clear_previous_widgets()
            self.window.title("Book an appointment")
            self.window.geometry("400x400")

            self.canvas = tk.Canvas(self.window)
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            self.frame = tk.Frame(self.canvas)
            self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

            self.text_label = tk.Label(self.frame, text="-----Choose Doctor-----")
            self.text_label.grid(row=0, column=0, columnspan=4)

            self.id_label = tk.Label(self.frame, text="ID")
            self.id_label.grid(row=1, column=0)

            self.fullname_label = tk.Label(self.frame, text="Full Name")
            self.fullname_label.grid(row=1, column=1)

            self.speciality_label = tk.Label(self.frame, text="Speciality")
            self.speciality_label.grid(row=1, column=2)

            for index, doctor in enumerate(self.doctors):
                id_entry = tk.Entry(self.frame, fg='blue')
                id_entry.grid(row=index+2, column=0)
                id_entry.insert(tk.END, index+1)

                fullname_entry = tk.Entry(self.frame, fg='blue')
                fullname_entry.grid(row=index+2, column=1)
                fullname_entry.insert(tk.END, doctor.full_name())

                speciality_entry = tk.Entry(self.frame, fg='blue')
                speciality_entry.grid(row=index+2, column=2)
                speciality_entry.insert(tk.END, doctor.get_speciality())

            self.user_given_doctor_id_label = tk.Label(self.frame, text="Enter the ID of the doctor:")
            self.user_given_doctor_id_label.grid(row=len(self.doctors)+2, column=0)

            self.user_given_doctor_id_entry = tk.Entry(self.frame, fg='black')
            self.user_given_doctor_id_entry.grid(row=len(self.doctors)+2, column=1, columnspan=3)

            self.doctor_id_submit_button = tk.Button(self.frame, text="Enter", command=self.assign_doctor_given_doctor_id_submit_button_action)
            self.doctor_id_submit_button.grid(row=len(self.doctors)+3, column=0, columnspan=4)

            self.go_home_button = tk.Button(self.frame, text="Go To Home", command=self.home_window)
            self.go_home_button.grid(row=len(self.doctors)+4, column=0, columnspan=4)

            self.alert_variable = tk.StringVar()
            self.alert_variable.set("")
            self.alert_label = tk.Label(self.frame, textvariable=self.alert_variable)
            self.alert_label.grid(row=len(self.doctors)+5, column=0, columnspan=4)

            self.frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def assign_doctor_given_doctor_id_submit_button_action(self):
        to_continue = False
        try:
            target_doctor_id = int(self.user_given_doctor_id_entry.get())-1
            doctor_index=self.admin.find_index(target_doctor_id,self.doctors)
            if doctor_index==False:
                self.alert_label.config(fg= "red")
                self.alert_variable.set("Doctor not found.")
            else:
                to_continue = True
        except:
            self.alert_label.config(fg= "red")
            self.alert_variable.set("The ID entered is incorrect.")

        if to_continue == True:
            target_patient_object = self.patients[self.__intermediate_variable]
            target_doctor_object = self.doctors[target_doctor_id]
            
            target_doctor_object.add_patient(target_patient_object) # Assigining the patient to the doctor 
            target_patient_object.link(target_doctor_object.full_name()) # Linking the doctor to the patient
                

            self.clear_previous_widgets()

            self.text_label = tk.Label(self.window, text=f"Patient {target_patient_object.full_name()} is assigned to {target_doctor_object.full_name()}.")
            self.text_label.grid(row=0, column=0)
            self.text_label.config(fg= "green")

            self.new_go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
            self.new_go_home_button.grid(row=1, column=0)






    def relocate_patient_to_another_doctor_action(self):
        patients = [each for each in self.patients if each.get_doctor() != 'None']

        if len(patients) == 0:
            self.clear_previous_widgets()
            self.window.geometry("400x400")
            self.window.title("Relocate Patient to another doctor")

            self.text_label = tk.Label(self.window, text=f"No patient assigned to any doctors! Assign a doctor to a patient first.")
            self.text_label.grid(row=0, column=0)
            self.text_label.config(fg= "red")

            self.new_go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
            self.new_go_home_button.grid(row=1, column=0)
        
        else:
            self.clear_previous_widgets()
            self.window.title("Relocate Patient to another doctor")
            self.window.geometry("800x600")

            self.canvas = tk.Canvas(self.window)
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            self.frame = tk.Frame(self.canvas)
            self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

            self.text_label = tk.Label(self.frame, text="-----Doctor Assigned Patients-----")
            self.text_label.grid(row=0, column=0, columnspan=4)

            self.id_label = tk.Label(self.frame, text="ID")
            self.id_label.grid(row=1, column=0)

            self.fullname_label = tk.Label(self.frame, text="Full Name")
            self.fullname_label.grid(row=1, column=1)

            self.speciality_label = tk.Label(self.frame, text="Doctor's Full Name")
            self.speciality_label.grid(row=1, column=2)

            self.speciality_label = tk.Label(self.frame, text="Age")
            self.speciality_label.grid(row=1, column=3)

            self.speciality_label = tk.Label(self.frame, text="Mobile")
            self.speciality_label.grid(row=1, column=4)

            self.speciality_label = tk.Label(self.frame, text="Postcode")
            self.speciality_label.grid(row=1, column=5)

            for index, patient in enumerate(patients):
                id_entry = tk.Entry(self.frame, fg='blue')
                id_entry.grid(row=index+2, column=0)
                id_entry.insert(tk.END, index+1)

                fullname_entry = tk.Entry(self.frame, fg='blue')
                fullname_entry.grid(row=index+2, column=1)
                fullname_entry.insert(tk.END, patient.full_name())

                speciality_entry = tk.Entry(self.frame, fg='blue')
                speciality_entry.grid(row=index+2, column=2)
                speciality_entry.insert(tk.END, patient.get_doctor())

                speciality_entry = tk.Entry(self.frame, fg='blue')
                speciality_entry.grid(row=index+2, column=3)
                speciality_entry.insert(tk.END, patient.get_age())

                speciality_entry = tk.Entry(self.frame, fg='blue')
                speciality_entry.grid(row=index+2, column=4)
                speciality_entry.insert(tk.END, patient.get_mobile())

                speciality_entry = tk.Entry(self.frame, fg='blue')
                speciality_entry.grid(row=index+2, column=5)
                speciality_entry.insert(tk.END, patient.get_postcode())

            self.user_given_patient_id_label = tk.Label(self.frame, text="Enter the ID of the patient:")
            self.user_given_patient_id_label.grid(row=len(self.patients)+2, column=0, columnspan=2)

            self.user_given_patient_id_entry = tk.Entry(self.frame, fg='black')
            self.user_given_patient_id_entry.grid(row=len(self.patients)+2, column=2, columnspan=4)

            self.relocate_target_patient_continue_button = tk.Button(self.frame, text="Enter", command=self.relocate_target_patient_continue_button_action)
            self.relocate_target_patient_continue_button.grid(row=len(self.patients)+3, column=0, columnspan=7)

            self.go_home_button = tk.Button(self.frame, text="Go To Home", command=self.home_window)
            self.go_home_button.grid(row=len(self.patients)+4, column=0, columnspan=7)

            self.alert_variable = tk.StringVar()
            self.alert_variable.set("")
            self.alert_label = tk.Label(self.frame, textvariable=self.alert_variable)
            self.alert_label.grid(row=len(self.patients)+5, column=0, columnspan=7)

            self.frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
    
    def relocate_target_patient_continue_button_action(self):
        to_continue = False
        try:
            target_patient_id = int(self.user_given_patient_id_entry.get())-1
            doctor_index=self.admin.find_index(target_patient_id,self.patients)
            if doctor_index==False:
                self.alert_label.config(fg= "red")
                self.alert_variable.set("Patient not found.")
            else:
                to_continue = True
                self.__intermediate_variable = target_patient_id
        except:
            self.alert_label.config(fg= "red")
            self.alert_variable.set("The ID entered is incorrect.")

        if to_continue == True:
            target_patient_object = self.patients[target_patient_id]

            self.clear_previous_widgets()
            self.window.title("Book an appointment")
            self.window.geometry("400x400")

            self.canvas = tk.Canvas(self.window)
            self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

            self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
            self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

            self.canvas.configure(yscrollcommand=self.scrollbar.set)

            self.frame = tk.Frame(self.canvas)
            self.canvas.create_window((0, 0), window=self.frame, anchor='nw')

            self.text_label = tk.Label(self.frame, text="-----Choose Doctor-----")
            self.text_label.grid(row=0, column=0, columnspan=4)

            self.id_label = tk.Label(self.frame, text="ID")
            self.id_label.grid(row=1, column=0)

            self.fullname_label = tk.Label(self.frame, text="Full Name")
            self.fullname_label.grid(row=1, column=1)

            self.speciality_label = tk.Label(self.frame, text="Speciality")
            self.speciality_label.grid(row=1, column=2)

            for index, doctor in enumerate(self.doctors):
                id_entry = tk.Entry(self.frame, fg='blue')
                id_entry.grid(row=index+2, column=0)
                id_entry.insert(tk.END, index+1)

                fullname_entry = tk.Entry(self.frame, fg='blue')
                fullname_entry.grid(row=index+2, column=1)
                fullname_entry.insert(tk.END, doctor.full_name())

                speciality_entry = tk.Entry(self.frame, fg='blue')
                speciality_entry.grid(row=index+2, column=2)
                speciality_entry.insert(tk.END, doctor.get_speciality())

            self.user_given_doctor_id_label = tk.Label(self.frame, text="Enter the ID of the doctor:")
            self.user_given_doctor_id_label.grid(row=len(self.doctors)+2, column=0)

            self.user_given_doctor_id_entry = tk.Entry(self.frame, fg='black')
            self.user_given_doctor_id_entry.grid(row=len(self.doctors)+2, column=1, columnspan=3)

            self.relocate_doctor_id_submit_button = tk.Button(self.frame, text="Enter", command=self.relocate_assign_doctor_given_doctor_id_submit_button_action)
            self.relocate_doctor_id_submit_button.grid(row=len(self.doctors)+3, column=0, columnspan=4)

            self.go_home_button = tk.Button(self.frame, text="Go To Home", command=self.home_window)
            self.go_home_button.grid(row=len(self.doctors)+4, column=0, columnspan=4)

            self.alert_variable = tk.StringVar()
            self.alert_variable.set("")
            self.alert_label = tk.Label(self.frame, textvariable=self.alert_variable)
            self.alert_label.grid(row=len(self.doctors)+5, column=0, columnspan=4)

            self.frame.update_idletasks()
            self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def relocate_assign_doctor_given_doctor_id_submit_button_action(self):
        patients = [each for each in self.patients if each.get_doctor() != 'None']
        to_continue = False
        try:
            target_doctor_id = int(self.user_given_doctor_id_entry.get())-1
            doctor_index=self.admin.find_index(target_doctor_id,self.doctors)
            if doctor_index==False:
                self.alert_label.config(fg= "red")
                self.alert_variable.set("Doctor not found.")
            else:
                to_continue = True
        except:
            self.alert_label.config(fg= "red")
            self.alert_variable.set("The ID entered is incorrect.")

        if to_continue == True:
            target_patient_object = patients[self.__intermediate_variable]
            target_doctor_object = self.doctors[target_doctor_id]
            
            target_doctor_object.add_patient(target_patient_object) # Assigining the patient to the doctor 
            target_patient_object.link(target_doctor_object.full_name()) # Linking the doctor to the patient
                

            self.clear_previous_widgets()

            self.text_label = tk.Label(self.window, text=f"Patient {target_patient_object.full_name()} is now relocated to {target_doctor_object.full_name()}.")
            self.text_label.grid(row=0, column=0)
            self.text_label.config(fg= "green")

            self.new_go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
            self.new_go_home_button.grid(row=1, column=0)








    def update_admin_details_action(self):
        self.clear_previous_widgets()
        self.window.title("Update Admin Detials")
        self.window.geometry("400x400")

        self.text_label = tk.Label(self.window, text=f"-----Update Admin Detials-----")
        self.text_label.grid(row=0, column=0)

        self.text_label = tk.Label(self.window, text=f"Choose the field to be updated:")
        self.text_label.grid(row=1, column=0)

        self.update_admin_username_button = tk.Button(self.window, text="Change Admin Username", command=self.update_admin_username_button_action)
        self.update_admin_username_button.grid(row=2, column=0)

        self.update_admin_password_button = tk.Button(self.window, text="Change Admin Password", command=self.update_admin_password_button_action)
        self.update_admin_password_button.grid(row=3, column=0)

        self.update_admin_address_doctor_button = tk.Button(self.window, text="Change Admin Address", command=self.update_admin_address_button_action)
        self.update_admin_address_doctor_button.grid(row=4, column=0)

        self.go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
        self.go_home_button.grid(row=5, column=0)

    def update_admin_entry_page_builder(self, title_text, update_option_name):
        self.clear_previous_widgets()
        self.window.title(title_text)
        self.window.geometry("400x400")

        self.text_label = tk.Label(self.window, text=f"-----{title_text}-----")
        self.text_label.grid(row=0, column=0, columnspan=3)

        self.admin_update_option_label = tk.Label(self.window, text=f"Enter new {update_option_name}:")
        self.admin_update_option_label.grid(row=1, column=0)

        self.admin_update_option_entry = tk.Entry(self.window)
        self.admin_update_option_entry.grid(row=1, column=1)

        button_action_list = [
            self.update_admin_username_option_entry_button_action,
            self.update_admin_password_option_entry_button_action,
            self.update_admin_address_option_entry_button_action
        ]
        if update_option_name == "username":
            self.register_doctor_button = tk.Button(self.window, text="Enter", command=button_action_list[0])
            self.register_doctor_button.grid(row=2, column=0, columnspan=3)
        elif update_option_name == "password":
            self.register_doctor_button = tk.Button(self.window, text="Enter", command=button_action_list[1])
            self.register_doctor_button.grid(row=2, column=0, columnspan=3)
        elif update_option_name == "address":
            self.register_doctor_button = tk.Button(self.window, text="Enter", command=button_action_list[2])
            self.register_doctor_button.grid(row=2, column=0, columnspan=3)

        self.go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
        self.go_home_button.grid(row=3, column=0, columnspan=3)
        
        self.alert_variable = tk.StringVar()
        self.alert_variable.set("")
        self.alert_label = tk.Label(self.window, textvariable=self.alert_variable)
        self.alert_label.grid(row=4, column=0, columnspan=3)

        self.make_window_responsive(5,2)
    
    def update_admin_action_feedback_page_builder(self):
        pass

    def update_admin_username_button_action(self):
        self.update_admin_entry_page_builder("Update Admin Username", "username")

    def update_admin_username_option_entry_button_action(self):
        new_username = self.admin_update_option_entry.get().strip()

        if new_username == '' or new_username.isspace() == True:
            self.alert_label.config(fg= "red")
            self.alert_variable.set('Please give a valid input - Not empty strings or spaces')
        else:
            self.admin.modify_database_content("./data/admin.txt", self.admin.get_admin_username(), new_username) # Changing in the database
            self.admin.set_admin_username(new_username)

            self.clear_previous_widgets()

            self.text_label = tk.Label(self.window, text="Username is changed.")
            self.text_label.grid(row=0, column=0)
            self.text_label.config(fg= "green")

            self.new_go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
            self.new_go_home_button.grid(row=1, column=0)


    def update_admin_password_button_action(self):
        self.update_admin_entry_page_builder("Update Admin Password", "password")

    def update_admin_password_option_entry_button_action(self):
        password = self.admin_update_option_entry.get().strip()
        self.__intermediate_variable = password

        if password == '' or password.isspace() == True:
            self.alert_label.config(fg= "red")
            self.alert_variable.set('Please give a valid input - Not empty strings or spaces')
        else:
            self.clear_previous_widgets()
            self.window.geometry("400x400")

            self.text_label = tk.Label(self.window, text=f" ")
            self.text_label.grid(row=0, column=0, columnspan=3)

            self.admin_update_option_label = tk.Label(self.window, text=f"Enter password again:")
            self.admin_update_option_label.grid(row=1, column=0)

            self.admin_update_option_entry = tk.Entry(self.window)
            self.admin_update_option_entry.grid(row=1, column=1)

            self.register_doctor_button = tk.Button(self.window, text="Change Detail", command=self.update_admin_password_again_option_entry_button_action)
            self.register_doctor_button.grid(row=2, column=0, columnspan=3)

            self.go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
            self.go_home_button.grid(row=3, column=0, columnspan=3)
            
            self.alert_variable = tk.StringVar()
            self.alert_variable.set("")
            self.alert_label = tk.Label(self.window, textvariable=self.alert_variable)
            self.alert_label.grid(row=4, column=0, columnspan=3)

            self.make_window_responsive(5,2)

    def update_admin_password_again_option_entry_button_action(self):
            again_password = self.admin_update_option_entry.get().strip()
            # validate the password
            if again_password == self.__intermediate_variable:
                self.admin.modify_database_content("./data/admin.txt", self.admin.get_admin_password(), again_password) # Changing in the database
                self.admin.set_admin_password(again_password)

                self.clear_previous_widgets()

                self.text_label = tk.Label(self.window, text="Password is changed.")
                self.text_label.grid(row=0, column=0)
                self.text_label.config(fg= "green")

                self.new_go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
                self.new_go_home_button.grid(row=1, column=0)
            else:
                self.alert_label.config(fg= "red")
                self.alert_variable.set('Inconsistent password entry. Password not updated!')


    def update_admin_address_button_action(self):
        self.update_admin_entry_page_builder("Update Admin Address", "address")

    def update_admin_address_option_entry_button_action(self):
        new_address = self.admin_update_option_entry.get().strip()

        if new_address == '' or new_address.isspace() == True:
            self.alert_label.config(fg= "red")
            self.alert_variable.set('Please give a valid input - Not empty strings or spaces')
        else:
            self.admin.modify_database_content("./data/admin.txt", self.admin.get_admin_address(), new_address) # Changing in the database
            self.admin.set_admin_address(new_address)

            self.clear_previous_widgets()

            self.text_label = tk.Label(self.window, text="Address is changed.")
            self.text_label.grid(row=0, column=0)
            self.text_label.config(fg= "green")

            self.new_go_home_button = tk.Button(self.window, text="Go To Home", command=self.home_window)
            self.new_go_home_button.grid(row=1, column=0)












    def request_management_report_action(self):
        total_doctors_numbers = len(self.doctors)

        total_patients_numbers = len(self.patients)

        total_patients_numbers_per_doctor = {}
        for doctor in self.doctors:
            total_patients_numbers_per_doctor[doctor.full_name()] = len(doctor.get_patients())

        total_number_of_appointments_per_doctor = {}
        for doctor in self.doctors:
            total_number_of_appointments_per_doctor[doctor.full_name()] = len(doctor.get_appointments())

        total_number_of_patiens_based_on_illness = {}
        for patient in self.patients:
            patient_symptoms = patient.get_symptoms()
            for symptom in patient_symptoms:
                if symptom not in total_number_of_patiens_based_on_illness:
                    total_number_of_patiens_based_on_illness[symptom] = 1
                else:
                    total_number_of_patiens_based_on_illness[symptom] = total_number_of_patiens_based_on_illness[symptom] + 1


        self.clear_previous_widgets()
        self.window.title("Management Report")
        self.window.geometry("1000x750")
        # self.window.attributes('-fullscreen', True)

        self.canvas = tk.Canvas(self.window)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.window, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor='nw')



        self.number_of_doctors_label = tk.Label(self.frame, text="Total number of doctors in the system -->")
        self.number_of_doctors_label.grid(row=0, column=0)

        self.number_of_doctors_label = tk.Label(self.frame, text=f"{total_doctors_numbers} doctors")
        self.number_of_doctors_label.grid(row=0, column=1, columnspan=4)

        self.number_of_patients_label = tk.Label(self.frame, text="Total number of patients in the system -->")
        self.number_of_patients_label.grid(row=1, column=0)

        self.number_of_patients_label = tk.Label(self.frame, text=f"{total_patients_numbers} patients")
        self.number_of_patients_label.grid(row=1, column=1, columnspan=4)

        for n, (k, v) in enumerate(total_patients_numbers_per_doctor.items()):
            if n == 0:
                self.number_of_patient_per_doctor_label = tk.Label(self.frame, text="Total number of patients per doctor -->")
                self.number_of_patient_per_doctor_label.grid(row=n+2, column=0)

                self.number_of_patient_per_doctor_label = tk.Label(self.frame, text=f"Dr. {k} -->")
                self.number_of_patient_per_doctor_label.grid(row=n+2, column=1)

                self.number_of_patient_per_doctor_label = tk.Label(self.frame, text=f"{v} patients")
                self.number_of_patient_per_doctor_label.grid(row=n+2, column=2)
            else:
                self.number_of_patient_per_doctor_label = tk.Label(self.frame, text=f"Dr. {k} -->")
                self.number_of_patient_per_doctor_label.grid(row=n+2, column=1)

                self.number_of_patient_per_doctor_label = tk.Label(self.frame, text=f"{v} patients")
                self.number_of_patient_per_doctor_label.grid(row=n+2, column=2)

        for n, (k, v) in enumerate(total_number_of_appointments_per_doctor.items()):
            if n == 0:
                self.number_of_appointments_per_doctor_label = tk.Label(self.frame, text="Total number of appointments per month per doctor -->")
                self.number_of_appointments_per_doctor_label.grid(row=len(self.doctors)+n+2, column=0)

                self.number_of_appointments_per_doctor_label = tk.Label(self.frame, text=f"Dr. {k} -->")
                self.number_of_appointments_per_doctor_label.grid(row=len(self.doctors)+n+2, column=1)

                self.number_of_appointments_per_doctor_label = tk.Label(self.frame, text=f"{v} appointments")
                self.number_of_appointments_per_doctor_label.grid(row=len(self.doctors)+n+2, column=2)
            else:
                self.number_of_appointments_per_doctor_label = tk.Label(self.frame, text=f"Dr. {k} -->")
                self.number_of_appointments_per_doctor_label.grid(row=len(self.doctors)+n+2, column=1)

                self.number_of_appointments_per_doctor_label = tk.Label(self.frame, text=f"{v} appointments")
                self.number_of_appointments_per_doctor_label.grid(row=len(self.doctors)+n+2, column=2)

        for n, (k, v) in enumerate(total_number_of_patiens_based_on_illness.items()):
            if n == 0:
                self.number_of_patients_per_illnesses_label = tk.Label(self.frame, text="Total number of patients based on the illness -->")
                self.number_of_patients_per_illnesses_label.grid(row=(2*len(self.doctors))+n+2, column=0)

                self.number_of_patients_per_illnesses_label = tk.Label(self.frame, text=f"{k} -->")
                self.number_of_patients_per_illnesses_label.grid(row=(2*len(self.doctors))+n+2, column=1)

                self.number_of_patients_per_illnesses_label = tk.Label(self.frame, text=f"{v} patients")
                self.number_of_patients_per_illnesses_label.grid(row=(2*len(self.doctors))+n+2, column=2)
            else:
                self.number_of_patients_per_illnesses_label = tk.Label(self.frame, text=f"{k} -->")
                self.number_of_patients_per_illnesses_label.grid(row=(2*len(self.doctors))+n+2, column=1)

                self.number_of_patients_per_illnesses_label = tk.Label(self.frame, text=f"{v} patients")
                self.number_of_patients_per_illnesses_label.grid(row=(2*len(self.doctors))+n+2, column=2)

        self.go_home_button = tk.Button(self.frame, text="Go To Home", command=self.home_window)
        self.go_home_button.grid(row=(2*len(self.doctors))+len(total_number_of_patiens_based_on_illness)+3, column=0, columnspan=3)

    def start(self):
        self.window.mainloop()
    
    def stop(self):
        self.window.destroy()

if __name__ == '__main__':
    window = Main()
    window.start()
