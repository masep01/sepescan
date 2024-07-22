#!/usr/bin/python

import argparse
import os
import subprocess
import signal
from termcolor import colored
import pyfiglet 

def scan(args):
	print(colored("[*] ", "yellow")+colored("SCAN Mode", attrs=["bold", "underline"])+" 🔍🧐")

	new_dir = create_reports_dir(args)
	if new_dir == None:
		exit(1)
	
	# nmap
	print(colored("[+]", "green") + " Scanning host: "+colored(args.host, "light_yellow", attrs=["bold"]))
	nmap_file = os.path.join(new_dir, "nmap.scan")
	command = [ 'nmap', '-p-', '-sV', '-sC', '--min-rate', '5000', '-Pn', '-n', '-oN', nmap_file, args.host ]
	result = subprocess.run(command, capture_output=True, text=True)
	if result.returncode == 0:
		print(colored("[+]", "green") + " nmap scan completed successfully!\n")
	else:
		print(colored("[!]", "red") + " Scan failed. Aborting...\n")

def fuzz(args):
	print(colored("[*]", "yellow")+" FUZZ Mode ⚡💣")

def print_banner():
	print(pyfiglet.figlet_format("SepeScan", font = "slant"))

def signal_handler(sig, frame):
    print(colored("[!]", "red") + " Ctrl+C pressed. Aborting...\n")
    exit(1) 

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

def main():
	# Parser configuration
	mainParser = argparse.ArgumentParser(
		prog='SepeScan',
		description='Scanning tool'
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

