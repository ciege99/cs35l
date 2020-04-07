

import random, sys
from argparse import ArgumentParser


class shuffle:
	def __init__(self, filename, args):
		self.lines = []
		self.args = args
		if filename:
			if (filename is not sys.stdin):
				f = open(filename, 'r')
			else:
				f = filename
			if (self.args.span == False):
				self.lines = f.readlines()
				self.isFile = True
			if (filename != sys.stdin):
				f.close()
		self.iProtocol()
		self.nProtocol()
		self.length = len(self.lines)
		self.randList = []

	def iProtocol(self):
		if (self.args.span != False):
			self.isFile = False
			r1 = int(self.args.span[0])
			r2 = int(self.args.span[1])
			if (r1 > 0 and r2 > 0 and r2 >= r1):
				self.lines = list(range(r1, r2+1)) #r2+1 since range not []
				self.length = len(self.lines) #update length

	def nProtocol(self):
		if (self.args.numlines >= 0):
			self.printLength = int(self.args.numlines)
			self.nSet = True
		else:
			self.printLength = len(self.lines)
			self.nSet = False

	def rProtocol(self):
		if self.args.repeat==True :
			if (self.nSet == True):
				for i in range(self.printLength):
					if (self.isFile):
						print(random.choice(self.lines), end="")
					else:
						print(random.choice(self.lines))
			else:
				while True == True:	
					if (self.isFile):
						print(random.choice(self.lines), end="")
					else:
						print(random.choice(self.lines))
		else:
			self.readPermutation()
	
	def chooseline(self):
		return random.choice(self.lines)
	
	def readLines(self):
		self.rProtocol()

	def readPermutation(self):
		self.randList = list(range(self.length))
		random.shuffle(self.randList)
		self.randList = self.randList[:self.printLength]
		for i in self.randList:
			if (self.isFile):
				print(self.lines[i], end="")
			else:
				print(self.lines[i])

def main():
	version_msg = "%prog 2.0"
	usage_msg = """%prog [OPTION]... FILE
Usage: shuf [OPTION]... [FILE]
  or:  shuf -i LO-HI [OPTION]...
  or:  shuf - [STDIN]...

Write a random permutation of the input lines to standard output."""

	parser = ArgumentParser()
	parser.add_argument("doc",  
					nargs='?', default=sys.stdin,
					help="Optional file input")
	parser.add_argument("-",
					action="store_const", dest="doc", const=sys.stdin,
					help="Use stdin as input")
	parser.add_argument("-n", "--head-count=numlines",
					dest="numlines",  default=False,
					help="output at most numlines lines") 
	parser.add_argument("-i", "--input-range=LO-HI",
					action="store", dest="span", default=False,
					help="treat each number LO through HI as an input line")
	parser.add_argument("-r", "--repeat",
					action="store_true", dest="repeat", default=False,
					help="output lines can be repeated")
	try:
		args = parser.parse_args()
	except IOError as err:
            errno, strerror = err.args
            print("I/O error({0}): {1}".format(errno, strerror)) 
	noArgs = not (args.doc or args.numlines or args.span==False 
			or args.repeat==False)
	if noArgs:
		parser.error("No operands given")
	
	input_file = args.doc
	
	if args.numlines:
		try:
			args.numlines = int(float(args.numlines))
		except:
			parser.error("invalid line count: '{0}'".format(args.numlines))

		if (args.numlines < 0):
			parser.error("invalid line count: '{0}'".format(args.numlines))	
	
	if (args.span != False):
		if (args.doc != sys.stdin):
			sys.exit('Segmentation fault')

		args.span = args.span.split('-')
		if (len(args.span) != 2):
			parser.error("incorrect range")
		if ( args.span != False and
		(int(args.span[0]) < 0 or int(args.span[1]) < 0)):
			parser.error("range is incorrect")
	
	if not noArgs:
		try:
			generator = shuffle(input_file, args)
			generator.readLines()
		except IOError as err:
			errno, strerror = err.args
			print("I/O error({0}): {1}".format(errno, strerror))

main()
