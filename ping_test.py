#!/usr/bin/env python3

#Luke Demi - 9/9/2024
#NSSA 221 - Ping Test Script
#ping_test.py is a python script designed to create a user-interactive menu to choose from 5 options:
	#1 - Display the Default Gateway
	#2 - Test Local Connectivity
	#3 - Test Remote Connectivity
	#4 - Test DNS Resolution
	#5 - Exit/Quit the Script
	
import time #used for sleep command which pauses the reset process
import subprocess #used for running linux commands

def display_menu(): #displays the initial menu for the 5 options
	subprocess.run("clear")
	print("\n\t**********************************\n")
	print("\t*****PING TEST TROUBLESHOOTER*****\n")
	print("\t**********************************\n\n")
	print("Enter Selection:\n")
	print("\t1 - Display the Default Gateway\n")
	print("\t2 - Test Local Connectiivty\n")
	print("\t3 - Test Remote Connectivity\n")
	print("\t4 - Test DNS Resolution\n")
	print("\t5 - Exit/Quit the Script\n")

def main():
	while True: #an infinite while loop until a user quits by pressing 5
		display_menu()
		user_choice = input("Enter your desired choice: ")
		if user_choice == "1": #if user chooses to display the default gateway
			try:
				gatewayIP = subprocess.run(["ip", "r"], capture_output=True, text=True, check=True)
				gatewayIP = str(gatewayIP.stdout).split()[2]
				print("The Default Gateway is:", gatewayIP)
				print("Success: Default Gateway displayed.")
			except subprocess.CalledProcessError: #if default gateway cannot be found
				print("Error: Failed to retrieve Default Gateway.")
			time.sleep(3)
		elif user_choice == "2": #if user chooses to test local connectivity
			print("Testing Local Connectivity...")
			result = subprocess.run(["ping", "-c", "3", gatewayIP], capture_output=True)
			if result.returncode == 0:
				print("Success: Local Connectivity test completed successfully.")
			else: #if the ping fails
				print("Error: Local Connectivity test failed.")
			time.sleep(3)
		elif user_choice == "3": #if user chooses to test remote connectivity
			print("Testing Remote Connectivity...")
			result = subprocess.run(["ping", "-c", "3", "129.21.3.17"], capture_output=True)
			if result.returncode == 0:
				print("Success: Remote Connectivity test completed successfully.")
			else: #if the ping fails
				print("Error: Remote Connectivity test failed.")
			time.sleep(3)
		elif user_choice == "4": #if user chooses to test DNS resolution
			print("Testing DNS Resolution...")
			result = subprocess.run(["ping", "-c", "3", "www.google.com"], capture_output=True)
			if result.returncode == 0:
				print("Success: DNS Resolution test completed successfully.")
			else: #if the ping fails
				print("Error: DNS Resolution test failed.")
			time.sleep(3)
		elif user_choice == "5": #if user chooses to quit/exit
			return
		else: #if user chooses something besides the five given options
			print("Invalid Choice, try typing something else instead.")
			time.sleep(3)
		
	
	
if __name__ == "__main__":
	main()
