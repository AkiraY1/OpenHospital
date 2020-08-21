class User():
    def __init__(self,user_id,email,name,password, role, practice, address, gender, ethnicity, age, birthdate, occupation, symptoms, history):
        self.id = user_id
        self.email = email
        self.name = name
        self.password = password
        self.role = role
        self.practice = practice
        self.address = address
        self.gender = gender
        self.ethnicity = ethnicity
        self.age = age
        self.birthdate = birthdate
        self.occupation = occupation
        self.symptoms = symptoms
        self.history = history
        self.active = True

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return str(self.id)