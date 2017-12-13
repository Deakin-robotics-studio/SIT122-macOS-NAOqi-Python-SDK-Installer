import Tkinter, tkFileDialog, subprocess, os, urllib.request
from time import sleep

def getNaoQiArchive():
    root = Tkinter.Tk()
    root.withdraw()
    root.update()
    filePath = tkFileDialog.askopenfilename(filetypes=[('Gzip archives', '*.gz')])
    if not filePath:
        raise Exception("Invalid file path provided.")
    root.destroy()
    return filePath

def main():
    print "Welcome to the NAOqi Python SDK installer for macOS."
    print "When prompted, please select the NAOqi Python SDK gzip archive " \
            "that you have already downloaded."

    archivePath = getNaoQiArchive()

    print "Thanks. Using archive %s." % archivePath

    os.system('./install.sh %s' % archivePath)


main()
