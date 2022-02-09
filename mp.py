from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
import base64
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import string
import random
import os
import sys,time
os.system("cls") #gunakan untuk windows. ganti ke os.system("clear") untuk linux

COLORS = {\
"black":"\u001b[30;1m",
"red": "\u001b[31;1m",
"green":"\u001b[32m",
"yellow":"\u001b[33;1m",
"blue":"\u001b[34;1m",
"magenta":"\u001b[35m",
"cyan": "\u001b[36m",
"white":"\u001b[37m",
"yellow-background":"\u001b[43m",
"black-background":"\u001b[40m",
"cyan-background":"\u001b[46;1m",
}
#Anda daapt menambahkan warna lain yang anda suka.

def colorText(text):
    for color in COLORS:
        text = text.replace("[[" + color + "]]", COLORS[color])
    return text

def typewriter(message):
    for char in message:
        sys.stdout.write(char)
        sys.stdout.flush()
        
        if char !=  "\n":
            time.sleep(0.001)
        else:
            time.sleep(0.2)


# Functions
# For getting the credentials

def getCredentials():
    # Credentials Input
    websiteName = input(
        "Masukan nama situs web atau aplikasi: ")
    username = input("Masukan username/email: ")
   
    password = input("Masukan password yang ingin anda gunakan:")

    return [websiteName, username, password]


# For getting the master password


def getMasterPassword(case):
    if case==1:
        masterPassword = input(
            "Masukan password utama untuk membuka data enkripsi (mohon untuk tetap mengingatnya):"
        ).encode()
    if case==2:
        masterPassword = input(
                "Masukan passsword utama untuk melanjutkan:").encode()

    return masterPassword


# For deriving the key


def keyDeriving(masterPassword, salt=None):
    # Making a salt file
    if salt != None:
        with open("salt.txt", "wb") as slt:
            slt.write(salt)

    #When the salt file is already present
    elif salt == None:
        try:
            with open("salt.txt","rb") as slt:
                salt = slt.read()
        # If salt file is not found then it has not been created or is removed.
        except FileNotFoundError:
            print()
            print(
               colorText("[[red]]Kesalahan! Tidak ada entri yang ditemukan! Data telah dihapus atau tidak dibuat di tempat pertama.[[white]]")
            )
            quit()
    # One time process of deriving key from master password and salt.

    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(),
                     length=32,
                     salt=salt,
                     iterations=100000,
                     backend=default_backend())
    new_key = base64.urlsafe_b64encode(kdf.derive(masterPassword))

    return new_key


# For writing the data


def writeData(websiteName, username, password, mode):
    s1 = '\n' + 'Site/Apps: ' + websiteName + '\n'
    s2 = 'User login: ' + username + '\n'
    s3 = 'Password: ' + password + '\n'
    # Writing the credentials to a text file.
    with open("credentials.txt", mode) as file:
        file.write(s1 + s2 + s3)


# For encryting the data


def encryptData(key, case):
    f = Fernet(key)

    # Encryption process
    with open("credentials.txt") as file:
        data = file.read()
    encryptedData = f.encrypt(bytes(data, encoding='utf8'))

    with open("credentials.txt", "w") as file:
        file.write(encryptedData.decode())
    if case == 1:
        print()
        print(colorText("[[cyan-background]]Kredensial Anda telah disimpan dengan aman dan di-enkripsi.[[black-background]]"))
        return
    if case == 2:
        quit()
    if case == 3:
        print()
        print(colorText("[[cyan-background]]Selesai Di-enkripsi Kembali![[black-background]]"))


# For decrypting the data


def decryptData(new_key):
    f = Fernet(new_key)
    with open("credentials.txt") as file:
        encryptedData = file.read()

    try:
        decryptedData = f.decrypt(bytes(encryptedData, encoding='utf8'))

        with open("credentials.txt", "w") as file:
            file.write(decryptedData.decode())

        return
    except InvalidToken:
        print('-'*60)
        print(typewriter(colorText("[[red]]Kata sandi salah, silakan coba lagi!\n[[white]]")))
        print('-'*60)
        #helpSection()
        quit()


# Help section


