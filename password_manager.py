import random
import hashlib
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import re

#chars used for the random password generation
chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%^&*(~`)+"


def store_password():
    user = str(input(
        "Are you a new or returning user (type 'n' for new or 'r' for returning ) : "))
    if user == 'n':

        # example of basic operation 5 Register
        print("Welcome new user")
        username = str(input("Username: "))
        password = str(input("Password: "))
        passcheck = str(input("Please re-type password to ensure no typos occured: "))
        if password == passcheck:

            # variable to use when making the hash with the users username and password
            uniqueUser = username + password
            inituniqueUser = bytes(uniqueUser, 'utf-8')

            #unique salt to be added on hash
            salty = uniqueUser + "adaed wioedu 9823q1eg uawd a" + uniqueUser +\
            "super secret complicarted words to throw into salty mc salt " +\
            "bxacxe1xdex1cx8fxecxc2x98x80nFxa5xcbxd35x8bx98x91xb2xfex0cx8bxa2mxc9xe4Fk"

            salt = bytes(salty, 'utf-8')

            # hash iterated 100,000 times for added difficulty
            kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,)        
            masterKey = base64.urlsafe_b64encode(kdf.derive(inituniqueUser))

            #this will be used as the file name and is the username+password+masterkey
            authRes = username + password + str(masterKey)
            authPre = bytes(authRes, 'utf-8')

            #hashed another 100,000 times for added complexity
            authKey= hashlib.pbkdf2_hmac('sha256', authPre, salt, 100000)

            #convereted to a sting and stripped so it will be a valid file name
            authKeyString = str(authKey)
            authKeyFileName = s = re.sub(r'\W+', '', authKeyString)

            print("Creating Credentials")

            #setting the file name for the user
            fileName = "%s.txt" % authKeyFileName

            if not os.path.exists(fileName):
                f = open(fileName, 'a')
                f.write("initialize file\n")
                f.close()
                print("Thank you for logging in")
                print("Ensure you quit properly by pressing 'q' when finished or else you data will be lost")
                lookOrStore(masterKey,fileName)
            else:
                print("It appears you are a retrurning user try logging in")
                store_password()
        else:
            print("passwords in account creation did not match please try again")
            store_password()
        

    elif user == 'r':
        print("Welcome back")
        print("Ensure you quit properly by pressing 'q' when finished or else you data will be lost")
        username = str(input("Username: "))
        password = str(input("Password: "))
        #similar to the account creation just used to verify credintials to log in

        uniqueUser = username + password
        inituniqueUser = bytes(uniqueUser, 'utf-8')

        salty = uniqueUser + "adaed wioedu 9823q1eg uawd a" + uniqueUser +\
        "super secret complicarted words to throw into salty mc salt " +\
        "bxacxe1xdex1cx8fxecxc2x98x80nFxa5xcbxd35x8bx98x91xb2xfex0cx8bxa2mxc9xe4Fk"
        
        salt = bytes(salty, 'utf-8')

        kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,)        
        masterKey = base64.urlsafe_b64encode(kdf.derive(inituniqueUser))


        authRes = username + password + str(masterKey)
        authPre = bytes(authRes, 'utf-8')

        authKey= hashlib.pbkdf2_hmac('sha256', authPre, salt, 100000)
        authKeyString = str(authKey)
        authKeyFileName = s = re.sub(r'\W+', '', authKeyString)

        print("Checking Credentials")

        fileName = "%s.txt" % authKeyFileName

        if os.path.exists(fileName):
            # Decryption of the file upon correct credentials
            open(fileName, 'a').close()
            decrypt(masterKey, fileName)
            print("Thank you for logging in")
            lookOrStore(masterKey,fileName)
        else:
            print('Password is incorrect')
            store_password()

    else:
        print("un recognized response please try again")
        store_password()


def lookOrStore(masterKey, fileName):
    decision = str(input("would you like to look up a old password, create and store a new one, or manipulate existing data (type 'l' too look up, 'c' to create and store a new one ,'m' to manipulate , or 'q' to encrypt and quit): "))
    if decision == 'l':
        print("you chose look up")
        search(masterKey, fileName)

    elif decision == 'c':
        print("you chose create and store")
        store(masterKey, fileName)

    elif decision == 'm':
        print("you chose manipulate data")
        manipulate(masterKey, fileName)

    elif decision == 'q':
        #How the file in encrypted when the user logs out correctly
        print("data has been encrypted")
        encrypt(masterKey, fileName)
        store_password()

    else:
        print("un recognized response please try again ")
        lookOrStore(masterKey, fileName)


def search(masterKey, fileName):
    # example of basic operation 3 Retreive
    websiteName = str(
        input("What website are you looking for the information of? : "))
    searchfile = open(fileName, "r")
    for line in searchfile:
        x = line.split(",")
        if websiteName in x[0]:
            print(line)
            lookOrStore(masterKey, fileName)
    else:
        print("No data from that website found")
        lookOrStore(masterKey, fileName)


def store(masterKey, fileName):
    print("Please enter relevant information before we generate and store a new password for you")
    # example of basic operation 4 Check
    website = str(input("Website: "))
    searchfile = open(fileName, "r")
    for line in searchfile:
        x = line.split(",")
        if website in x[0]:
            print("there already exists data for this website on your account")
            lookOrStore(masterKey, fileName)

    else:
        site_username = str(input("Username or e-mail: "))
        indi_password = ""
        while True:
            # example of basic operation 1 Generate
            try:
                pass_len = int(input("How long would you like your password (reccomened min 20)  : "))
                break
            except ValueError:
                print("Please input integer only...")  
            continue
        for x in range(0, pass_len):
            password_val = random.choice(chars)
            indi_password = indi_password + password_val
        print("Your password is :", indi_password)
         # example of basic operation 2 Store
        f = open(fileName, "a")
        f.write(f"{website}, {site_username}, {indi_password}\n")
        f.close()
        print("Data has been saved")
        lookOrStore(masterKey, fileName)



def manipulate(masterKey, fileName):
    whatSite = str(
        input("What websites data are you looking to manipluate? : "))
    searchfile = open(fileName, "r")
    for line in searchfile:
        x = line.split(",")
        if whatSite in x[0]:
                whatToDo = str(input(
                    "Would you like to change the password or delete entierly (type 'c' to change type 'd' to delete): "))
                if whatToDo == 'c':
                    # example of basic operation 7 Change
                    x = line.split(",")
                    print(x)
                    cuser = x[1]
                    yON = str(input(
                        "Would you like us to generate a new password for this website (type 'y' for yes or 'n' for no): "))
                    if yON == 'y':
                        n_indi_password = ""
                        while True:
                            try:
                                pass_len = int(input("How long would you like your password (reccomened min 20)  : "))
                                break
                            except ValueError:
                                print("Please input integer only...")  
                            continue
                        for x in range(0, pass_len):
                            password_val = random.choice(chars)
                            n_indi_password = n_indi_password + password_val
                        print("deleted the previously saved data for this website")
                        deval = line
                        with open(fileName, 'r+') as f:
                            t = f.read()
                            to_delete = deval.strip()
                            f.seek(0)
                            for line in t.split('\n'):
                                if line != to_delete:
                                    f.write(line + '\n')
                            f.truncate()
                        print("Your new password is :", n_indi_password)
                        f = open(fileName, "a")
                        f.write(f"{whatSite}, {cuser}, {n_indi_password}\n")
                        f.close()
                        lookOrStore(masterKey, fileName)
                    elif yON == 'n':
                        print("saved data for this website was not manipulated")
                        lookOrStore(masterKey, fileName)
                    else:
                        print("un recognized response please try again ")
                        lookOrStore(masterKey, fileName)

                elif whatToDo == 'd':
                    # example of basic operation 6 Remove
                    print(line)
                    aDo = str(input(
                        "Are you sure you would like to delete this data (type 'y' for yes or 'n' for no): "))
                    if aDo == 'y':
                        print("Data is being removed")
                        deval = line
                        delete_line(masterKey, fileName, deval)
                    elif aDo == 'n':
                        print("saved data for this website was not manipulated")
                        lookOrStore(masterKey, fileName)
                    else:
                        print("un recognized response please try again ")
                        lookOrStore(masterKey, fileName)
                else:
                    print("un recognized response please try again ")
                    lookOrStore(masterKey, fileName)
    else:
        print("No data from that website found")
        lookOrStore(masterKey, fileName)

def delete_line(masterKey,fileName,deval):
    #actual removal of line
    print(deval)
    with open(fileName, 'r+') as f:
        t = f.read()
        to_delete = deval.strip()
        f.seek(0)
        for line in t.split('\n'):
            if line != to_delete:
                f.write(line + '\n')
        f.truncate()
    lookOrStore(masterKey, fileName)


def encrypt(masterKey,file_name):
    f = Fernet(masterKey)
    with open(file_name,'rb') as file:
        original = file.read()
    encrypted = f.encrypt(original)

    with open(file_name, 'wb') as file:
        file.write(encrypted)

def decrypt(masterKey,file_name):
    f = Fernet(masterKey)
    with open(file_name, 'rb') as file:
        encrypted = file.read()
    
    decrypted = f.decrypt(encrypted)

    with open(file_name,'wb') as file:
        file.write(decrypted)



store_password()
