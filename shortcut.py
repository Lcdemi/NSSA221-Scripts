#!/usr/bin/env python3

#Luke Demi - 10/17/2024
#NSSA 221 - Shortcut Script
#shortcut.py is a python script designed for easy file access and managing different library versions
	#1 - Display the Default Gateway
	#2 - Test Local Connectivity
	#3 - Test Remote Connectivity
	
import time #Used for sleep command which pauses the reset process
import subprocess #Used for running linux commands
import os #Used for running linux commands
from alive_progress import alive_bar #Used for the progress bar

def clear_terminal(): #Clears the terminal
	subprocess.run("clear")
	
def progress_bar(): #Displays a progress bar
	with alive_bar(3, title='Processing', length=20) as bar:
		for _ in range(3):
			time.sleep(1)  # Sleep for 1 second per iteration
			bar()  # Update the progress bar

def display_menu(): #Displays the initial menu for the 3 options
	clear_terminal()
	print("\n\t**********************************")
	print("\t*********Shortcut Creater*********")
	print("\t**********************************\n")
	print("Enter Selection:\n")
	print("\t1 - Create a shortcut in your home directory.")
	print("\t2 - Remove a shortcut from your home directory.")
	print("\t3 - Run shortcut report.\n")

def shortcut_report_menu(): #Displays the shortcut report menu
	clear_terminal()
	print("\n\t**********************************")
	print("\t*********Shortcut  Report*********")
	print("\t**********************************\n\n")
	
def get_home_directory(): #Gets the home directory
	return os.path.expanduser("~")
    
def create_shortcut(): #Creates a new shortcut
	home = get_home_directory() #Gets home directory
	desktop = os.path.join(home, "Desktop") #Gets the desktopo for shortcuts
	target_file = input("Please enter the file name to create a shortcut: ")

	try: #Trying to find target file
		result = subprocess.run(['find', home, '-name', target_file], capture_output=True, text=True, check=True)
		paths = result.stdout.strip().split('\n')

	except subprocess.CalledProcessError: #Error handling
		print("Sorry, couldn't find " + target_file)
		print("Returning to Main Menu...")
		return
		
	target_path = paths[0] #Uses the first found path	
	if not os.path.exists(target_path): #If the file cant be found
		print("Searching, please wait...")
		progress_bar()
		print("Sorry, couldn't find " + target_file)
		print("Returning to Main Menu...")
		return

	shortcut_selection = input("Found " + target_path + ". Select Y/y to create shortcut: ")
	if shortcut_selection == "Y" or shortcut_selection == "y":
		print("Creating Shortcut, please wait...")
		progress_bar()
		shortcut_path = os.path.join(desktop, target_file)
		try: #Trying to create a new shortcut
			os.symlink(target_path, shortcut_path)
			print("Shortcut created, returning to Main Menu.")
		except FileExistsError: #Shortcut already exists
			print("Error: A shortcut with that name already exists.")
			return
		except Exception as e: #Error handling
			print("Error: {e}")
			return
	else:
		print("Exiting...")
		return
			
def remove_shortcut(): #Removes a shortcut
	home = get_home_directory() #Gets home directory
	desktop = os.path.join(home, "Desktop") #Gets desktop for shortcuts
	shortcut_name = input("Please enter the shortcut/link to remove: ")
	
	shortcuts = [f for f in os.listdir(desktop) if os.path.islink(os.path.join(desktop, f))] #Goes through all of the shortcuts
	if shortcut_name not in shortcuts: #If shortcut cannot be found
		print("Searching, please wait...")
		progress_bar()
		print("Sorry, couldn't find " + shortcut_name)
		print("Returning to Main Menu...")
		return
	
	shortcut_path = os.path.join(desktop, shortcut_name) #If shortcut is found, make shortcut path

	shortcut_selection = input("Are you sure you want to remove " + shortcut_name + "? Select Y/y to confirm: ")
	if shortcut_selection == "Y" or shortcut_selection == "y":
		print("Removing link, please wait...")
		progress_bar()
		try:
			os.remove(shortcut_path)  #Removes the shortcut
			print("Link removed, returning to Main Menu.")
		except FileNotFoundError: #Shortcut cannot be found
			print("Error: The specified shortcut does not exist.")
		except Exception as e: #Error Handling
			print("Error: {e}")
	else:
		print("Exiting...")
		return

def shortcut_report(): #Runs the shortcut report
	home = get_home_directory() #Gets home directory
	desktop = os.path.join(home, "Desktop") #Gets desktop for shortcuts
	shortcuts = [f for f in os.listdir(desktop) if os.path.islink(os.path.join(desktop, f))] #Goes through all of the shortcuts

	shortcut_report_menu()
	print("Your current directory is: " + home)
	print("The number of links is: " + str(len(shortcuts)))
	print("\nSymbolic Link\t\tTarget Path")
	for link in shortcuts: #Iterates through list of shortcuts and prints
		target = os.readlink(os.path.join(desktop, link))
		print(link + "\t\t" + target)

	return_selection = input("\nTo return to the Main Menu, press Enter. Or select R/r to remove a link: ")
	if return_selection == "R" or return_selection == "r": #Removes a shortcut
		clear_terminal()
		remove_shortcut()
	else: #Returns to main menu
		clear_terminal()
		print("Returning to Main Menu shortly. Please wait...")
		progress_bar()

def main():
	while True: #An infinite while loop until a user quits by pressing Q/q
		display_menu()
		user_choice = input("Please enter a number (1-3) or ""Quit"" to exit the program: ")
		if user_choice == "1": #If user chooses to create a shortcut in the home directory
			clear_terminal()
			create_shortcut()
			time.sleep(1.5)
		elif user_choice == "2": #If user chooses to remove a shortcut from the home directory
			clear_terminal()
			remove_shortcut()
			time.sleep(1.5)
		elif user_choice == "3": #If user chooses to run a shortcut report
			clear_terminal()
			shortcut_report()
		elif user_choice == "Quit" or user_choice == "quit": #If user chooses to quit/exit
			return
		else: #If user chooses something besides the four given options
			print("Invalid Choice, try typing something else instead.")
			time.sleep(2)
		clear_terminal()
	
	
if __name__ == "__main__":
	main()
