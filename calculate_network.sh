#!/bin/bash 
 
#Colours
greenColour="\e[0;32m\033[1m"
endColour="\033[0m\e[0m"
redColour="\e[0;31m\033[1m"
blueColour="\e[0;34m\033[1m"
yellowColour="\e[0;33m\033[1m"
purpleColour="\e[0;35m\033[1m"
turquoiseColour="\e[0;36m\033[1m"
grayColour="\e[0;37m\033[1m"

# Help 
function help(){
	echo -e "\n\n\t${redColour}[!]${endColour} ${grayColour}Uso:${endColour} ${purpleColour}$0${endColour} ${yellowColour}{target_ip}/{bits}${endColour}"
	echo -e "\t${grayColour}Example${endColour} ${yellowColour}-->${endColour} ${purpleColour}$0${endColour} ${yellowColour}192.168.1.36/24${endColour}\n\n"
	exit 0  
}

# Exec 

function main(){
  ip=$1
  cidr=$(echo $ip | /usr/bin/tr "/" " " | /usr/bin/awk '{print $2}')
  maxbits=32
  exist=$(/bin/which ipcalc)
  if [ ! $ip ]; then 
	  help
  fi
  if [ ! $exist ]; then
	if [[ $EUID -ne 0 ]]; then 
	  echo -e "\n\n\t${redColour}Necesita ejecutarse como sudo :)${endColour}\n\n" 
	  exit 1;
	fi
	  apt install ipcalc 
  fi 
  netmask=$(/bin/ipcalc -n $ip | /usr/bin/cut -f2 -d/ | /bin/grep -i netmask: | /usr/bin/awk '{print $2}')
  broadcast=$(/bin/ipcalc -n $ip | /usr/bin/cut -f2 -d/ | /bin/grep -i broadcast: | /usr/bin/awk '{print $2}')
  totalHosts=$( echo "2^$(($maxbits - $cidr)) - 2" | bc)

  IFS=. read -r i1 i2 i3 i4 <<< "$(echo $ip | /usr/bin/tr "/" " " | /usr/bin/awk '{print $1}')"
  IFS=. read -r m1 m2 m3 m4 <<< "$netmask"
  networkID=$((i1 & m1)).$((i2 & m2)).$((i3 & m3)).$((i4 & m4))

  echo -e "\n\n\t${grayColour}Subnet values for${endColour} ${purpleColour}->${endColour} ${yellowColour}$ip${endColour}"
  echo -e "\t${purpleColour}------------------------------------${endColour}"
  echo -e "\t${yellowColour}(!)${endColour} ${grayColour}Netmask:${endColour} ${purpleColour}$netmask${endColour}"
  echo -e "\t${yellowColour}(!)${endColour} ${grayColour}Total Hosts:${endColour} ${purpleColour}$totalHosts${endColour}"
  echo -e "\t${yellowColour}(!)${endColour} ${grayColour}Network ID:${endColour} ${purpleColour}$networkID${endColour}"
  echo -e "\t${yellowColour}(!)${endColour} ${grayColour}Broadcast Address:${endColour} ${purpleColour}$broadcast${endColour}\n\n"
}

main $1