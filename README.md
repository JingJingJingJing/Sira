# Sira
Welcome to Sira! 
Sira is a command line tool to query or update JIRA's data. 
Sira 2.0 is total different from Sira 1.0. It runs in shell environment.

Here is the way to build sira 2.0:
  1. Make sure you have installed python(3.+) and git bash
  2. Install python dependencies using pip:
      pip install pyinstaller
      pip install termcolor
      pip install requests
  3. Run build/build.sh in git bash
  4. Run build/setup.ps1 in powershell
  5. Open cmd and make sure the cuurent directory contains .sirarc file.
  
  Tips: The current version does not include functions to initial configuration file. So the tips is to cd the current directory to '/Sira' before you start to use Sira.
