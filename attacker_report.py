#!/usr/bin/env python3

#Luke Demi - 10/30/2024
#NSSA 221 - Attacker Report Script
#attacker_report.py is a python script designed to analyze logs and highlight IP addresses with 10 or more failed login attempts
	#This will also include the number of attempts, country of origin, and the report's date
	
import re #Used for regexing log files
import os #Used for running linux commands
import subprocess #Used for running linux commands
from geoip import geolite2

def get_date():
	date = subprocess.run("date", capture_output=True, text=True)
	date = str(date.stdout)
	return date
	
def parse_log():
	log_file_path = '/home/student/scripts/syslog.log' #Hardcodes log file path
	ip_regex = re.compile(r'(\d+\.\d+\.\d+\.\d+)') #Creates a pattern that can capture IP addresses
	ip_attempts = {} #Initializes a python dictionary
	
	with open(log_file_path, 'r') as file:
		for line in file:
			if "Failed" in line: #Searching for Failed login attempts
				match_found = ip_regex.search(line)
				if match_found:
					ip_address = match_found.group(1) #Gets the matched IP address
					ip_attempts[ip_address] = ip_attempts.get(ip_address, 0) + 1 #Increments the count of attempts for this IP address
	return ip_attempts
	
def filter_ips(ip_attempts):
	filtered_ips = {}
	for ip, count in ip_attempts.items(): #Goes through all the IP's added
		if count >= 10:
			filtered_ips[ip] = count; #Only adds the IP's to the dictionary if there was over 10 failed login attempts
	return filtered_ips
	
def find_country(ip):
	match_found = geolite2.lookup(ip)
	if match_found:
		return match_found.country
	else:
		return "Unknown"
	
def display_report(ip_attempts):
	print("\033[1;92mAttacker Report - \033[0m" + get_date())
	filtered_ip_attempts = filter_ips(ip_attempts)
	sorted_ip_attempts = dict(sorted(filtered_ip_attempts.items(), key=lambda x: x[1])) #Sorts by ascending order
	print("\033[1;91mCOUNT\tIP ADDRESS\tCOUNTRY\033[0m")
	for ip, count in sorted_ip_attempts.items():
		country = find_country(ip) #Finds the country from the IP address
		print(f"{count}\t{ip}\t" + country)  #Print IPs and their count in a readable format			
def main():
	os.system("clear") #Clears the terminal
	ip_attempts = parse_log()
	display_report(ip_attempts)
	
if __name__ == "__main__":
	main()
