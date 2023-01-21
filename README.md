# CommentGPT
This python script/command line tool is able to comment code using ChatGPT. The results are sometimes a little *odd*, so a human will need to look at them, but the results can be very efficient at 
commented undermaintained files.

You'll never have to write comments again!

## Installation
### Download
#### Clone the repository
```bash
git clone https://github.com/brendankane04/CommentGPT.git
```
#### Download the packages with pip
```bash
pip3 install -r requirements.txt
```
### Installation of ChatGPT-wrapper
This module needed by the script must be installed in its own way. You will need to run these commands.
```bash
pip install git+https://github.com/mmabrouk/chatgpt-wrapper
pip install playwright
playwright install firefox
```
After running this command, you will reach a web page run by OpenAI. 
You will need to log in with your OpenAI username & password
```bash
chatgpt install
```
Afterwards, exit the webpage.

## How to use
#### script in terminal
The python script can be called from the terminal and used with the following script
Clone the script using git, then access the file `main.py`.
```bash
python3 main.py -i test_file.cpp -o test_file_commented.cpp
```
The script will comment the file
#### python package
import the package with pip, then apply this to your own python script
```python
from CommentGPT import commenter as c
combined_response = c.comment_code(snippet, section_size)
```

## Future work
The tool currently uses the python ChatGPT-interfacing library [chatgpt-wrapper](https://github.com/mmabrouk/chatgpt-wrapper).
Unfortunately, it is slow, and has an involved configuration process, so that should be changed. 

The code also sometimes modifies the code being commented on a rare occasion. Using some diff tool & comment verifier in the script would prevent this.
Until then, take care to look at the modifications made in the code. 