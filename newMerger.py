#!/usr/local/bin/python3
#
# (That line is included so we don't have to launch the program
# as 'python <program>', we can just run it directly on the commandline.
# The path specified there is the path to your preferred version of
# python. How to make a python package executable on a windows machine
# is different.)
#
# merger
#
#
import sys, os, getopt
from shutil import copytree, rmtree, copyfile
from datetime import datetime

# Variable declarations
# global bookInfo
# If I don't define these at some point, doContent may fail if all of those
# fields aren't declared in the file. So it seems reasonable to declare these in
# the beginning especially since they are "global" and have significance
# throughout the program. They are now at least initialized into a known state.

global force
force = False
global today
today = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day)


def replace(search, result, line):
    # I do this several times in the code, so hey, mod it!
    newline = line
    found = line.find(search)
    if found > -1:
        newline = line[0:found] + result + line[found + len(search):]
    return newline


def findInfo( name ):
    htmlComment = "<!-- "
    trailing = ": "

    return htmlComment + name + trailing


def extract(search, line):

    htmlComment = "<!-- "
    trailing = ": "
    # returns the juicy data, without the cruft
    if findInfo(search) in line:
        endPoint = line.find(" -->") # these lines should always end " -->"
        return line[line.find(findInfo(search)) + len(search):endPoint]


class BookInfo:

    class Name:
        forename = ""
        surname = ""

    class Chapter:
    	name = ""
    	title = ""
    	number = 0
    	body = ""

    title = ""
    dir = ""
    copyright = ""
    publisher = ""
    uu_id = ""
    source = ""

    author = Name()
    editor = Name()
    cover = Name()

    subjects = []

    bookDir = ""
    filepath = ""

    chapters = [Chapter()]


def parseBook(self, info):

	startChapter = "Start"
	endChapter = "End"
	startStyle = "StartStyle"
	endStyle = "EndStyle"
	findTitle = "Title"
	findSource = "Source"
	findUUID = "UUID"
	findBookDir = "BookDir"
	findAuthor = "Author"
	findEditor = "Editor"
	findCoverArtist = "CoverArtist"
	findSubjects = "Subjects"
	findPublisher = "Publisher"
	findCopyright = "Copyright"

	with open(info.filepath) as source:
		inChapter = False
		inStyle = False
		chapter = Chapter()
		style = ""
		for line in source:
			if findInfo(findTitle) in line:
				info.title = extract(findInfo(findTitle), line)
			elif findInfo(findBookDir) in line:
				info.dir = extract(findInfo(findBookDir), line)
			elif findInfo(findAuthor) in line:
				info.author.surname, info.author.forname  = extract(findInfo(findAuthor), line).split(", ", 1)
			elif findInfo(findEditor) in line:
				info.editor.surname, info.editor.forname  = extract(findInfo(findEditor), line).split(", ", 1)
			elif findInfo(findCoverArtist) in line:
				info.coverArtist.surname, info.coverArtist.forname  = extract(findInfo(findCoverArtist), line).split(", ", 1)
			elif findInfo(findSubjects) in line:
				info.subjects = extract(findInfo(findSubjects), line).split(", ")
			elif findInfo(findPublisher) in line:
				info.publisher = extract(findInfo(findPublisher), line)
			elif findInfo(findCopyright) in line:
				info.copyright = extract(findInfo(findCopyright), line)
			elif findInfo(findUUID) in line:
				info.source = extract(findInfo(findSource), line)
			elif findInfo(startChapter) in line:
				chapter.title, chapter.number, chapter.name = extractChapter(line)
				inChapter = True
			elif findInfo(endChapter) in line:
				info.chapters.append(chapter)
				chapter = Chapter()
				inChapter = False
			elif findInfo(startStyle) in line:
				inStyle = True
			elif findInfo(endSytle) in line:
				inStyle = False
			else:
				if inChapter:
					chapter.body = chapter.body + line
				elif inStyle:
					style = style + line


def parseArgs(opts):
    filepath = ''

    print(args)
    for opt, args in opts:
        if opt in ("-h"):
            print("got -h")
            print("merger <inputfile> [-f]")
            print("-i: Input HTML file that we are using as a source")
            print("-f: if the destination directory exists, ",
                "force a delete before generating the new one")
            exit()
        if opt in ("-f"):
            print("Overwriting with -f flag.")
            force = True

    filepath = str(args[0])

    if os.path.isfile(filepath):
        return filepath
    else:
        print("File path {} does not exist. Exiting...".format(filepath))
        # if it doesn't, tell the user and quit
        exit()


def main(argv):

    try:
        opts, args = getopt.getopt(argv, ":hf")
    except getopt.GetoptError:
        print("merger <inputfile> [-f]")
        exit(2)

	parseArgs(opts)
	info = BookInfo()
	info.filepath = parseArgs(argv)

	doBookInfo(info)
	print(info)


main(sys.argv[1:]) # run the program