def helpSection():
    print()
    print('-'*60)	
    print(
        "Saat ini, Anda sedang melihat bagian bantuan Manajemen Password (Pengelola kata sandi yang sederhana namun cukup efektif)"
    )
    print('-'*60)	
    print("* Jika Anda pengguna untuk pertama kalinya atau mau memformat ulang data, ketik 'n' untuk new. Pilihan ini memulai data baru kembali. \n")
    print(
        "* Jika Anda pernah menggunakan untuk menyimpan beberapa kata sandi dan ingin melihatnya, ketikkan 'o' untuk Old dan pilih opsi 2 \n"
    )
    print(
        "* Jika Anda pernah menggunakan dan ingin menyimpan kata sandi lain, ketikkan 'o' untuk Old and pilih opsi 1 \n"
    )
    print('-'*60)
    print("Sekarang Anda akan kembali ke menu.")
    print()
    return

# Main program starts from here.
# Greetings!
print('-'*60)
print(typewriter(colorText("[[green]]Halo, selamat datang di [[yellow]]Manajemen Kata Sandi. [[green]]\nIni adalah pengelola kata sandi yang sederhana dan mudah digunakan, \nuntuk menyimpan semua kredensial penting Anda.\n")))
print('-'*60)
 
while True:
    print(colorText("[[yellow-background]][[white]]- Untuk mengetahui lebih banyak, ketik 'h' untuk help"))
    print("- Jika pertama kalinya digunakan atau mau memformat ulang data, Ketik 'n' untuk New")
    print("- Jika sudah pernah digunakan sebelumnya ketik 'o' untuk Old")
    print(colorText("- Jika ingin keluar ketik 'q' untuk Quit[[black-background]]"))
    print()
    userChoice = input("Ketikan pilihan Anda:").lower()

    if userChoice == 'n':

        while True:
            # prompt for ready

            readyOrNot = input(
                "Sekarang kami akan meminta kredensial Anda. Saat siap ketik 'y' jika tidak ketik 'q':"
            )
            # if ready

            if readyOrNot.lower() == "y":
                # input of credentials
                websiteName, username, password = [
                    str(x) for x in getCredentials()
                ]

                # Input for master password
                masterPassword = getMasterPassword(1)

                # One time process
                salt = os.urandom(16)
                key = keyDeriving(masterPassword, salt)

                # writing the data
                writeData(websiteName, username, password, 'w')

                # Encryption process
                encryptData(key, 1)

                break
            elif readyOrNot.lower() == 'q':
                quit()
            else:
                print("Pilihan yang salah!!")
        break
    elif userChoice == 'o':
        print()
        print(
            "\n- Untuk memasukan kredensial baru ketik 1 \n- Untuk melihat kata sandi yang disimpan ketik 2")
        print()
        manageOrStore = input("Ketikkan pilihan Anda:")

        # If user wants to enter new data
        if manageOrStore == '1':

            masterPassword=getMasterPassword(2)

            new_key = keyDeriving(masterPassword)

            decryptData(new_key)

            while True:
                readyOrNot = input(
                    "Sekarang kami akan meminta kredensial Anda. Saat siap ketik 'y' jika tidak ketik 'q': "
                )
                if readyOrNot.lower() == "y":

                    websiteName, username, password = [
                        str(x) for x in getCredentials()
                    ]

                    writeData(websiteName, username, password, 'a')

                    encryptData(new_key, 1)

                    break

                # If user wants to quit
                elif readyOrNot.lower() == 'q':
                    encryptData(new_key, 2)

        # If user wants to view stored data
        if manageOrStore == '2':

            masterPassword=getMasterPassword(2)

            new_key = keyDeriving(masterPassword)
            decryptData(new_key)
            f = open("credentials.txt", "r")
            print()
            print(
                colorText("[[yellow]]File data sekarang di-dekripsi dan Anda dapat membukanya untuk melihat kredensial Anda.[[white]]")
            )
            print('-'*60)
            print(f.read())
            print('-'*60)
            while True:
                inp = input(colorText("[[yellow]]Setelah selesai ketik 'q' untuk meng-enkripsi kembali file data yang tersimpan: [[white]]"))
                if inp.lower() == 'q':
                    encryptData(new_key, 3)
                    break
                elif inp.lower() != 'q':
                     encryptData(new_key, 2)
        break

    elif userChoice == 'h':
        helpSection()
    elif userChoice == 'q':
        quit()	
    else:
        print("Pilihan Salah, Anda akan dikirim ke bagian bantuan sekarang")
        helpSection()