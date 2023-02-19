# Imports
from Admin import Admin
from Doctor import Doctor
from Patient import Patient

def database_to_model(person_database_file, person_type):
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

# def parameter_to_model()   
def main():
    """
    the main function to be ran when the program runs
    """

    # Initialising the actors

    # admin = Admin('admin','123','B1 1AB') # username is 'admin', password is '123'
    admin = database_to_model("./data/admin.txt", 'admin')

    # doctors = [Doctor('John','Smith','Internal Med.'), Doctor('Jone','Smith','Pediatrics'), Doctor('Jone','Carlos','Cardiology')]
    doctors = database_to_model("./data/doctors.txt", 'doctor')

    # patients = [Patient('Sara','Smith', 20, '07012345678','B1 234'), Patient('Mike','Jones', 37,'07555551234','L2 2AB'), Patient('Daivd','Smith', 15, '07123456789','C1 ABC')]
    patients = database_to_model("./data/patients.txt", 'patient')
    patients = admin.group_patients_by_family(patients) # Patients of the same family are grouped together 
    
    discharged_patients = []

    # keep trying to login tell the login details are correct
    while True:
        if admin.login():
            running = True # allow the program to run
            break
        else:
            print('Incorrect username or password.')

    while running:
        # print the menu
        print('Choose the operation:')
        print(' 1- Register/view/update/delete doctor')
        print(' 2- Add patients')
        print(' 3- View/Discharge patients')
        print(' 4- View discharged patient')
        print(' 5- Book appointment/check appointment status')
        print(' 6- Assign doctor to a patient')
        print(' 7- Relocate a patient from one doctor to another')
        print(' 8- Update admin detais') 
        print(' 9- Request management report')
        print(' 10- Quit')

        # get the option
        op = input('Option: ')

        if op == '1':
            # 1- Register/view/update/delete doctor
            returned_data = admin.doctor_management(doctors)
            if type(returned_data) == list: # Only assigining new modified doctors when returned datatype is list because functions like 'view' in 'doctor_management' method of class 'Admin' does not return anything
                doctors = returned_data

        elif op == '2':
            # 2- Add patient
            patients = admin.add_patient(patients)

        elif op == '3':
            # 2- View or discharge patients
            try:
                user_confirmed = True
                # Only assigining new modified patiends and discharged patients when returned datatype is list because whenever user confirmation is 'n' or any input except 'y' for:
                # input("Do you want to discharge a patient(Y/N): ") in Admin.discharge(patients, discharge_patients) method
                # It does not return anything and the line below won't work; throws TypeError: cannot unpack non-iterable NoneType object
                returned_patients_data, returned_discharged_patients_data = admin.discharge(patients, discharged_patients)
                if type(returned_patients_data) == list and type(returned_discharged_patients_data) == list: 
                    patients, discharged_patients = returned_patients_data, returned_discharged_patients_data
                # Grouping by same family
                patients = admin.group_patients_by_family(patients)
                discharged_patients = admin.group_patients_by_family(discharged_patients)
            except:
                user_confirmed = False

            while user_confirmed == True:
                op = input('Do you want to discharge a patient(Y/N):').lower()

                if op == 'yes' or op == 'y':
                    try:
                        # Only assigining new modified patiends and discharged patients when returned datatype is list because whenever user confirmation is 'n' or any input except 'y' for:
                        # input("Do you want to discharge a patient(Y/N): ") in Admin.discharge(patients, discharge_patients) method
                        # It does not return anything and the line below won't work; throws TypeError: cannot unpack non-iterable NoneType object
                        returned_patients_data, returned_discharged_patients_data = admin.discharge(patients, discharged_patients)
                        if type(returned_patients_data) == list and type(returned_discharged_patients_data) == list: 
                            patients, discharged_patients = returned_patients_data, returned_discharged_patients_data
                            # Grouping by same family
                            patients = admin.group_patients_by_family(patients)
                            discharged_patients = admin.group_patients_by_family(discharged_patients)
                    except:
                        pass # Do nothing

                elif op == 'no' or op == 'n':
                    break

                # unexpected entry
                else:
                    print('Please answer by yes or no.')
        
        elif op == '4':
            # 3 - view discharged patients
            admin.view_discharge(discharged_patients)

        elif op == '5':
            # 4- Book/check appointments
            admin.appointment_management(patients, doctors)

        elif op == '6':
            # 5- Assign doctor to a patient
            admin.assign_doctor_to_patient(patients, doctors, False)

        elif op == '7':
            # 6- Relocate patient to another doctor
            admin.assign_doctor_to_patient(patients, doctors, True)

        elif op == '8':
            # 7- Update admin detais
            admin.update_details()
        
        elif op == '9':
            # 8- Request management report
            admin.request_management_report(patients, doctors)

        elif op == '10':
            # 9 - Quit
            break

        else:
            # the user did not enter an option that exists in the menu
            print('Invalid option. Try again')

if __name__ == '__main__':
    main()
