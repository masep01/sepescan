#!/usr/bin/python

import argparse
import os
import subprocess
import signal
from termcolor import colored
import pyfiglet 

def launch_scan(tool, host, dir):
	file = os.path.join(dir, f"{tool}.scan")
	commands = {
		'nmap' : [ 'nmap', '-p-', '-sV', '-sC', '--min-rate', '5000', '-Pn', '-n', '-oN', file, host ],
		'nikto' : [ 'nikto', '-h', host, '-p', '443', '-o', file, '-Format', 'txt'],
		'whatweb' : [ 'whatweb', '--color=always', '-v', '-a', '3', host ]
	}
	command = commands.get(tool)
	
	result = ''
	if tool == 'whatweb':
		try:
			with open(file, "w") as output:
				result = subprocess.run(command, stdout=output, stderr=subprocess.PIPE, universal_newlines=True)
		
		except Exception as e:
			print(colored("[!]", "red") + f" An error occurred: {e}")
	else:
		result = subprocess.run(command, capture_output=True, text=True)

	if result.returncode == 0:
		print(colored("[+]", "green") + f" {tool} scan completed successfully!\n")
	else:
		print(colored("[!]", "red") + f" {tool} scan failed. Aborting...\n")
		exit(1)

def scan(args):
	print(colored("[*] ", "light_magenta")+colored("SCAN Mode", attrs=["bold"])+" 🔍🧐\n")

	# Checking requirements
	print(colored("[*] ", "light_yellow")+colored("Checking requirements...\n"))
	if not check_requirements(["nmap", "whatweb", "nikto"]):
		print(colored("[!]", "red") + " Some program may not installed. Please check requirements.\n")
		exit(1)

	# Create reports directory
	new_dir = create_reports_dir(args)
	if new_dir == None:
		exit(1)
	
	print(colored("[*]", "cyan") + " Scanning host: "+colored(args.host, "light_yellow", attrs=["bold"])+"\n")

	# Scans
	launch_scan('nmap', args.host, new_dir)
	launch_scan('nikto', args.host, new_dir)
	launch_scan('whatweb', args.host, new_dir)

	print(colored("[*]", "cyan")+" Scan completed successfully. See results in "+colored(f"{new_dir}\n", "light_yellow"))

def fuzz(args):
	print(colored("[*]", "yellow")+colored(" FUZZ Mode",attrs=["bold"])+" ⚡💣\n")
	print("Coming soon...")

def create_reports_dir(args):
	base_path = os.getcwd()
	dir = 'sepescan_report'

	if args.reports_path:
		base_path = args.reports_path

	new_dir = os.path.join(base_path, dir)
	try:
		os.makedirs(new_dir, exist_ok=True)
		return new_dir
	except Exception as e:
		print(f'Error creating directory: {e}')
		return None
	
def check_requirements(programs):
	for program in programs:
		try:
			subprocess.check_output(["which", program], stderr=subprocess.STDOUT, universal_newlines=True)
		except subprocess.CalledProcessError:
			return False
	return True
	
def signal_handler(sig, frame):
    print(colored("[!]", "red") + " Ctrl+C pressed. Aborting...\n")
    exit(1) 

def print_banner():
	print(pyfiglet.figlet_format("SepeScan", font = "slant"))

def main():
	# Parser configuration
	mainParser = argparse.ArgumentParser(
		prog='sepescan',
		description='Scanning tool by masep01.',
	)

	subParsers = mainParser.add_subparsers(dest='mode', help='Choose a mode')

	# SCAN Mode
	scanParser = subParsers.add_parser('scan', help='Scan Mode')
	scanParser.add_argument('host', type=str, help='hostname')
	scanParser.add_argument('-p', '--reports-path', type=str, help='specify path to save all reports (default: ./ )')
	scanParser.set_defaults(func=scan)

	# FUZZ Mode
	fuzzParser = subParsers.add_parser('fuzz', help='Fuzzing Mode')
	fuzzParser.add_argument('host', help='hostname')
	fuzzParser.add_argument('-w', '--wordlist', type=str, help='wordlist used (default: directory-list-2.3-medium.txt)')
	fuzzParser.add_argument('-u', '--url-path', type=str, help='relative path')
	fuzzParser.add_argument('-p', '--reports-path', type=str, help='specify path to save all reports (default: ./ )')
	fuzzParser.set_defaults(func=fuzz)

	# Mode selection
	args = mainParser.parse_args()

	if 'func' in args:
		print_banner()
		args.func(args)
	else:
		mainParser.print_help()


if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal_handler)
	main()

