from Person import Person

class Patient(Person):
    """Patient class"""

    def __init__(self, first_name, surname, age, mobile, postcode, symptoms=[]):
        """
        Args:
            first_name (string): First name
            surname (string): Surname
            age (int): Age
            mobile (string): the mobile number
            address (string): address
            symptoms (list): list of symptoms of patient
        """

        super().__init__(first_name, surname)

        self.__age = age
        self.__mobile = mobile
        self.__postcode = postcode
        self.__doctor = 'None'

        self.__symptoms = [each.title() for each in symptoms]
        self.__appointments_made = []

    def get_age(self):
        return self.__age

    def set_age(self, new_age):
        self.__age = new_age

    def get_mobile(self):
        return self.__mobile

    def set_age(self, new_mobile):
        self.__mobile = new_mobile

    def get_postcode(self):
        return self.__postcode

    def set_age(self, new_mobile):
        self.__postcode = new_postcode

    def get_doctor(self) :
        return self.__doctor

    def link(self, doctor):
        """Args: doctor(string): the doctor full name"""
        self.__doctor = doctor

    def get_symptoms(self):
        return self.__symptoms
    
    def add_to_symptoms(self, symptom):
        self.__symptoms.append(symptom)
    
    def set_symptom(self, symptoms_list):
        self.__symptoms = symptoms_list
        
    def print_symptoms(self):
        """prints all the symptoms"""
        
        print(f"The patient's symptoms:")
        for index, symptom in enumerate(self.__symptoms):
            print(f"{index+1}. {symptom}")
    
    def get_appointments_made(self):
        return self.__appointments_made
    
    def add_to_appointments_made(self, appointment):
        self.__appointments_made.append(appointment)
        

    def __str__(self):
        return f'{self.full_name():^30}|{self.__doctor:^30}|{self.__age:^5}|{self.__mobile:^15}|{self.__postcode:^10}'
