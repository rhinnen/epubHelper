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

    # returns the juicy data, without the cruft
    startPoint = len(search)
    endPoint = line.find(" -->") # these lines should always end " -->"
    return line[startPoint:endPoint]


class Chapter:
    def __init__(self):
        self.name = ""
        self.title = ""
        self.number = 0
        self.body = ""


class BookInfo:

    class Name:
        def __init__(self):
            self.forename = ""
            self.surname = ""

    def __init__(self):
        self.title = ""
        self.dir = ""
        self.copyright = ""
        self.publisher = ""
        self.uu_id = ""
        self.source = ""
        self.bookDir = ""
        self.filepath = ""
        self.style = ""
        self.subjects = []
        self.chapters = []
        self.author = self.Name()
        self.editor = self.Name()
        self.cover = self.Name()


def parseBook():

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

    chapter = Chapter()
    inChapter = False
    inStyle = False

    with open(info.filepath) as source:

        for line in source:
            if findInfo(findTitle) in line:
                info.title = extract(findInfo(findTitle), line)
            elif findInfo(findBookDir) in line:
                info.dir = extract(findInfo(findBookDir), line)
                print(info.dir)
            elif findInfo(findAuthor) in line:
                info.author.surname, info.author.forename = (extract(findInfo(findAuthor), line).split(" ", 1))
            elif findInfo(findEditor) in line:
                info.editor.surname, info.editor.forename  = extract(findInfo(findEditor), line).split(" ", 1)
            elif findInfo(findCoverArtist) in line:
                info.coverArtist.surname, info.coverArtist.forename  = extract(findInfo(coverArtist), line).split(" ", 1)
            elif findInfo(findSubjects) in line:
                info.subjects = extract(findInfo(findSubjects), line).split(", ")
            elif findInfo(findPublisher) in line:
                info.publisher = extract(findInfo(findPublisher), line)
            elif findInfo(findCopyright) in line:
                info.copyright = extract(findInfo(findCopyright), line)
            elif findInfo(findUUID) in line:
                info.source = extract(findInfo(findSource), line)
            elif findInfo(startChapter) in line:
                chapter.name, chapter.number, chapter.title = extract(findInfo(startChapter), line).split(' ', 2)
                inChapter = True
            elif findInfo(endChapter) in line:
                info.chapters.append(chapter)
                chapter = Chapter()
                inChapter = False
            elif findInfo(startStyle) in line:
                inStyle = True
            elif findInfo(endStyle) in line:
                inStyle = False
            else:
                if inChapter:
                    chapter.body = chapter.body + line
                elif inStyle:
                    info.style = info.style + line


def writeStructure():
    mode = 0o775

    if os.path.isfile(info.dir):
        if force:
            shutil.rmtree(info.dir)
        else:
            print("Directory exists.")
            exit()

    os.mkdir(info.dir, mode)

    for directory in ["META-INF", "OEBPS", "OEBPS/Images", "OEBPS/Styles", "OEBPS/Text"]:
        path = os.path.join(info.dir, directory)
        os.mkdir(path, mode)


def writeMisc():
    mode = 0o664
    access = 'w'
    file = os.path.join(info.dir, "mimetype")

    mimetype = open(file, access)
    mimetype.write("application/epub+zip")
    mimetype.close()

    file = os.path.join(info.dir, "META-INF", "com.apple.ibooks.display-options.xml")
    meta1 = open(file, access)
    meta1.write('<?xml version="1.0" encoding="UTF-8"?>\n<display_options>\n  <platform name="*">\n    <option name="specified-fonts">false</option>\n  </platform>\n</display_options>')
    meta1.close()

    file = os.path.join(info.dir, "META-INF", "container.xml")
    meta2 = open(file, access)
    meta2.write('<?xml version="1.0" encoding="UTF-8"?>\n<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n  <rootfiles>\n    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>\n  </rootfiles>\n</container>')
    meta2.close()


def writeTOC():
    pass
    access = 'w'
    file = os.path.join(info.dir, 'OEBPS', 'toc.ncx')
    navpoints = []

    contentsstart = """<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <head>
    <meta content="urn:isbn:""" + info.uu_id + """" name="dtb:uid"/>
    <meta content="1" name="dtb:depth"/>

    <!-- totalPageCount and maxPageNumber are mandatory, but they're not used in ebooks -->
    <meta content="-1" name="dtb:totalPageCount"/>
    <meta content="-1" name="dtb:maxPageNumber"/>
  </head>
  <docTitle>
    <text>""" +info.title + """</text>
  </docTitle>
  <navMap>
    <navPoint id="navpoint1" playOrder="1">
      <navLabel>
        <text>Cover</text>
      </navLabel>
      <content src="Text/cover.xhtml"/>
    </navPoint>"
    """
    contentsend = """  </navMap>
</ncx>"""

    for each in info.chapters:
        navpoints.append("\t<navPoint id =\"" + each.name + "\" playOrder=\"" + str(each.number) + "\">\n" +
            "\t\t<navLabel>\n\t\t\t<text>" + each.name + "</text>\n\t\t</navLabel>\n" +
            "\t\t<content src=\"" + each.name + ".xhtml\"/>\n\t</navPoint>\n")

    contents = contentsstart
    for each in navpoints:
        contents += each
    contents += contentsend

    print(contents)
    toc = open(file, access)
    toc.write = contents
    toc.close()

def writeCover():
    pass


def writeContents():
    pass


def writeChapters():
    pass


def writeStyles():
    pass


def parseArgs(argv):

    try:
        opts, args = getopt.getopt(argv, ":hf")
    except getopt.GetoptError:
        print("merger <inputfile> [-f]")
        exit(2)

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

    info.filepath = str(args[0])

    if os.path.isfile(info.filepath):
        print("Directory {} already exists")
    else:
        print("File path {} does not exist. Exiting...".format(filepath))
        # if it doesn't, tell the user and quit
        exit()


def main(argv):

    global force
    global today
    global info

    force = False
    today = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day)
    info = BookInfo()

    parseArgs(argv)
    parseBook()
    writeStructure()
    writeMisc()
    writeTOC()
    writeCover()
    writeContents()
    writeChapters()
    writeStyles()


main(sys.argv[1:]) # run the program
