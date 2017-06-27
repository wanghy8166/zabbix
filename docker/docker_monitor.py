#!/usr/bin/env python
#-*- coding: utf-8 -*-
from docker import APIClient
import sys
import subprocess
import os
 
def check_container_stats(container_name,collect_item):
    container_collect=docker_client.stats(container_name)
    old_result=eval(container_collect.next())
    new_result=eval(container_collect.next())
    container_collect.close()
    if collect_item == 'cpu_total_usage':
        result=new_result['cpu_stats']['cpu_usage']['total_usage'] - old_result['cpu_stats']['cpu_usage']['total_usage']
    elif collect_item == 'cpu_system_usage':
        result=new_result['cpu_stats']['system_cpu_usage'] - old_result['cpu_stats']['system_cpu_usage']
    elif collect_item == 'cpu_percent':
        cpu_total_usage=new_result['cpu_stats']['cpu_usage']['total_usage'] - old_result['cpu_stats']['cpu_usage']['total_usage']
        cpu_system_uasge=new_result['cpu_stats']['system_cpu_usage'] - old_result['cpu_stats']['system_cpu_usage']
        cpu_num=len(old_result['cpu_stats']['cpu_usage']['percpu_usage'])
        result=round((float(cpu_total_usage)/float(cpu_system_uasge))*cpu_num*100.0,2)
    elif collect_item == 'mem_usage':
        result=new_result['memory_stats']['usage']
    elif collect_item == 'mem_limit':
        result=new_result['memory_stats']['limit']
    elif collect_item == 'mem_percent':
        mem_usage=new_result['memory_stats']['usage']
        mem_limit=new_result['memory_stats']['limit']
        result=round(float(mem_usage)/float(mem_limit)*100.0,2)
    elif collect_item == 'network_rx_bytes':
        network_check_command="""sudo /usr/bin/docker exec %s cat /proc/net/dev|sed -n 3p|awk '{print $2,$10}'"""%container_name
        result=os.popen(network_check_command).read().split()[0]
    elif collect_item == 'network_tx_bytes':
        network_check_command="""sudo /usr/bin/docker exec %s cat /proc/net/dev|sed -n 3p|awk '{print $2,$10}'"""%container_name
        result=os.popen(network_check_command).read().split()[1]
    return result
if __name__ == "__main__":
    docker_client = APIClient(base_url='unix://var/run/docker.sock')
    container_name=sys.argv[1]
    collect_item=sys.argv[2]
    print check_container_stats(container_name,collect_item)