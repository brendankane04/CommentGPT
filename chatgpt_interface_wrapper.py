# This is a wrapper around the chatGPT interface to interface with different chatGPT interfaces as they're new
# and changing quite rapidly.
from chatgpt_wrapper import ChatGPT

initialized = False

class chat_gpt_interface:
    # run this function to get the interface initialized
    def init(self):
        print("ERROR: running a chatGPT interface parent class without implemented functionality.")

    # ask the interface a 'question' & get a 'response'
    def ask(self, question):
        print("ERROR: running a chatGPT interface parent class without implemented functionality.")

    # returns true if the interface can get a simple '2 + 2' answer from chatGPT for verification purposes
    # WARNING: ChatGPT isn't exact, so this *may* return false negatives or positives, but the question "2 + 2?" should be
    # simple enough for little variation.
    def is_working(self):
        # Verify the ChatGPT interface can be started up
        print("Initializing ChatGPT...", end="")
        if not initialized: self.init()

        print("Done!")
        # Verify if a question can be sent to the API & can receive a response
        question = "What is 2 + 2?"
        print("Sending question to ChatGPT: (", question, ") ...", end="")
        response = self.ask(question)
        print("Done!")

        # Verify if the response is, at least, *somewhat* logically consistent to the question
        if any(str in response for str in ("4", "four", "Four")):
            return True
        else:
            return False


class chatgpt_wrapper_interface(chat_gpt_interface):
    # run this function to get the interface initialized
    def init(self):
        global bot
        global initialized
        bot = ChatGPT()
        initialized = True


    # ask the interface a 'question' & get a 'response'
    def ask(self, question):
        response = bot.ask(question)
        return response



