#!/usr/bin/python
#
# Google Keep notes backup
# Robert Nowotniak <rnowotniak@gmail.com>
#


import gkeepapi
import re
import argparse
import sys

argparser = argparse.ArgumentParser(description='Backup your Google Keep notes to local text files')
argparser.add_argument('--username', help='You Google account username')
argparser.add_argument('--password', help='Password to use for login')
argparser.add_argument('--token', help='Token to use for login')
argparser.add_argument('--directory', default='./notes/', help='Local directory where to save downloaded notes files (default: %(default)s)')
argparser.add_argument('--dry-run', '-n', action='store_true', help="Don't write files, just list the notes")

args = argparser.parse_args()

if len(sys.argv) == 1:
	argparser.print_help()
	sys.exit()

if not args.username.lower().endswith('@gmail.com'):
	args.username += '@gmail.com'


if (not args.token and not args.password) or (args.token and args.password):
	argparser.error('Either --token or --password should be given (and not both)')
	sys.exit()

keep = gkeepapi.Keep()

try:
	if args.password:
		success = keep.login(args.username, args.password)
		print('Token is:\n%s' % keep.getMasterToken())
	elif args.token:
		success = keep.resume(args.username, args.token)
except:
	print("Login to Google Keep failed")	
	sys.exit(1)

if not success:
	print("Login to Google Keep failed")	
	sys.exit(1)

for note in keep.all():
	if note.trashed:
		continue
	title = note.title
	if not title:
		title = note.timestamps.edited.strftime('%Y-%m-%d %H%M')
	title = re.sub('[\\/]', '_', title)
	print(title)
	if not args.dry_run:
		fh = open('%s/%s.txt' % (args.directory, title), 'w')
		fh.write(note.text)
		fh.close()

