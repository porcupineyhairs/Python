# Auto complite py file to pyc
# Author Harvey

# Main Script
echo '1.Files Compiling'
python3.6 -m compileall ./
echo '2.Files Compiled'

# File Move 
echo '3.Moving Files'
mv ./__pycache__/*.pyc ./
echo '4.Files Move Completed'

# File rename
echo '5.pyc Files Rename'
rename -v -f 's/.cpython-36//' *.pyc
echo '6.Files Rename Completed'

# Delete dir  __pycache__
echo '7.Deleting Dir __pycache__'
rm -r ./__pycache__
echo '8.Delete Dir Completed'

# Delete source file
#echo '9.Deleting Source Files'
#rm ./*.py
#echo '10.Delete Source Files Completed'
