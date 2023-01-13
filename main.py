from chatgpt_wrapper import ChatGPT
import sys, getopt
from tqdm import tqdm


def test_gpt():
    # Verify the ChatGPT interface can be started up
    print("Initializing ChatGPT...", end="")
    bot = ChatGPT()

    print("Done!")
    # Verify if a question can be sent to the API & can receive a response
    question = "What is 2 + 2?"
    print("Sending question to ChatGPT: (", question, ") ...", end="")
    response = bot.ask(question)
    print("Done!")

    # Verify if the response is, at least, *somewhat* logically consistent to the question
    if "4" or "four" or "Four" in response:
        print ("We have a working connection!")
        print("We have a working connection! Response: (", response, ") ...")
        return True
    else:
        print ("Not Working!")
        print("We DON'T have a working connection! Response: (", response, ") ...")
        return False



def snippet_to_question(snippet):
    # the question being asked to API
    prompt = "Give me this code but with comments written in. "
    # narrows down the question to avoid  "undesirable" components in the response
    # things like "This is the code: " or "This is code with comments in it."
    narrower = "Don't say something before the code. Don't modify the code. Only add comments.:\n\n"
    question = prompt + snippet
    return question


def get_args():
    argv = sys.argv[1:]
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    # trim the leading & trailing spaces
    inputfile = inputfile.strip()
    outputfile = outputfile.strip()
    return inputfile, outputfile


if __name__=="__main__":
    bot = ChatGPT()

    inputfile, outputfile = get_args()

    with open(inputfile) as file:
        snippet= file.read()

    lines = snippet.splitlines() # split the code into a list of strings, each one line of the code
    snippet_size = 50 # How many lines compose each section
    snippet_sections = []

    # create a list of 'snippet_size' line sections of the file
    while len(lines) > 0:
        # TODO: figure out a way to split along lines without splitting along '\n' segments within the lines
        snippet_section = '\n'.join(lines[:snippet_size])
        lines = lines[snippet_size:]
        snippet_sections.append(snippet_section)

    print("Commenting the code with ChatGPT: ")
    combined_response = ""
    for snippet_section in tqdm(snippet_sections):
        question = snippet_to_question(snippet_section)
        response = bot.ask(question)
        # if the response is empty, populate it.
        if combined_response == "":
            combined_response = response
        # if the response isn't empty, add a new line & the new section
        else:
            combined_response = '\n'.join([combined_response, response])

    with open(outputfile, 'w') as file:
        file.write(combined_response)