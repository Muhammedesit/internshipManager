from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel
from PyQt5 import QtGui

from page_stack import PageStack

class InstructorRegisterPage(QDialog):
    def __init__(self):
        super().__init__()
        loadUi("ui_docs\\instructor_register.ui",self)
        self.pageStack = PageStack.getInstance()

        self.btnGoBack.clicked.connect(self.goback)
        self.btnRegister.clicked.connect(self.registerInstructor)

        self.btnRadioMale.toggled.connect(self.setGender)
        self.btnRadioFemale.toggled.connect(self.setGender)
        self.gender = ""

    def getInputs(self):
        username = self.inputUsername.text()
        password = self.inputPassword.text()
        confirmpassword = self.inputConfirmPassword.text()
        phone = self.inputPhone.text()
        email = self.inputEmail.text()
        
        name = self.inputName.text()
        surname = self.inputSurname.text()
        gender = self.getGender()
        
        department = self.inputDepartmentName.text()

        print(username, password, confirmpassword, phone, email, name,
                                    surname, gender, department)

        dataMap = {
            'username':username,
            'password':password,
            'confirmpassword':confirmpassword,
            'phone':phone,
            'email':email,
            'name':name,
            'surname':surname,
            'gender':gender,
            'department':department,
        }

        return dataMap

    def setGender(self):
        
        if self.btnRadioMale.isChecked()==True:
            self.gender = "male"
        elif self.btnRadioFemale.isChecked()==True:
            self.gender = "female"

    def getGender(self):
        return self.gender # boş olmasın validate

    

    def registerInstructor(self):
        # TODO check if entered data is in valid form.
        # check if there is a user having the same username, phone and email. If there is raise error.
        dataMap = self.getInputs()
        isvalid = self.validateInput(dataMap)

        if(isvalid):
            try:
                self.pageStack.dbOperations.insertUser(dataMap['username'], dataMap['password'], dataMap['phone'], dataMap['email'])
                uid = self.pageStack.dbOperations.getUserID(dataMap['username'], dataMap['password'])
                self.pageStack.dbOperations.insertPerson(uid, dataMap['name'], dataMap['surname'], dataMap['gender'])
                deptNo = self.pageStack.dbOperations.getDepartmentNo(dataMap['department'])

                self.pageStack.dbOperations.insertInstructor(uid, deptNo)

                self.showWarning("registered")
                
            except Exception as err:
                self.showWarning(str(err))

    
    def validateInput(self, dataMap):
        isvalid = True
        # isEmpty?
        for key in dataMap:
            print(key, dataMap[key], str(dataMap[key]))
            if str(dataMap[key])=="":
                isvalid = False
                self.showWarning("Do not leave the field "
                                    + key + " empty!")
                
                break
        # other criterias:
        if dataMap['confirmpassword'] != dataMap['password']:
            isvalid = False
            self.showWarning("Entered passwords do not match! Check them.")
        elif len(dataMap['password']) <7 and dataMap['password'] != "":
            isvalid = False
            self.showWarning("Password must be at least 7 characters!")
        elif len(dataMap['username']) < 3:
            isvalid = False
            self.showWarning("Username must be at least 3 characters!")
        elif len(dataMap['name']) < 3 and dataMap['name'] != "":
            isvalid = False
            self.showWarning("Name must be at least 3 characters!")
        elif len(dataMap['surname']) < 3 and dataMap['surname']!= "":
            isvalid = False
            self.showWarning("Surname must be at least 3 characters!")
        elif dataMap['email'] != "":
            if len(dataMap['email']) < 7:
                isvalid = False
                self.showWarning("Email must be at least 7 characters!")
            elif dataMap['email'].find("@") == -1 or dataMap['email'].find(".com") == -1:
                isvalid = False
                self.showWarning("There must be '@' and '.com' in the email." )
        elif dataMap['phone']!= "" and dataMap['phone'].isdigit() == False:
            isvalid = False
            self.showWarning("The phone number must consist of digits!" )
        elif dataMap['department']!="" and len(dataMap['department'])>6:
            isvalid = False
            self.showWarning("Department name can be at most 6 characters!")
        elif dataMap['department'] != "":
            departments = ["COMP", "EE", "IE", "ME", "BA", "POL"]
            for dept in departments:
                if dataMap['department'] != dept:
                    isvalid = False
                    self.showWarning("No such department")

        return isvalid 


    def showWarning(self, text):
        dlg = CustomDialog(text)
        if dlg.exec():
            print("Success!")
        else:
            print("Cancel!")

    def goback(self):
        # TODO clear the entered data
        self.pageStack.setWindowTitle("Register Menu Page")
        self.pageStack.removeWidget(self)






class CustomDialog(QDialog):
    def __init__(self, text, parent=None):
        super().__init__(parent)


        if text=="registered":
            self.setWindowTitle("CONGRATS :)")

            QBtn = QDialogButtonBox.Ok

            self.buttonBox = QDialogButtonBox(QBtn)
            self.buttonBox.accepted.connect(self.accept)

            self.layout = QVBoxLayout()
            message = QLabel("Succesfully Registered")
            self.layout.addWidget(message)
            self.layout.addWidget(self.buttonBox)
            self.setLayout(self.layout)

        else:
            self.setWindowTitle("Warning!")

            QBtn = QDialogButtonBox.Ok

            self.buttonBox = QDialogButtonBox(QBtn)
            self.buttonBox.accepted.connect(self.accept)

            self.layout = QVBoxLayout()
            message = QLabel(text)
            self.layout.addWidget(message)
            self.layout.addWidget(self.buttonBox)
            self.setLayout(self.layout)