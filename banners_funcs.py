from termcolor import colored
import time, os

def skull_banner():
    banner = """
          :=+*######**+=-.              
       =#@@@@@@@@@@@@@@@@@@*:           
     :%@@@@@@@@@@@@@@@@@@@@@@*          
    :@@@@@@@@@@@@@@@@@@@@@@@@@:         
    %@@@@@%***%@@@@@%#%@@@@@@@.         
    @@@@@-     -@@#.    -@@@@*          
    +@@@*   $   #@   $   -@@*           
     +@@#       %@       =@+          ________        ___.   .__  .__               
      =@@#-. .-%@@#:    =@+           \______ \   ____\_ |__ |  | |__|__ ____  _  __ 
     .@@@@@@@@@=.:%@@@@@@@@=           |    |  \ /  _ \| __ \|  | |  |  |  \ \/ \/ /  
      +#@@@@@@.   -@@@@@@@+.      By   |    `   (  <_> | \_\ |  |_|  |  |  /\     / 
        =@@@@@#@@*#@@@@@#             /_______  /\____/|___  |____|__|____/  \/\_/        
        #@@@@@@@@@@@@@@@:                     \/           \/          
     *+ =@@#@@@@+@@@%%@%  =*.            
    %@@#-..  =+: .=+. :.-#@@%                
 .=%@@@@@@#=.       .=#@@@@@@%=.        
 .++===+*#@@@@*=:=*%@@@#*+===++.        
  ..       :*@@@@@@@*-       ..         
 -@@@%%%%@@@%*-. .-*%@@@%%%%@@@=        
  #@@@@@@*-           -*@@@@@@#         
   :@@%-                 -%@@:          
   :@@.                   .@@:          
      
      
"""
    for line in banner.split('\n'):
        print(colored(line, 'red'))
        time.sleep(0.1)

    time.sleep(1)
    os.system("clear" if os.name == 'posix' else 'cls')

# ARP Spoofer 
def arp_spoofer():
    print(colored("""
   _____ ____________________    _________                     _____             
  /  _  \\\\______   \______   \  /   ___________   ____   _____/ ____\___________ 
 /  /_\  \|       _/|     ___/  \_____  \\\\____ \ /  _ \ /  _ \   ___/ __ \_  __ \\
/    |    |    |   \|    |      /        |  |_> (  <_> (  <_> |  | \  ___/|  | \/
\____|__  |____|_  /|____|     /_______  |   __/ \____/ \____/|__|  \___  |__|   
        \/       \/                    \/|__|                           \/        By Dobliuw ツ
""" ,"red"))

# DNS Sniffer
def dns_sniffer_banner():
    print(colored("""
________   _______    _________   _________      .__  _____  _____             
\______ \  \      \  /   _____/  /   _____/ ____ |___/ _____/ ____\___________ 
 |    |  \ /   |   \ \_____  \   \_____  \ /    \|  \   __\\\\   ___/ __ \_  __ \\
 |    `   /    |    \/        \  /        |   |  |  ||  |   |  | \  ___/|  | \/
/_______  \____|__  /_______  / /_______  |___|  |__||__|   |__|  \___  |__|   
        \/        \/        \/          \/     \/                     \/       By Dobliuw ツ
""", "green"))

# HTTP Sniffer
def http_sniffer_banner():
    print(colored("""
.__     __    __             _________      .__  _____  _____             
|  |___/  |__/  |_______    /   _____/ ____ |___/ _____/ ____\___________ 
|  |  \   __\   __\____ \   \_____  \ /    \|  \   __\\\\   ___/ __ \_  __ \\
|   Y  |  |  |  | |  |_> >  /        |   |  |  ||  |   |  | \  ___/|  | \/
|___|  |__|  |__| |   __/  /_______  |___|  |__||__|   |__|  \___  |__|   
     \/           |__|             \/     \/                     \/        By Dobliuw ツ
""", "green"))

# HTTPS Sniffer
def https_sniffer_banner():
    print(colored("""
.__     __    __                   _________      .__  _____  _____             
|  |___/  |__/  |_______  ______  /   _____/ ____ |__|/ ____\/ ____\___________ 
|  |  \   __\   __\____ \/  ___/  \_____  \ /    \|  \   __\\\\   __\/ __ \_  __ \\
|   Y  \  |  |  | |  |_> >___ \   /        \   |  \  ||  |   |  | \  ___/|  | \/
|___|  /__|  |__| |   __/____  > /_______  /___|  /__||__|   |__|  \___  >__|   
     \/           |__|       \/          \/     \/                     \/       By Dobliuw ツ
""", "green"))


# ICMP Banner
def icmp_scan_banner():
    print(colored("""
.___                          _________                                         
|   | ____   _____ ______    /   _____/ ____ _____    ____   ____   ___________ 
|   |/ ___\ /     \\\\____ \   \_____  \_/ ___\\\\__  \  /    \ /    \_/ __ \_  __ \\
|   \  \___|  Y Y  \  |_> >  /        \  \___ / __ \|   |  \   |  \  ___/|  | \/
|___|\___  >__|_|  /   __/  /_______  /\___  >____  /___|  /___|  /\___  >__|   
         \/      \/|__|             \/     \/     \/     \/     \/     \/        By Dobliuw ツ

""", 'green'))
    

# MAC Changer Banner
def mac_changer_banner():
    print(colored("""
                               .__                                        
  _____ _____    ____     ____ |  |__ _____    ____    ____   ___________ 
 /     \\\\__  \ _/ ___\  _/ ___\|  |  \\\\__  \  /    \  / ___\_/ __ \_  __ \\
|  Y Y  \/ __ \\\\  \___  \  \___|   Y  \/ __ \|   |  \/ /_/  >  ___/|  | \/
|__|_|  (____  /\___  >  \___  >___|  (____  /___|  /\___  / \___  >__|   
      \/     \/     \/       \/     \/     \/     \//_____/      \/        By Dobliuw ツ ...                 
""", 'green'))
    

# ARP Scanner Banner
def arp_scan_banner():
    print(colored("""
   _____ ____________________    _________                     
  /  _  \\\\______   \______   \  /   _____/ ____ _____    ____  
 /  /_\  \|       _/|     ___/  \_____  \_/ ___\\\\__  \  /    \ 
/    |    |    |   \|    |      /        \  \___ / __ \|   |  \\
\____|__  |____|_  /|____|     /_______  /\___  (____  |___|  /
        \/       \/                    \/     \/     \/     \/    By Dobliuw ツ

""", 'green'))
    
# Port Scan Banner
def port_scan_banner():
    print(colored("""
$$$$$$$\                    $$\            $$$$$$\                            
$$  __$$\                   $$ |          $$  __$$\                           
$$ |  $$ |$$$$$$\  $$$$$$\$$$$$$\         $$ /  \__|$$$$$$$\$$$$$$\ $$$$$$$\  
$$$$$$$  $$  __$$\$$  __$$\_$$  _|        \$$$$$$\ $$  _____\____$$\$$  __$$\ 
$$  ____/$$ /  $$ $$ |  \__|$$ |           \____$$\$$ /     $$$$$$$ $$ |  $$ |
$$ |     $$ |  $$ $$ |      $$ |$$\       $$\   $$ $$ |    $$  __$$ $$ |  $$ |
$$ |     \$$$$$$  $$ |      \$$$$  |      \$$$$$$  \$$$$$$$\$$$$$$$ $$ |  $$ |
\__|      \______/\__|       \____/        \______/ \_______\_______\__|  \__|
                                                                              
                                                                  By Dobliuw ツ ...                     
""", 'green'))