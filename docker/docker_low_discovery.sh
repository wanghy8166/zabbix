#!/bin/bash
#Fucation:docker low-level discovery
docker() {
            port=($(sudo docker ps -a|grep -v "CONTAINER ID"|awk '{print $NF}'))
            printf '{\n'
            printf '\t"data":[\n'
               for key in ${!port[@]}
                   do
                       if [[ "${#port[@]}" -gt 1 && "${key}" -ne "$((${#port[@]}-1))" ]];then
                          printf '\t {\n'
                          printf "\t\t\t\"{#CONTAINERNAME}\":\"${port[${key}]}\"},\n"
  
                     else [[ "${key}" -eq "((${#port[@]}-1))" ]]
                          printf '\t {\n'
                          printf "\t\t\t\"{#CONTAINERNAME}\":\"${port[${key}]}\"}\n"
  
                       fi
               done
  
                          printf '\t ]\n'
                          printf '}\n'
}
case $1 in
docker)
docker
;;
*)
echo "Usage:`basename $0` {docker}"
;;
esac