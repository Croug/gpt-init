# Installation
## Virtual Environment Setup
It is recommended to run this in a virtual environment with venv althought it is not required

1. Install venv e.g. `pip install virtualenv`
2. cd into the directory you cloned gpt-init
3. run `python -m venv venv`
4. activate the environment
    - Windows `venv/scripts/activate.bat` or `venv/scripts/activate.ps1`
    - Linux `source venv/scripts/activate`

## First time install
If you created a virtual env in the previous section you should activate it first if you haven't already.

1. Install the program requirements `pip install -r requirements.txt`
2. Setup playwright `playwright install`
3. Run `chatgpt install` this will open a chromium window with the chatgpt login
4. Login to chatgpt and then close the window
5. Go back to the terminal where you ran the chatgpt install. Type exit to leave the chatgpt setup, the login token has already been cached

# Using the script
If you set up a virtual environment activate it, then simply run `python main.py` in the gpt-init directory. This will start the process, it may take a moment to actually output anything, this is just because chatgpt is being primed with instructions. Once you get the first prompt, simply talk to chat gpt. It may ask you questions about your project and give you ideas. Have a conversation, talk about the goals the technologies. Talk with it a little bit about the visuals. Anything you can think of. Once you think it has a good handle on your project, type `generate` this will initiate the next phase where it builds out your project structure and fills it in with some starter content. The entire project will end up in a directory with the script, the name will depend on the project you told it about, likely using the name of the project if you provided it.

###### *Bonus tip: You can open the chat back up in the ChatGPT chat history to continue to talk about the project and get additional help*