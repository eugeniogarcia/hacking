#!/usr/bin/env python
import nmap # import nmap.py module

nm = nmap.PortScanner() # instantiate nmap.PortScanner object

resultado=nm.scan('127.0.0.1', '22-443') # scan host 127.0.0.1, ports from 22 to 443

print("Comando")
print(nm.command_line()) # get command line used for the scan : nmap -oX - -p 22-443 127.0.0.1
print("\n")

info=nm.scaninfo() # get nmap scan informations {'tcp': {'services': '22-443', 'method': 'connect'}}
print("Metodo y puertos escaneados")
print(info)
print("\n")

print("Hosts scaneados")
hosts=nm.all_hosts()
print(hosts) # get all hosts that were scanned
print("\n")

print("Restulado del Scaneado")
print(resultado)
print("\n")

print("Datos")
print("Host names")

print(nm['127.0.0.1'].hostname()) # get one hostname for host 127.0.0.1, usualy the user record
print(nm['127.0.0.1'].hostnames()) # get list of hostnames for host 127.0.0.1 as a list of dict
# [{'name':'hostname1', 'type':'PTR'}, {'name':'hostname2', 'type':'user'}]
print("\n")

print("Estado")
print(nm['127.0.0.1'].state()) # get state of host 127.0.0.1 (up|down|unknown|skipped)
print("\n")

print("Protocolos")
print(nm['127.0.0.1'].all_protocols()) # get all scanned protocols ['tcp', 'udp'] in (ip|tcp|udp|sctp)
print(nm['127.0.0.1']['tcp'].keys()) # get all ports for tcp protocol
print("\n")

print("Puertos por protocolo")
print("tcp: ",nm['127.0.0.1'].all_tcp()) # get all ports for tcp protocol (sorted version)
print("udp: ",nm['127.0.0.1'].all_udp()) # get all ports for udp protocol (sorted version)
print("ip: ",nm['127.0.0.1'].all_ip()) # get all ports for ip protocol (sorted version)
print("sctp: ",nm['127.0.0.1'].all_sctp()) # get all ports for sctp protocol (sorted version)
print("\n")

print("Informacion del puerto 80")
print(nm['127.0.0.1'].has_tcp(80)) # is there any information for port 80/tcp on host 127.0.0.1
print(nm['127.0.0.1']['tcp'][80]) # get infos about port 80 in tcp on host 127.0.0.1
print(nm['127.0.0.1'].tcp(80)) # get infos about port 80 in tcp on host 127.0.0.1
print(nm['127.0.0.1']['tcp'][80]['state']) # get state of port 80/tcp on host 127.0.0.1 (open
print("\n")

# a more usefull example :
for host in nm.all_hosts():
    print('\n--------------------')
    print('Host : %s (%s)' % (host, nm[host].hostname()))
    print('State : %s' % nm[host].state())

    for proto in nm[host].all_protocols():
        print('--------------------')
        print('Protocol : %s' % proto)
    
        lport = nm[host][proto].keys()

        for port in lport:
            print('port : %s\tstate : %s' % (port, nm[host][proto][port]['state']))

print('\n--------------------')
# print result as CSV
print(nm.csv())


print('\--------------------')
# If you want to do a pingsweep on network 192.168.1.0/24:
nm.scan(hosts='192.168.1.0/24', arguments='-n -sP -PE -PA21,23,80,3389')

hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

for host, status in hosts_list:
    print('{0}:{1}'.format(host, status))


print('\n--------------------')

# Asynchronous usage of PortScannerAsync
nma = nmap.PortScannerAsync()

def callback_result(host, scan_result):
    print('--------------------')
    print(host, scan_result)
    nma.scan(hosts='192.168.1.0/30', arguments='-sP', callback=callback_result)
    while nma.still_scanning():
        print("Waiting ...")
        nma.wait(2) # you can do whatever you want but I choose to wait after the end of the scan
