import chatgpt_interface_wrapper
import os, sys, getopt
from tqdm import tqdm


testing_mode = False

def snippet_to_question(snippet):
    # the question being asked to API
    prompt = "Give me this code but with comments written in. "
    # narrows down the question to avoid  "undesirable" components in the response
    # things like "This is the code: " or "This is code with comments in it."
    narrower = "Don't say something before or after the code. Don't add any backticks. Don't modify the code. Only add comments.:\n\n"
    prompt += narrower
    question = prompt + snippet
    return question


def get_args():
    argv = sys.argv[1:]
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:t", ["ifile=", "ofile=", "test"])
    except getopt.GetoptError:
        print('test.py -i <inputfile> -o <outputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
        elif opt in ("-t", "--test"):
            global testing_mode
            testing_mode = True

    if inputfile != '':
        inputfile = inputfile.strip() # trim the leading & trailing spaces
    else:
        inputfile = argv[-1] # if there's no flag used, the last argument is the input file

    if outputfile != '':
        outputfile = outputfile.strip() # trim the leading & trailing spaces
    else:
        # if no '-o' flag was provided, the output file will be the input file + "_commented
        # (Ex: input.cpp -> input_commented.cpp)
        name, ext = os.path.splitext(inputfile)
        outputfile = name + "_commented" + ext
    return inputfile, outputfile


def divide_into_sections(snippet, section_size):
    lines = snippet.splitlines() # split the code into a list of strings, each one line of the code
    snippet_sections = []
    # create a list of 'snippet_size' line sections of the file
    while len(lines) > 0:
        # TODO: figure out a way to split along lines without splitting along '\n' segments within the lines
        snippet_section = '\n'.join(lines[:section_size])
        lines = lines[section_size:]
        snippet_sections.append(snippet_section)
    return snippet_sections


if __name__=="__main__":
    # get a ChatGPT interface & initialize it
    curr_gpt_tool = chatgpt_interface_wrapper.chatgpt_wrapper_interface()
    curr_gpt_tool.init()

    # get the input file & output file names from the arguments
    inputfile, outputfile = get_args()

    if testing_mode:
        is_working = curr_gpt_tool.is_working()
        if is_working:
            print("ChatGPT is working.")
        else:
            print("ChatGPT is NOT working.")
        exit()

    # read in the input file's text
    with open(inputfile) as file:
        snippet= file.read()

    snippet_size = 50 # How many lines compose each section

    # break the input 'snippet' of text into a list of strings. i.e. "snippet_sections"
    snippet_sections = divide_into_sections(snippet, snippet_size)

    # send each section of the input text to chatGPT, requesting to comment each section
    print("Commenting the code with ChatGPT: ")
    combined_response = ""
    for snippet_section in tqdm(snippet_sections):
        # format each the section of the text into a question, requesting comments
        question = snippet_to_question(snippet_section)
        # send the question
        response = curr_gpt_tool.ask(question)
        # combine each individual commented section into a combined, commented file
        combined_response = response if combined_response == "" else combined_response + '\n' + response
        # if combined_response == "":
        #     # if the response is empty, populate it.
        #     combined_response = response
        # else:
        #     # if the response isn't empty, add a new line & the new section
        #     combined_response = combined_response + '\n' + response

    # write the commented code to an output file
    with open(outputfile, 'w') as file:
        file.write(combined_response)