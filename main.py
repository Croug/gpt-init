import os
from chatgpt_wrapper import ChatGPT

bot = ChatGPT()

def find_text(s: str, start: str, end: str) -> tuple[str, str]:
    start_index = s.find(start)
    if start_index == -1:
        return "", s.strip()
    start_index += len(start)
    end_index = s.find(end, start_index)
    if end_index == -1:
        return "", s.strip()
    found_text = s[start_index:end_index].strip()
    original_text = s[:start_index-len(start)].strip() + s[end_index+len(end):]
    return found_text, original_text.strip()

def extract_code(markdown_string):
    lines = markdown_string.split("\n")
    code_lines = []
    in_code_block = False

    for line in lines:
        if line.startswith("```"):
            if in_code_block:
                # Return the code lines if we are already in a code block
                return "\n".join(code_lines)
            else:
                in_code_block = True
            continue
        if in_code_block:
            code_lines.append(line)

    return "\n".join(code_lines)

def count_depth(s):
    stripped_s = s.lstrip()  # remove all leading spaces
    spaces = len(s) - len(stripped_s)  # compare lengths to get number of
    return int(spaces/2)

def parse_tree(s):
  ret = []
  path = []
  for line in s.splitlines():
    if count_depth(line) < len(path):
      path = path[:count_depth(line)]

    ret.append('/'.join(path + [line.strip()]))

    if line.strip()[-1] == '/':
      path.append(line.strip()[:-1])

  return ret

def build_tree(files):
  for file in files:
    if file[-1] != '/':
      open(file, 'w').close()
    elif not os.path.exists(file):
      os.makedirs(file)

def sep(n=80):
  print("="*n)

resp = bot.ask(""" [The following conversation will be an attempt to create a simple project outline and template. Please ask the user questions about their project to gain a sufficient understanding of the project. You should be attempting to learn as much as possible about the project in an effort to determine things like what files the project should be split into, what technologies will work best, what stack to implement, what languages to use, and other important things around starting a project. Please avoid giving the user direct instructions to install specific programs or packages as that is something that will be handled by me automatically handled in the generation step. Following your conversation with the user *I* will then ask you some questions about about the project structure you have devised in order to do my best to recreate it on the users filesystem. Additionally please prefix every response to the user with a number from 0 to 100 in square brackets that will represent your confidence in your ability to create a good project outline with your present knowledge of the users project, this value should be 0 at the beginning, and get larger as you learn more about the project. Additionally if you learn a piece of information that requires you to learn more your confidence can go back down until you learn the required info. At any point please feel free to remind the user that they can simple type the word "generate" to exit the research phase, and enter the generation phase. Until further notice all of your messages are going directly to the user. including your response to this prompt. please respond as such] 
  [In your response also please inform the user they can type "generate" to move on to the generation step or "exit" to exit the program] """)
sep()
print(resp[4:])
sep()

head = """ [Please prefix the following message with a number from 0 to 100 encased in square brackets representing your confidence in your ability to create a good project outline with your present knowledge of the users project. At any point where your confidence is greater than 80 please feel free to remind the user that they can simple type the word "generate" to exit the research phase, and enter the generation phase. Until further notice all of your messages are going directly to the user. including your response to this prompt. please respond as such] """
confidence = 0

while True:
  inp = input("> ")

  if inp == "exit":
    print("Exiting...")
    exit()

  if inp == "generate" and confidence < 60:
    print("Are you sure you want to attempt generation? The bot is only " + str(confidence) + "% confident in its ability to create a good project outline. If you continue to discuss the project ChatGPT may become more confident in it's ability. If you are sure you want to attempt generation please type 'generate' again.")
    inp = input("> ")
    if inp == "generate":
      break

  elif inp == "generate":
    break

  print("Thinking...", end="\r")
  resp = bot.ask(head + "\n" + inp)
  confidence, txt = find_text(resp, "[", "]")
  confidence = int(confidence)
  sep()
  print(str(confidence) + "%\n" + txt)
  sep()

sep()
print("Please wait while I generate your project outline...")
resp = bot.ask(""" [The user has indicated that they are ready to move onto the generation step, and I will now proceed to ask you questions about the project structure you have developed. Please send me the file structure of the outline you have helped create. The output will be fed directly into a directory parser so please ensure the directory structure follows the format described exactly, and is contained within the first code block. Each file or directory should be on it's own line. If it's a directory it should end with "/". The first item should be the project root. Files and directories should appear underneath their parent, indented once more than their parent. Use 2 spaces to indent.] """)
tree, txt = find_text(resp, "```", "```")

sep()
print("This is the file structure we will be using...")
print(tree)
sep()

files = parse_tree(tree)
build_tree(files)

for file in files:
  if file[-1] == '/':
    continue
  if file.upper().endswith("README.MD"):
    continue
  if file.upper().endswith(".GITIGNORE"):
    continue

  print("Generating %s" % (file))

  prompt = """ [Please respond only with the complete contents of "%s". Please make sure to use comments to make it obvious what should be changed or filled in by the user. Please include any description of the code in the code, as a comment.] """ % (file)
  resp = bot.ask(prompt)
  content = extract_code(resp)

  with open(file, "w") as f:
    f.write(content.strip() + "\n") 

resp = bot.ask(" [Please respond only with the complete contents of good .gitignore for this project. Please make sure to use comments to categorize it] ")
fname = files[0] + ".gitignore"
content = extract_code(resp)
print("Generating %s" % (fname))
with open(fname, "w") as f:
  f.write(content.strip() + "\n")

resp = bot.ask(" [The entirety of your next response will placed directly into a readme.md describing how to use the template we have just created] ")
fname = files[0] + "README.md"
print("Generating %s" % (fname))
with open(fname, "w") as f:
  f.write(resp.strip() + "\n")

resp = bot.ask(" [The entirety of your next response will be sent directly to the user as the final goodbye before this program exits, please make any final notes to the user now.] ")
sep()
print(resp)
input("Press enter to exit...")
