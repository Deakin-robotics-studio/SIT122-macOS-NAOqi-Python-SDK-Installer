import Tkinter, tkFileDialog, subprocess, os
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

def writeBash():
    bash = """#!/bin/bash
echo "Removing old versions of naoqi..."
rm -rf ~/.naoqi
echo "Extracing to ~/.naoqi..."
mkdir -p ~/.naoqi
tar -xf $1 -C ~/.naoqi
mv ~/.naoqi/* ~/.naoqi/naoqi
echo "Done"
echo "Backing up your ~/.bash_profile to ~/.naoqi/.bash_profile_bk..."
cp ~/.bash_profile ~/.naoqi/.bash_profile_bk
echo "Done"

echo "Writing environment variables to ~/.bash_profile..."
echo export PYTHONPATH=${PYTHONPATH}:~/.naoqi/naoqi >> ~/.bash_profile
echo export DYLD_LIBRARY_PATH=${DYLD_LIBRARY_PATH}:~/.naoqi/naoqi >> ~/.bash_profile
echo "Done"

echo "Dynamically relinking libraries..."
target_path=~/.naoqi/naoqi/
all_libs="$target_path/*.dylib $target_path/*.so"
boost_libs=$target_path/libboost*.dylib

for lib in $all_libs; do
  echo "Treating $lib"
  for boost_lib in $boost_libs; do
    echo "Changing boost lib $boost_lib"
    install_name_tool -change $(basename $boost_lib) $boost_lib $lib
  done
done

echo "Reloading ~/.bash_profile"
source ~/.bash_profile
echo "Done."

echo -e "import naoqi\nprint 'It works!'\n" > /tmp/python-naoqi-test.py
echo "Installation complete. Test it by issuing"
echo "python /tmp/python-naoqi-test.py"
"""
    with open("install-tmp.sh", "w") as f:
        f.write(bash)

def main():
    print "Welcome to the NAOqi Python SDK installer for macOS."
    print "When prompted, please select the NAOqi Python SDK gzip archive " \
            "that you have already downloaded."

    archivePath = getNaoQiArchive()

    print "Thanks. Using archive %s." % archivePath

    writeBash()
    os.system('chmod +x install-tmp.sh')

    os.system('./install-tmp.sh %s' % archivePath)


main()
