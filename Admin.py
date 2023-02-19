from Doctor import Doctor
from Patient import Patient

class Admin:
    """A class that deals with the Admin operations"""
    def __init__(self, username, password, address = ''):
        """
        Args:
            username (string): Username
            password (string): Password
            address (string, optional): Address Defaults to ''
        """

        self.__username = username
        self.__password = password
        self.__address =  address

        self.__intermediate_variable = None # This is an intermediate variable which methods of this class can use to store before finally storing it else where and using it

    def get_admin_username(self):
        return self.__username
    def set_admin_username(self, new_username):
        self.__username = new_username

    def get_admin_password(self):
        return self.__password
    def set_admin_password(self, new_password):
        self.__password = new_password

    def get_admin_address(self):
        return self.__address
    def set_admin_address(self, new_address):
        self.__address = new_address
    
    def add_entry_to_database(self, file_path, to_add):
        """
        Adds a new line "to_add" to "file_path" file.
        """
        # Reading file
        db_file_read = open(file_path, 'a')
        db_file_read.write(f"\n{to_add}")
        db_file_read.close()
        

    def modify_database_content(self, file_path, to_replace, replacement):
        '''Allows modification of parameter in person's database file'''
        # Reading file
        db_file_read = open(file_path, 'r')
        db_orignal_list_of_lines = db_file_read.readlines() # making each line into a list
        db_orignal_list_of_lines = [each.strip() for each in db_orignal_list_of_lines] # stripping empty spaces and empty line
        db_file_read.close()

        # Replacing the content
        db_changed_list_of_lines = [line.replace(to_replace, replacement) if to_replace in line else line for line in db_orignal_list_of_lines]

        # Writing the mofication to the file
        db_file_write = open(file_path, 'w')
        for index, line in enumerate(db_changed_list_of_lines):
            if index != len(db_changed_list_of_lines)-1:
                db_file_write.write(f"{line}\n")
            else:
                db_file_write.write(line)
        db_file_write.close()

    def view(self,a_list):
        """
        print a list
        Args:
            a_list (list): a list of printables
        """
        for index, item in enumerate(a_list):
            print(f'{index+1:3}|{item}')

    def login(self) :
        """
        A method that deals with the login
        Raises:
            Exception: returned when the username and the password ...
                    ... don`t match the data registered
        Returns:
            string: the username
        """
    
        print("\n-----Login-----")
        #Get the details of the admin

        username = input('Enter the username: ')
        password = input('Enter the password: ')

        # check if the username and password match the registered ones
        return self.__username in username and self.__password == password

    def login_for_GUI(self, username, password) :
        # check if the username and password match the registered ones
        return self.__username in username and self.__password == password

    def find_index(self,index,doctors):
        
            # check that the doctor id exists          
        if index in range(0,len(doctors)):
            
            return True

        # if the id is not in the list of doctors
        else:
            return False
            
    def get_doctor_details(self) :
        """
        Get the details needed to add a doctor
        Returns:
            first name, surname and ...
                            ... the speciality of the doctor in that order.
        """

        new_doctor_f_name = input("Enter the first name: ")
        new_doctor_l_name = input("Enter the surname: ")
        new_doctor_speciality = input("Enter the speciality: ")

        # Checking for invalid input
        user_valid_input_counter = 0
        if new_doctor_f_name.isspace() == True or new_doctor_f_name == '' or new_doctor_l_name.isspace() == True or new_doctor_l_name == '' or new_doctor_speciality.isspace() == True or new_doctor_l_name == '':
            print("Please give a valid input - Not empty strings or spaces")
            return None, None, None
        # if valid input
        else:
            return new_doctor_f_name, new_doctor_l_name, new_doctor_speciality

    def doctor_management(self, doctors):
        """
        A method that deals with registering, viewing, updating, deleting doctors
        Args:
            doctors (list<Doctor>): the list of all the doctors names
        """

        print("-----Doctor Management-----")

        # menu
        print('Choose the operation:')
        print(' 1 - Register')
        print(' 2 - View')
        print(' 3 - Update')
        print(' 4 - Delete')

        op = input('Input: ')

        # register
        if op == '1':
            print("-----Register-----")

            # get the doctor details
            print('Enter the doctor\'s details:')

            first_name, surname, speciality = self.get_doctor_details()

            if first_name==None and surname==None and speciality==None:
                return doctors

            # check if the name is already registered
            name_exists = False
            for doctor in doctors:
                if first_name == doctor.get_first_name() and surname == doctor.get_surname():
                    print('Name already exists.')

                    name_exists = True
                    break # save time and end the loop

            if name_exists == False:
                new_doc = Doctor(first_name, surname, speciality) 
                doctors.append(new_doc) # add the doctor ...
                                                         # ... to the list of doctors
                print('Doctor registered.')
                self.add_entry_to_database("./data/doctors.txt", f"{first_name}, {surname}, {speciality}")
                return doctors

        # View
        elif op == '2':
            print("-----List of Doctors-----")

            print(f"{'ID':3}|{'Full name':^30}|{'Speciality':^15}")
            all_doctors_detail = [] # Making a list of printable strings to use in view method of Adim class
            for doctor in doctors:
                doctor_full_name = doctor.full_name()
                doctor_speciality = doctor.get_speciality()
                doc_str_detail = f"{doctor_full_name:^30}|{doctor_speciality:^15}"
                all_doctors_detail.append(doc_str_detail)
            
            self.view(all_doctors_detail)

        # Update
        elif op == '3':
            while True:
                print("-----Update Doctor`s Details-----")
                print('ID |          Full name           |  Speciality')
                self.view(doctors)
                try:
                    index = int(input('Enter the ID of the doctor: ')) - 1
                    doctor_index=self.find_index(index,doctors)
                    if doctor_index!=False:
                
                        break
                        
                    else:
                        print("Doctor not found")

                    
                        # doctor_index is the ID mines one (-1)
                        

                except ValueError: # the entered id could not be changed into an int
                    print('The ID entered is incorrect')

            # menu
            while True:
                print('Choose the field to be updated:')
                print(' 1 First name')
                print(' 2 Surname')
                print(' 3 Speciality')
                try:
                    op = int(input('Input: ')) # make the user input lowercase
                    break
                except ValueError:
                    print('The entered option is invalid. Please enter 1/2/3.')

            to_update_doctor = doctors[index]
            if op == 1:
                to_update_first_name = input('Enter the new first name: ')
                to_update_first_name = to_update_first_name.title() # Converting the first letter to uppercase and rest to lower case

                previous_name = to_update_doctor.full_name()
                self.modify_database_content("./data/doctors.txt", f"{to_update_doctor.get_first_name()}, {to_update_doctor.get_surname()}", f"{to_update_first_name}, {to_update_doctor.get_surname()}") # Changing in the database
                to_update_doctor.set_first_name(to_update_first_name) # Updating the first name in the object
                print(f"First name of {previous_name} successfully changed to {to_update_first_name}.")
                return doctors
            elif op == 2:
                to_update_surname = input('Enter the new surname: ')
                to_update_surname = to_update_surname.title() # Converting the first letter to uppercase and rest to lower case

                previous_name = to_update_doctor.full_name()
                self.modify_database_content("./data/doctors.txt", f"{to_update_doctor.get_first_name()}, {to_update_doctor.get_surname()}", f"{to_update_doctor.get_first_name()}, {to_update_surname}") # Changing in the database
                to_update_doctor.set_surname(to_update_surname) # Updating the last name in the object
                print(f"Surname name of {previous_name} successfully changed to {to_update_surname}.")
                return doctors
            elif op == 3:
                to_update_speciality = input('Enter the new speciality: ')
                to_update_speciality = to_update_speciality.title() # Converting the first letter to uppercase and rest to lower case

                previous_speciality = to_update_doctor.get_speciality()
                self.modify_database_content("./data/doctors.txt", f"{to_update_doctor.get_surname()}, {to_update_doctor.get_speciality()}", f"{to_update_doctor.get_surname()}, {to_update_speciality}") # Changing in the database
                to_update_doctor.set_speciality(to_update_speciality) # Updating the first name in the object
                print(f"Speciality of {to_update_doctor.full_name()} successfully changed from {previous_speciality} to {to_update_speciality}.")
                return doctors

        # Delete
        elif op == '4':
            print("-----Delete Doctor-----")
            print('ID |          Full Name           |  Speciality')
            self.view(doctors)

            doctor_index = input('Enter the ID of the doctor to be deleted: ')

            try:
                doctor_index = int(doctor_index) - 1
                if self.find_index(doctor_index,doctors):
                    to_removed_doctor = doctors[doctor_index]

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

                    removed_doc = doctors.pop(doctor_index)
                    print(f"Doctor {removed_doc.full_name()} is deleted.")

                    return doctors
                else:
                    print('The id entered was not found')
            except ValueError:
                print('The doctor id entered is incorrect')

        # if the id is not in the list of patients
        else:
            print('Invalid operation choosen. Check your spelling!')


    def view_patient(self, patients):
        """
        print a list of patients
        Args:
            patients (list<Patients>): list of all the active patients
        """
        print("-----View Patients-----")
        print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')

        self.view(patients)

    def add_patient(self, patients):
        print("-----Add a patient-----")
        new_patient_f_name = input("Enter the first name: ")
        new_patient_l_name = input("Enter the surname: ")
        new_patient_age = input("Enter age: ")
        new_patient_hone_number = input("Enter phone number: ")
        new_patient_postcode = input("Enter postcode (Address): ")

        new_patient_symptoms = input("Enter symptoms seperated by commas ',': ")
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
        user_valid_input_counter = 0
        if new_patient_f_name.isspace() == True or new_patient_f_name == '' or new_patient_l_name.isspace() == True or new_patient_l_name == '' or new_patient_age.isspace() == True or new_patient_age == '' or new_patient_hone_number.isspace() == True or new_patient_hone_number == ''  or new_patient_postcode.isspace() == True or new_patient_postcode == '':
            print("Please give a valid input - Not empty strings or spaces")
            return patients
        # if valid input
        else:
            new_patient_object = Patient(new_patient_f_name, new_patient_l_name, new_patient_age, new_patient_hone_number, new_patient_postcode, new_patient_symptoms)
            patients.append(new_patient_object)

            self.add_entry_to_database("./data/patients.txt", f"{new_patient_f_name}, {new_patient_l_name}, {new_patient_age}, {new_patient_hone_number}, {new_patient_postcode}, {new_patient_symptoms_in_str_form}")
            print(f"Patient {new_patient_f_name} {new_patient_l_name} added successfully.")

            return patients

    def appointment_management(self, patients, doctors):
        print("-----Appointment management-----")
        # menu
        print('Choose the operation:')
        print(' 1 - Book an appointment')
        print(' 2 - Check appointment status')

        op = input('Input: ')

        if op == "1":
            print("-----Book an appointment-----")

            print("-----List of patients-----")
            print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')
            self.view(patients)
            try:
                p_index = int(input('Enter the ID of the patient: ')) - 1
                patient_index=self.find_index(p_index,patients)
                if patient_index==False:
                    print("Patient not found")
            except ValueError:
                print('The ID entered is incorrect')

            selected_patient = patients[p_index] # patient object

            print("-----List of doctors-----")
            print('ID |          Full name           |  Speciality')
            self.view(doctors)
            try:
                d_index = int(input('Enter the ID of the doctor: ')) - 1
                doctor_index=self.find_index(d_index,doctors)
                if doctor_index==False:
                    print("Doctor not found")
            except ValueError:
                print('The ID entered is incorrect')

            selected_doctor = doctors[d_index] # doctor object

            selected_patient.add_to_appointments_made(selected_doctor)
            selected_doctor.add_appointment(selected_patient)

            print("Appointment booked. You can check your appointment status.")
        
        elif op == "2":
            '''
            For appointment checking logic:
                - If no doctor is assigned to a patient, then every appointment made by that patient has pending status
                - If an assigned doctor to a patient is same as the name of doctor with whom they booked an appointment, then the status is approved
                - If an assigned doctor to a patient is not same as the name of doctor with whom they booked an appointment, then the status is pending
            '''
            print("-----Check appointment status-----")

            print("-----List of patients-----")
            print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')
            self.view(patients)
            try:
                p_index = int(input('Enter the ID of the patient: ')) - 1
                patient_index=self.find_index(p_index,patients)
                if patient_index==False:
                    print("Patient not found")
            except ValueError:
                print('The ID entered is incorrect')
            
            selected_patient = patients[p_index] # patient object

            appointments_made = selected_patient.get_appointments_made()

            if len(appointments_made) == 0:
                print(f"{selected_patient.full_name()} hasn't booked any appointments. Book an appointment first.")
            else:
                print("-----Appointment Status-----")
                print(f"{'S.No.':5}|{'Appointments':^60}|{'Status':^30}")
                for counter, doctor in enumerate(appointments_made):
                    if selected_patient.get_doctor() == 'None':
                        print(f"{counter+1:>5}|{'Appointment with '+doctor.full_name():^60}|{'Pending':^30}")
                    elif selected_patient.get_doctor() == doctor.full_name():
                        print(f"{counter+1:>5}|{'Appointment with '+doctor.full_name():^60}|{'Approved':^30}")
                    else:
                        print(f"{counter+1:>5}|{'Appointment with '+doctor.full_name():^60}|{'Pending':^30}")

        
        else:
            print('Invalid operation choosen. Check your input!')

    def assign_doctor_to_patient(self, patients, doctors, relocate=False):
        """
        Allow the admin to assign a doctor to a patient or relocate a patient from one doctor to another
        Args:
            patients (list<Patients>): the list of all the active patients
            doctors (list<Doctor>): the list of all the doctors
            relocate (Boolean): True if the task is to relocate a patient from one doctor to another or Flase if assigning a doctor to a patient
        """

        patient_index = 0

        if relocate == False:
            print("-----Assign-----")

            print("-----Patients-----")
            print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')
            self.view(patients)

            index = input('Please enter the patient ID: ')
            patient_index = index
        
        elif relocate == True:
            patients = [each for each in patients if each.get_doctor() != 'None']

            if len(patients) == 0:
                print("No patient assigned to any doctors! Assign a doctor to a patient first.")
                return
            else:
                print("-----Relocate a patient from one doctor to another-----")

                print("-----Patients-----")
                print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')
                self.view(patients)

                index = input('Please enter the patient ID: ')
                patient_index = index

        try:
            # patient_index is the patient ID mines one (-1)
            patient_index = int(patient_index) -1

            # check if the id is not in the list of patients
            if patient_index not in range(len(patients)):
                print('The id entered was not found.')
                return # stop the procedures

        except ValueError: # the entered id could not be changed into an int
            print('The id entered is incorrect')
            return # stop the procedures

        print("-----Doctors Select-----")
        print('Select the doctor that fits these symptoms:')
        patients[patient_index].print_symptoms() # print the patient symptoms

        print('--------------------------------------------------')
        print('ID |          Full Name           |  Speciality   ')
        self.view(doctors)
        doctor_index = input('Please enter the doctor ID: ')

        try:
            # doctor_index is the patient ID mines one (-1)
            doctor_index = int(doctor_index) -1

            # check if the id is in the list of doctors
            if self.find_index(doctor_index,doctors)!=False:
                    
                # link the patients to the doctor and vice versa

                chosen_doctor = doctors[doctor_index] # Taking the user specified doctor object
                chosen_patient = patients[patient_index] # Taking the user specified patient object
                chosen_doctor.add_patient(chosen_patient) # Assigining the patient to the doctor 
                chosen_patient.link(chosen_doctor.full_name()) # Linking the doctor to the patient
                
                print('The patient is now assign to the doctor.')

            # if the id is not in the list of doctors
            else:
                print('The id entered was not found.')

        except ValueError: # the entered id could not be changed into an in
            print('The id entered is incorrect')


    def discharge(self, patients, discharge_patients):
        """
        Allow the admin to discharge a patient when treatment is done
        Args:
            patients (list<Patients>): the list of all the active patients
            discharge_patients (list<Patients>): the list of all the non-active patients
        """
        # print("-----Discharge Patient-----")

        # patient_index = input('Please enter the patient ID: ')

        while True:
            self.view_patient(patients) # Printing list of all patients
            user_confirmation = input("Do you want to discharge a patient(Y/N): ").lower() # Asking user for confirmation if they want to discharge a patient & converting to lowercase
            if user_confirmation == 'y':
                print("-----Discharge Patient-----")
                while True:
                    patient_index = input('Please enter the patient ID: ')
                    try:
                        patient_index = int(patient_index) - 1
                        if self.find_index(patient_index,patients)==True:
                            discharge_patient = patients.pop(patient_index) # Removing the patient we want to discharge from patients list and keeping it in a variable
                            discharge_patients.append(discharge_patient)
                            print(f"Patient {discharge_patient.full_name()} is discharged.")
                            return patients, discharge_patients
                        else:
                            print("Coudn't find the enter patient ID.")
                    except ValueError:
                        print("Invalid ID. Please enter a number ID.")
            elif user_confirmation == 'n':
                break
                return 
            else:
                print("Enter a valid input - Y or N")


    def view_discharge(self, discharged_patients):
        """
        Prints the list of all discharged patients
        Args:
            discharge_patients (list<Patients>): the list of all the non-active patients
        """
        if len(discharged_patients) == 0:
            print(f'No patients discharged yet. Discharge a patient first!')
        else:
            print("-----Discharged Patients-----")
            print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode ')
            self.view(discharged_patients)

    def update_details(self):
        """
        Allows the user to update and change username, password and address
        """

        print('Choose the field to be updated:')
        print(' 1 Username')
        print(' 2 Password')
        print(' 3 Address')
        try:
            op = int(input('Input: '))
        except ValueError: # the entered id could not be changed into an int
            print('The option entered is incorrect')
            return # stop the procedures

        if op == 1:
            new_username = input("Enter new username: ")
            self.modify_database_content("./data/admin.txt", self.__username, new_username) # Changing in the database
            self.set_admin_username(new_username)
            print('Username is changed.')

        elif op == 2:
            password = input('Enter the new password: ')
            # validate the password
            if password == input('Enter the new password again: '):
                self.modify_database_content("./data/admin.txt", self.__password, password) # Changing in the database
                self.set_admin_username(password)
            else:
                print(f"Inconsistent password entry. Password not updated!")

        elif op == 3:
            new_address = input("Enter new address: ")
            self.modify_database_content("./data/admin.txt", self.__address, new_address) # Changing in the database
            self.set_admin_username(new_address)
            print('Address is changed.')

        else:
            print('Enter a valid option id - 1/2/3')

    def group_patients_by_family(self, patients_list):
        """This function assumes patients with same surname are family. So they are grouped as such."""

        # Grouping related patients together in a dictionary
        grouped_by_surname_dict = {}
        for patient in patients_list:
            patient_surname = patient.get_surname()
            if patient_surname not in grouped_by_surname_dict:
                grouped_by_surname_dict[patient_surname] = [patient]
            else:
                li = grouped_by_surname_dict[patient_surname]
                li.append(patient)
                grouped_by_surname_dict[patient_surname] = li
        
        # Converting the dict into a list with all the patients objects
        grouped_by_surname = []
        for key, value in grouped_by_surname_dict.items():
            grouped_by_surname.extend(value)

        return grouped_by_surname

    def request_management_report(self, patients, doctors):

        total_doctors_numbers = len(doctors)

        total_patients_numbers = len(patients)

        total_patients_numbers_per_doctor = {}
        for doctor in doctors:
            total_patients_numbers_per_doctor[doctor.full_name()] = len(doctor.get_patients())

        total_number_of_appointments_per_doctor = {}
        for doctor in doctors:
            total_number_of_appointments_per_doctor[doctor.full_name()] = len(doctor.get_appointments())

        total_number_of_patiens_based_on_illness = {}
        for patient in patients:
            patient_symptoms = patient.get_symptoms()
            for symptom in patient_symptoms:
                if symptom not in total_number_of_patiens_based_on_illness:
                    total_number_of_patiens_based_on_illness[symptom] = 1
                else:
                    total_number_of_patiens_based_on_illness[symptom] = total_number_of_patiens_based_on_illness[symptom] + 1


        print("\n-----Management Report-----")
        print(f"\n{'Total number of doctors in the system':<50} : {total_doctors_numbers}")
        print(f"\n{'Total number of patients in the system':<50} : {total_patients_numbers}")

        for n, (k, v) in enumerate(total_patients_numbers_per_doctor.items()):
            if n == 0:
                print(f"\n{'Total number of patients per doctor':<50} : {'Dr. '+k:<23} = {v:>3} patients")
            else:
                print(f"{' ':>50}   {'Dr. '+k:<23} = {v:>3} patients")
        
        for n, (k, v) in enumerate(total_number_of_appointments_per_doctor.items()):
            if n == 0:
                print(f"\n{'Total number of appointments per month per doctor':<50} : {'Dr. '+k:<23} = {v:>3} appointments")
            else:
                print(f"{' ':>50}   {'Dr. '+k:<23} = {v:>3} appointments")

        for n, (k, v) in enumerate(total_number_of_patiens_based_on_illness.items()):
            if n == 0:
                print(f"\n{'Total number of patients based on the illness':<50} : {k:<23} = {v:>3} patients")
            else:
                print(f"{' ':>50}   {k:<23} = {v:>3} patients")