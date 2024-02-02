#!/bin/bash

# Help
function help_panel(){
    echo -e "\n\n\t- Run '$0 -i' to isolate the host."
    echo -e "\t- Run '$0 -u' to undo-isolation.\n\n"
}

# Global Vars
declare -a endpoints=('sumologic.com' 'velo.dobliuw.io' 'cdn-dobliuw.nyc3.digitaloceanspaces.com' 'cdn-dobliuw.nyc3.cdn.digitaloceanspaces.com' 'pairing.dobliuw.io' 'api.dobliuw.io')
declare -a ips
declare -r service_begin="[Unit]\nDescription=Isolate Host\n\n[Service]\nType=simple"
declare -r service_end="\n[Install]\nWantedBy=default.target"
mkdir_cmd=$(which mkdir)
awk_cmd=$(which awk)
base64_cmd=$(which base64)
cp_cmd=$(which cp)
cat_cmd=$(which cat)
head_cmd=$(which head)
tail_cmd=$(which tail)
rm_cmd=$(which rm)
dig_cmd=$(which dig)
tr_cmd=$(which tr)
tee_cmd=$(which tee)
grep_cmd=$(which grep)
find_cmd=$(which find)
readlink_cmd=$(which readlink)
sed_cmd=$(which sed)
timeout_cmd=$(which timeout)
sleep_cmd=$(which sleep)
chmod_cmd=$(which chmod)
systemctl_cmd=$(which systemctl)
iptable_cmd=$(which iptables)
iptables_save=$(which iptables-save)
iptables_restore=$(which iptables-restore)
isolate_path="$($readlink_cmd -f "$0")"
rclocal_path=$($find_cmd / -name "rc.local" 2>/dev/null)

# Verify if iptables and tools needed exists in the linux server
function check_firewall(){
    if [[ "$iptable_cmd" && "$iptables_save" && "$iptables_restore" ]];then  
        if [ ! -e "/etc/dobliuw/.../fw_conf_bp.conf" ]; then 
            $iptables_save > "/etc/dobliuw/.../fw_conf_bp.conf" && $chmod_cmd 600 '/etc/dobliuw/.../fw_conf_bp.conf'
        fi
        return 0
    else
        exit 1 
    fi
}

# Add the domains and their ips
function config_hosts(){
    domain=$1
    shift
    local ips_for_domain=$@
    echo "$ips_for_domain $domain" >> "/etc/hosts"
}

# Block all coneccions and config succesfull trafic with dobliuw domains & ips
function config_firewall(){
    if [ ! -e "/etc/dobliuw/.../hosts_bp.conf" ]; then
        $cp_cmd '/etc/hosts' '/etc/dobliuw/.../hosts_bp.conf' && $chmod_cmd 600 '/etc/dobliuw/.../hosts_bp.conf'
        $cat_cmd '/etc/dobliuw/.../hosts_bp.conf' | $head_cmd -n 5 > '/etc/hosts'

        endpoints+=($($cat_cmd /etc/dobliuw/dobliuw.conf  | $grep_cmd server | $awk_cmd 'NF{print $NF}' | $sed_cmd 's/https\?\:\/\///g' | $tr_cmd -d "\"" | $awk_cmd '{print $1}' FS=':'))

        for domain in ${endpoints[@]}; do
            $sleep_cmd 2
            ip=$($timeout_cmd 10 $dig_cmd +short $domain 2>/dev/null | $tr_cmd '\n' ' ')
            error=$(echo "$ip" | $grep_cmd -iE "timed|out|communication|#|;;")
            if [ ! "$error" ]; then 
                ips+="$ip"
                config_hosts "$domain" "$ip"
            fi
        done

    else
        ips=($($cat_cmd '/etc/hosts' | $tail_cmd -n +6 | $grep_cmd -oP '\d{0,3}\.\d{0,3}\.\d{0,3}\.\d{0,3}' | $tr_cmd '\n' ' '))
    fi
    $sleep_cmd 1
    echo -e "\n[i] File /etc/hosts configurated."

    # Block all coneccions
    $iptable_cmd -P INPUT DROP  
    $iptable_cmd -P OUTPUT DROP
    #$iptable_cmd -P FORWARD DROP   <- Ojo
    # Allow loopback trafic
    $iptable_cmd -I INPUT -i lo -j ACCEPT
    $iptable_cmd -I OUTPUT -o lo -j ACCEPT
    # Allow connections with allowed endpoints
    for ip in ${ips[@]}; do
        #echo "Ip: $ip"
        $iptable_cmd -I INPUT -s "$ip" -j ACCEPT
        $iptable_cmd -I OUTPUT -d "$ip" -j ACCEPT
    done
    $sleep_cmd 1
    echo -e "\n[i] Firewall succesfully configurated. The all connections was blocked."
}

# # Change the DNS Server for invalid one
# function config_dns(){
#     if [ ! -e "/etc/dobliuw/.../dns_bp.conf" ]; then
#     fi
#     # Make backup in /etc/dobliuw/...
#     $cp_cmd '/etc/resolv.conf' '/etc/dobliuw/.../dns_bp.conf' && $chmod_cmd 600 '/etc/dobliuw/.../dns_bp.conf'
#     # Change DNS address
#     echo 'nameserver 127.0.0.45' > /etc/resolv.conf
#     $sleep_cmd 1
#     echo -e "\n[i] The DNS Server was changed."
# }

