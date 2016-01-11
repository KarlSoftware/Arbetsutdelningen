### Arbetsutdelningen
Scan Arbetsförmedlingen for emails (Python)

#### What does it do?
Arbetsutdelningen is a Python script for Arbetsförmedlingen, a Swedish website that is for finding jobs. The script scans through job advertisements and finds all the emails, which can simplify the process of applying. It also automatically sends an application with your CV attached. With this script you can apply for hundreds of jobs in a matter of minutes.

There is also a website version at http://thomasmyrman.se/dev/arbetsutdelningen/

#### Dependencies
* Python
* yagmail https://github.com/kootenpv/yagmail
  * Make sure you go to this link if you have any problems

#### Notes
* This will only work if you are currently using Gmail to send emails.
* There might be a warning about lxml but don't worry about it.
* You must enable apps on Gmail by going here: https://www.google.com/settings/security/lesssecureapps
* Of course, the script will never email the same people twice.


#### Installing & use
Download all the files to your computer. Then modify the file called "email-content". It has a basic template for the email you're going to send out. Modify as you wish, and change your name at the bottom. If you don't the script will fail.

Make sure you have all three files (blacklist, email-content and start.py). Run start.py with Python. The script will ask for a couple of things to get you started. Fill it in and confirm to begin. And don't worry, there is a function to email yourself first, to see how it looks.
