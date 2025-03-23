from nicegui import ui
import CiscoAT

class Index():
    def __init__(self, val=0):
        self.val = val
    def increment(self):
        self.val = self.val + 1
    def get_index(self):
        return self.val

class Answer():
    def __init__(self):
        self.answer = ""
    def set(self, answer):
        self.answer = answer
        print(answer)
    def get(self):
        return self.answer

class Player():
    def __init__(self):
        self.score = 0
    def increment(self):
        self.score = self.score + 1
    def get_score(self):
        return self.score 
    def reset_score(self):
        self.score = 0

# sets global variable for the memocard index and refreshes the general view
def handle_next_question(index: Index):
    index.increment()
    general_view.refresh()
    print("hej")
    pass

#TODO create a function that checks if memocard contains picture and displays it if True
#TODO create a function that checks if answer is correct and updates player
@ui.refreshable
def general_view(memocards: list[CiscoAT.Memocard], chosen_answer: Answer, index: Index):
    memocard = memocards[index.get_index()]
    ui.label(memocard.question)
    answer_list = memocard.get_answer_list()
    radio = ui.radio(answer_list, value=answer_list[0], on_change=lambda: chosen_answer.set(radio.value))
    ui.button("tryk her:", on_click=lambda: handle_next_question(index))

# score_board: Should display at the right and show the current score of the player.
# should be a ui.card or the like with a different background color maybe a light grey. 
# displays correct answers, questions answered so far and total answers. 
def score_board():
    pass

chosen_answer = Answer()
memocards = CiscoAT.generate_cards()
index = Index()
general_view(memocards, chosen_answer, index)

ui.run(native=True)