#!/usr/bin/env python3

#Luke Demi - 9/30/2024
#NSSA 221 - System Report Script
#system_report.py is a python script designed to collect and return system information across the organization.

import subprocess #imports the subprocess library to run commands in terminal
import platform #imports the platform library which is helpful for OS functions
import sys #imports the sys library which is used for logging

# Global log file variable
log_file_path = 'system_report.log'
log_file = None

def clear_terminal(): #clears the terminal
	subprocess.run("clear")
	
def new_line(): #creates a new line
	log_and_print("")
	
def log_and_print(message):  # logs and prints a message
	print(message)
	log_file.write(message + '\n')
	
def get_date(): #gets the date and time
	date = subprocess.run("date", capture_output=True, text=True)
	date = str(date.stdout)
	date_string = "System Report - " + date
	log_and_print("\033[91m" + date_string + "\033[0m")
	
def get_hostname(): #gets the hostname
	hostname = subprocess.run("hostname", capture_output=True, text=True)
	hostname = str(hostname.stdout).split(".")[0]
	log_and_print("Hostname: \t\t" + hostname)

def get_domain(): #gets the domain
	domain = subprocess.run("hostname", capture_output=True, text=True)
	domain = str(domain.stdout).split(".")[1]
	log_and_print("Domain: \t\t" + domain)
	
def get_ip_address(): #gets the IPv4 address
	IP = subprocess.run(["ip", "r"], capture_output=True, text=True, check=True)
	IP = str(IP.stdout).split()[8]
	log_and_print("IP Address: \t\t" + IP)

def get_default_gateway(): #gets the default gateway
	gatewayIP = subprocess.run(["ip", "r"], capture_output=True, text=True, check=True)
	gatewayIP = str(gatewayIP.stdout).split()[2]
	log_and_print("Gateway: \t\t" + gatewayIP)
	
def get_network_mask(): #gets the subnet mask
	mask = subprocess.run("ifconfig", capture_output=True, text=True, check=True)
	mask = str(mask.stdout).split()[7]
	log_and_print("Network Mask: \t\t" + mask)
	
def get_dns(): #gets the two DNS servers
	with open("/etc/resolv.conf", "r") as file:
		dns_servers = [line.split()[1] for line in file if line.startswith("nameserver")]
	log_and_print("DNS1: \t\t\t" + str(dns_servers[0]))
	log_and_print("DNS2: \t\t\t" + str(dns_servers[1]))
	
def get_os_info(): #gets the OS, OS Version, and Kernel Version
	os_info = subprocess.run("hostnamectl", capture_output=True, text=True, check=True)
	lines = os_info.stdout.splitlines()
	for line in lines:
		if 'Operating System' in line:
			parts = line.split()
			log_and_print("Operating System: \t" + ' '.join(parts[2:4]))
			log_and_print("Operating Version: \t" + parts[4])
		if 'Kernel' in line:
			parts = line.split()
			log_and_print("Kernel Version: \t" + parts[2])
	
def get_storage_info(): #gets the Hard Drive Capacity and Available Space
	storage_info = subprocess.run(["df", "-h"], capture_output=True, text=True, check=True)
	lines = storage_info.stdout.splitlines()
	for line in lines:
		if '/dev/mapper/rl-root' in line:
			parts = line.split()
			log_and_print("Hard Drive Capacity: \t" + parts[1])
		if '/dev/mapper/rl-root' in line:
			parts = line.split()
			log_and_print("Available Space: \t" + parts[3])
			
def get_processor_info(): #gets the CPU Model, # of Processors, and # of Cores
	processor_info = subprocess.run(["lscpu"], capture_output=True, text=True, check=True)
	lines = processor_info.stdout.splitlines()
	model_name = ''
	num_processors = ''
	num_cores = ''
	printed_processors = False #necessary because there are two lines with the same name
	for line in lines:
		if 'Model name' in line:
			parts = line.split(":")
			model_name = parts[1].strip()
		if 'CPU(s):' in line and not printed_processors: #prevents from printing twice
			parts = line.split(":")
			num_processors = parts[1].strip()
			printed_processors = True
		if 'Core(s) per socket:' in line:
			parts = line.split(":")
			num_cores = parts[1].strip()
	log_and_print("CPU Model: \t\t" + model_name)
	log_and_print("Number of Processors: \t" + num_processors)
	log_and_print("Number of Cores: \t" + num_cores)
	
def get_memory_info(): #gets the Total RAM and Available RAM
	memory_info = subprocess.run(["free", "-h"], capture_output=True, text=True, check=True)
	lines = memory_info.stdout.splitlines()
	for line in lines:
		if 'Mem:' in line:
			parts = line.split()
			log_and_print("Total RAM: \t\t" + parts[1])
			log_and_print("Available RAM: \t\t" + parts[6])

def main():
	global log_file  #Declare log_file as global
	with open(log_file_path, 'w') as log_file_handle:
		log_file = log_file_handle  #Assign the global variable
		clear_terminal()  #startup information
		get_date()

		log_and_print("\033[92mDevice Information\033[m")  #device information
		get_hostname()
		get_domain()

		log_and_print("\033[92mNetwork Information\033[m")  #network information
		get_ip_address()
		get_default_gateway()
		get_network_mask()
		get_dns()
		new_line()

		log_and_print("\033[92mOS Information\033[m")  #operating system information
		get_os_info()
		new_line()

		log_and_print("\033[92mStorage Information\033[m")  #storage information
		get_storage_info()
		new_line()

		log_and_print("\033[92mProcessor Information\033[m")  #processor information
		get_processor_info()
		new_line()

		log_and_print("\033[92mMemory Information\033[m")  #memory information
		get_memory_info()
		new_line()
	
if __name__ == "__main__":
	main()