# Make persistence with rc.local or systemd 
function configure_boot(){
    
    if [ "$rclocal_path" ]; then
        if [ ! -e "/etc/dobliuw/.../rclocal_bc.conf" ]; then
            # Make a rclocal backup and add an execution script isolate line
            $cp_cmd $rclocal_path '/etc/dobliuw/.../rclocal_bc.conf'
            $cat_cmd $rclocal_path | $sed_cmd 's/exit 0//' | $tee_cmd $rclocal_path &>/dev/null
            echo -e "bash $isolate_path\nexit 0" >> $rclocal_path
            echo -e "\n[i] rc.local successfully configurated"
        fi
    else
        if [ ! -e "/etc/systemd/system/isolate_unix.service" ]; then
            declare -r service_path='/etc/systemd/system/isolate_unix.service'
            # Create an isoalte-service and enable it 
            echo -e $service_begin > $service_path && $chmod_cmd 664 $service_path
            echo "ExecStart=/bin/bash $isolate_path -i" >> $service_path # Replace for $isolate_path
            echo -e $service_end >> $service_path
            # Enable and start the service created
            $systemctl_cmd enable isolate_unix.service
            echo -e "\n[i] Service isolate_unix successfully created"
        #else
           # $systemctl_cmd start isolate_unix.service
            #echo -e "\n[i] Service isolate_unix started"
        fi
    fi
}

# Restore the original Firewall conf
function restore_firewall_config(){   #TODO Consultar "backup" (Endpoint API dobliuw backup)
    $iptable_cmd -F
    $iptables_restore < "/etc/dobliuw/.../fw_conf_bp.conf"
    $rm_cmd '/etc/dobliuw/.../fw_conf_bp.conf'
    $sleep_cmd 1 
    echo -e "\n[i] Firewall configuration restored"
}

# Restore the original DNS Server address
function restore_dns(){
    $cp_cmd '/etc/dobliuw/.../dns_bp.conf' '/etc/resolv.conf'
    #$iptable_cmd -A OUTPUT -p udp --dport 53 -j ACCEPT
    $rm_cmd '/etc/dobliuw/.../dns_bp.conf'
    $sleep_cmd 1 
    echo -e '\n[i] DNS Server address restored'
}

function restore_hosts(){
    $cp_cmd '/etc/dobliuw/.../hosts_bp.conf' '/etc/hosts'
    $rm_cmd '/etc/dobliuw/.../hosts_bp.conf'
    $sleep_cmd 1 
    echo -e "\n[i] File /etc/hosts restored"
}

function restore_boot(){
    if [ "$rclocal_path" ]; then
        $cp_cmd '/etc/dobliuw/.../rclocal_bc.conf' $rclocal_path
        echo -e "\n[i] rc.local restored"
    else
        $rm_cmd '/etc/systemd/system/isolate_unix.service'
        $systemctl_cmd daemon-reload
        echo -e "\n[i] Service isolate_unix deleted"
    fi
}

# Main script
declare -i pointer=0

while getopts "iuh" arg; do
    case $arg in 
    i) let pointer+=1;;
    u) let pointer+=2;;
    h) ;;
    esac
done


if [ $EUID -ne 0 ]; then
    echo -e "\n\t[!] This script needs run like sudo ツ\n"
    exit 1
else

    if [ "$pointer" -eq 1 ]; then
        $mkdir_cmd -p '/etc/dobliuw/...' 2>/dev/null # Change dobliuw path 
        check_firewall 

        if [ "$?" -eq 0 ]; then
            $sleep_cmd 1
            echo -e "\n\t[+] Starting the isolation..."
            config_firewall

            if [ "$?" -eq 0 ]; then
                configure_boot
                echo -e "\n\t[+] Host isolated successfully.\n"
                exit 0 
            else
                echo -e "\n\n\t[!] An error ocurred configurating the firewall.\n"
                exit 1 
            fi
        else
            echo -e "\n\n\t[!] The firewall or some tool relationated isn't installed.\n"
            exit 1 
        fi
    # # If the script was execute with -u
    elif [ "$pointer" -eq 2 ]; then    
        $sleep_cmd 1 
        echo -e "\n\t[+] Starting with the undo-isolation"
        restore_hosts
        if [ "$?" -eq 0 ]; then
                restore_firewall_config   
                if [ "$?" -eq 0 ]; then
                    restore_boot
                    if [ "$?" -eq 0 ]; then 
                        echo -e "\n\t[+] Host succesfully recovered."
                        exit 0
                    else 
                        echo -e "\n\t[!] An error ocurred deleting the service / rc.local"
                        exit 1
                    fi 
                else 
                    echo -e "\n\t[!] An error ocurred recovering the iptables rules.\n"
                    exit 1 
                fi
        else 
            echo -e "\n\t[!] An error ocurred recovering the /etc/hosts file.\n"
            exit 1 
        fi
    else 
        help_panel
    fi
fi 