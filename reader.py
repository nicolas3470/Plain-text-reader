#! /usr/bin/python
# reader.py
import sys, os, md5

#check number of arguments
if len(sys.argv) != 2 and len(sys.argv) != 4:
	sys.exit('Error: This script takes at least one argument (a text file input) and at most 3 arguments')

#Get input file and paging information
if len(sys.argv) == 4:
	if sys.argv[1] != '-n':
		sys.exit('Error: -n is the only flag allowed')
	elif not sys.argv[2].isdigit():
		sys.exit('Error: the -n flag only takes positive integer inputs')
	else:
		if not os.path.isfile(sys.argv[3]):
			sys.exit('Error: Input text file does not exist')
		file_index = 3
		page = int(sys.argv[2])
else:
	if not os.path.isfile(sys.argv[1]):
		sys.exit('Error: Input text file does not exist')
	file_index = 1
	page = 40

#Get input file hash and check to see if it has been read yet
infile = open(sys.argv[file_index],'r')
hash = md5.new()
hash.update(infile.read())
infile.close()

#Get reader_rc file and create if one doesn't exist
if not os.path.exists(os.path.expanduser("~/.reader_rc")):
	open(os.path.expanduser("~/.reader_rc"),'w').close()
	index = 0
	reader_lines = [hash.hexdigest()+",0\n"]
else:
        #Find index for input file
        reader = open(os.path.expanduser("~/.reader_rc"),'r')
        reader_lines = reader.readlines()
        reader.close()
        if len(reader_lines) == 0:
                reader_lines = [hash.hexdigest()+",0\n"]
                print reader_lines
        index = 0
        while index < len(reader_lines) and not hash.hexdigest() in reader_lines[index]:
                index += 1

#Show initial page
lines_read = int(reader_lines[index].partition(",")[2])
to_read = open(sys.argv[file_index],'r')
read_file = to_read.readlines()
to_read.close()
for line in xrange(lines_read,lines_read+page):
        if line < len(read_file):
                print read_file[line],

#Update .reader_rc file
lines_read += page
reader_lines[index] = hash.hexdigest() + ',' + str(lines_read) + '\n'
outfile = open(os.path.expanduser("~/.reader_rc"),'w')
outfile.writelines(reader_lines)
outfile.close()

#Handle user input
usr_input = raw_input("\nPress one of the following then press enter: 'n' for next page, 'p' for previous page, and 'q' to quit\n\n")

while usr_input != 'q':
        if not (usr_input == 'n' or usr_input == 'p'):
                print "Only 'n', 'p', and 'q' are valid commands\n"
        else:
                if usr_input == 'n':
                        for line in xrange(lines_read,lines_read+page):
                                if line < len(read_file):
                                        print read_file[line],
                        lines_read += page
                else: 
                        new_lines_read = lines_read - page
                        if new_lines_read < 0:
                                new_lines_read = 0
                        for line in xrange(new_lines_read,lines_read):
                                if line < len(read_file):
                                        print read_file[line],
                        lines_read = new_lines_read
                reader_lines[index] = hash.hexdigest() + ',' + str(lines_read) + '\n'
                outfile = open(os.path.expanduser("~/.reader_rc"),'w')
                outfile.writelines(reader_lines)
                outfile.close()
        usr_input = raw_input("\nPress one of the following then press enter: 'n' for next page, 'p' for previous page, and 'q' to quit\n\n")
