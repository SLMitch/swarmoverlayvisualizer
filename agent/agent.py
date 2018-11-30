#Run this script on the hosts running the Docker Engine. The script will report the services with listening ports and the input chain firewall status to the database.
#Run the script on a set interval using crontab.
#Please change the address of the webserver.

webserver = "http://webserver"
import subprocess
import os
import requests
import json
import socket

def get_containers_running():
    return (subprocess.getoutput("docker ps | cut -d \' \' -f 1 | tail -n +2"))

def get_pid_for_container(container):
        return (subprocess.getoutput("docker inspect -f \'{{.State.Pid}}\' %s" % container))

def get_open_ports(pid):
        return (subprocess.getoutput("nsenter -t %s -n netstat -ntlpu | tail -n +3" % pid))

def get_iptables(pid):
    return (subprocess.getoutput("nsenter -t %s -n iptables -L" % pid))

for container in get_containers_running().split(os.linesep):
     print (get_pid_for_container(container))
     netstatoutput = get_open_ports(get_pid_for_container(container)).split("\n")
     for line in netstatoutput:
        line_list = line.split()
        data = {}
        data['host'] = socket.gethostname()
        data['container'] = container
        data['protocol'] = line_list[0]
        data['localaddress'] = line_list[3]
        data['foreignaddress'] = line_list[4]
        data['program'] = line_list[-1]
        json_data = json.dumps(data, ensure_ascii = 'False')
        r = requests.post(webserver + '/openportreporter.php',verify=False, json=json_data)
        headers = {'Content-type': 'application/json'}

     iptablesoutput = get_iptables(get_pid_for_container(container)).split(os.linesep)
     print(container)
     if iptablesoutput[0] == "Chain INPUT (policy ACCEPT)":
         policy = "ACCEPT"
     if iptablesoutput[0] == "Chain INPUT (policy DROP)":
         policy = "DROP"
     data = {}
     data['host'] = socket.gethostname()
     data['container'] = container
     data['inputpolicy'] = policy
     print(data)
     json_data = json.dumps(data, ensure_ascii='False')
     r = requests.post(webserver + '/firewallreporter.php', verify=False, json=json_data)
     headers = {'Content-type': 'application/json'}