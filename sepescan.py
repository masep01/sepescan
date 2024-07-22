#!/usr/bin/python

import argparse
import os

def scan(args):
	print('----- SCAN Mode 🔍🧐 -----')

	base_path = os.getcwd()
	dir = 'sepescan_report'

	if args.reports_path:
		base_path = args.reports_path

	new_dir = os.path.join(base_path, dir)
	try:
		os.makedirs(new_dir, exist_ok=True)
	except Exception as e:
		print(f'Error creating directory: {e}')



def fuzz(args):
    print('----- FUZZ Mode ⚡💣 -----')



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
		args.func(args)
	else:
		mainParser.print_help()


if __name__ == "__main__":
    main()

