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
def handle_next_question(index: Index, memocards: list[CiscoAT.Memocard], chosen_answer: Answer, player: Player):
    memocard = memocards[index.get_index()]
    if memocard.is_correct_answer(chosen_answer.get()):
        player.increment()
        ui.notify("Correct!", color="green")
    else:
        ui.notify("Incorrect!", color="red")
    index.increment()
    general_view.refresh()

#TODO create a function that checks if memocard contains picture and displays it if True
#TODO create a function that checks if answer is correct and updates player
@ui.refreshable
def score_board(player: Player, index: Index, total_questions: int):
    with ui.card().style("background-color: lightgrey; color: white; font-family: Courier;"):
        ui.label(f"Score: {player.get_score()}")
        ui.label(f"Questions Answered: {index.get_index()}/{total_questions}")
        ui.label(f"Total Questions: {total_questions}")

#TODO: implement what to do if question has picture
@ui.refreshable
def general_view(memocards: list[CiscoAT.Memocard], chosen_answer: Answer, index: Index, player: Player):
    memocard = memocards[index.get_index()]
    with ui.row():
        # Question and answers
        with ui.column():
            ui.label(memocard.question)
            answer_list = memocard.get_answer_list()
            radio = ui.radio(answer_list, value=answer_list[0], on_change=lambda: chosen_answer.set(radio.value))
            ui.button("Next Question", on_click=lambda: handle_next_question(index, memocards, chosen_answer, player))
        
        # Scoreboard
        with ui.card().style("background-color: lightgrey; color: white; font-family: Courier;"):
            ui.label(f"Score: {player.get_score()}")
            ui.label(f"Questions Answered: {index.get_index()}/{len(memocards)}")
            ui.label(f"Total Questions: {len(memocards)}")

player = Player()
chosen_answer = Answer()
memocards = CiscoAT.generate_cards()
index = Index()
general_view(memocards, chosen_answer, index, player)

ui.run(native=True)