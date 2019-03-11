# Simple Testing Script for Assignment 1 
# 
# Builds program and tests for two simple cases.
# 
# How to use:
#	- Copy this file to the directory you're using to store your program.
#	- If this file, once copied, can't be run using test.sh, you may need
#		to run `chmod 777 test.sh` in your terminal window.
#	- Compile your program as usual.
#	- You can feel free to use this program for your own testing, we would 
#		however recommend you ensure your program still executes on the original
#		version of this file.
#	- You may like to explain what you think the output should be using the echo
#		command, so you know what to expect from your program.
#	- After saving your changes, you can run this script using test.sh.
#
# NOTE: This is in no sense a complete set of test cases, you'll need to write
#	some of your own to ensure your program is correct.
#
# NOTE2: This program will overwrite any file you have called exactly datafile,
#	datafile2, keyfile, keyfile2, outputfile1_1, outputfile1_2, outputfile2_1, 
#	outputfile2_2 stdout1_1, stdout1_2, stdout2_1, stdout2_2, e_stdout1, 
#	e_stdout2, e_outputfile1 or e_outputfile2.
#
# Written by Grady Fitzpatrick (Staff Number 110064, Student 575753) for 
# COMP20003, Algorithms and Data Structures

# Removes .o files and the dict programs, to make sure you're not 
# building something using old files.
rm -f *.o dict1 dict2

# -B forces make to make the programs even if they are up to date.
echo "Making dict1 and dict2"
make dict1 -B
make dict2 -B

# Test data, single characters where possible, single record.
TESTDATAFILE1="9,a,F,5,6,8,T,AUS,1 Summer,7,Summer,A,X,Y,NA"
TESTKEYFILE1="a"

# Second Test data, another, different, single character where possible, single
# 	record.
TESTDATAFILE2="4,b,M,4,NA,7,t,RUS,2 Summer,5,Winter,C,S,E,Gold"
TESTKEYFILE2="b"

# Expected outputs. Variations in this are certainly possible, however it should
#	give you something to expect.
EXPECTEDOUTPUT1="a --> ID: 9 Sex: F || Age: 5 || Height: 6 || Weight: 8 || Team: T || NOC: AUS || Games: 1 Summer || Year: 7 || Season: Summer || City: A || Sport: X || Event: Y || Medal: NA ||
"
EXPECTEDSTDOUTPUT1="a --> 1
"
EXPECTEDOUTPUT2="b --> ID: 4 Sex: M || Age: 4 || Height: NA || Weight: 7 || Team: t || NOC: RUS || Games: 2 Summer || Year: 5 || Season: Winter || City: C || Sport: S || Event: E || Medal: Gold ||
"
EXPECTEDSTDOUTPUT2="b --> 1
"

# Output test data to files named datafile, keyfile, datafile2 and keyfile2 and
# 	all expected data to expected files.
printf "$TESTDATAFILE1" > datafile
printf "$TESTKEYFILE1" > keyfile
printf "$TESTDATAFILE2" > datafile2
printf "$TESTKEYFILE2" > keyfile2
printf "$EXPECTEDOUTPUT1" > e_outputfile1
printf "$EXPECTEDSTDOUTPUT1" > e_stdout1
printf "$EXPECTEDOUTPUT2" > e_outputfile2
printf "$EXPECTEDSTDOUTPUT2" > e_stdout2

# Run the tests on both programs.
echo "Running dict1 datafile outputfile < keyfile > stdout1_1"
dict1 datafile outputfile1_1 < keyfile > stdout1_1
#echo "Contents of outputfile"
#cat outputfile

echo "Running dict1 datafile2 outputfile2 < keyfile2 > stdout1_2"
dict1 datafile2 outputfile1_2 < keyfile2 > stdout1_2
#echo "Contents of outputfile2"
#cat outputfile2

echo "Running dict2 datafile outputfile < keyfile > stdout2_1"
dict2 datafile outputfile2_1 < keyfile > stdout2_1
#echo "Contents of outputfile"
#cat outputfile

echo "Running dict2 datafile2 outputfile2 < keyfile2 > stdout2_2"
dict2 datafile2 outputfile2_2 < keyfile2 > stdout2_2
#echo "Contents of outputfile2"
#cat outputfile2

# Compare outputs to expected outputs.
echo "Checking output against expected"
echo "--------------------------------"
# Check out  man diff  to see what this does! This part is entirely for your 
#	benefit, you should get "".
echo "dict1 stdout comparison with expected - Test Case 1"
diff --side-by-side --suppress-common-lines --minimal --report-identical-files --ignore-all-space stdout1_1 e_stdout1
echo "dict1 file output comparison with expected - Test Case 1"
diff --side-by-side --suppress-common-lines --minimal --report-identical-files --ignore-all-space outputfile1_1 e_outputfile1
echo "--"
echo
echo "dict1 stdout comparison with expected - Test Case 2"
diff --side-by-side --suppress-common-lines --minimal --report-identical-files --ignore-all-space stdout1_2 e_stdout2
echo "dict1 file output comparison with expected - Test Case 2"
diff --side-by-side --suppress-common-lines --minimal --report-identical-files --ignore-all-space outputfile1_2 e_outputfile2
echo "--"
echo
echo "dict2 stdout comparison with expected - Test Case 1"
diff --side-by-side --suppress-common-lines --minimal --report-identical-files --ignore-all-space stdout2_1 e_stdout1
echo "dict2 file output comparison with expected - Test Case 1"
diff --side-by-side --suppress-common-lines --minimal --report-identical-files --ignore-all-space outputfile2_1 e_outputfile1
echo "--"
echo
echo "dict2 stdout comparison with expected - Test Case 2"
diff --side-by-side --suppress-common-lines --minimal --report-identical-files --ignore-all-space stdout2_2 e_stdout2
echo "dict2 file output comparison with expected - Test Case 2"
diff --side-by-side --suppress-common-lines --minimal --report-identical-files --ignore-all-space outputfile2_2 e_outputfile2
echo "--"
echo
