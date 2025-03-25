from nicegui import ui
import quiz_backend

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
def handle_next_question(index: Index, memocards: list[quiz_backend.Memocard], chosen_answer: Answer, player: Player):
    memocard = memocards[index.get_index()]
    if memocard.is_correct_answer(chosen_answer.get()):
        player.increment()
        ui.notify("Correct!", color="green")
    else:
        ui.notify("Incorrect!", color="red")
    index.increment()
    general_view.refresh()

#TODO: implement what to do if question has picture
@ui.refreshable
def general_view(memocards: list[quiz_backend.Memocard], chosen_answer: Answer, index: Index, player: Player):
    memocard = memocards[index.get_index()]
    with ui.row():
        # Question and answers
        with ui.column():
            if memocard.get_is_last():
                ui.image(memocard.picture)#.props("height= 400 px") #picture veeeeeeery smalll - 
                ui.label("Game Over!")
                ui.button("Play Again", on_click=lambda: player.reset_score()) #implement reset score and play again in handle_next_question
            else:
                if memocard.has_picture:
                    ui.image(memocard.picture)
                ui.label(memocard.question)
                answer_list = memocard.get_answer_list()
                radio = ui.radio(answer_list, value=answer_list[0], on_change=lambda: chosen_answer.set(radio.value))
                ui.button("Next Question", on_click=lambda: handle_next_question(index, memocards, chosen_answer, player))
        
        # Scoreboard
        #TODO create a function that checks if memocard contains picture and displays it if True
        with ui.card().style("background-color: lightgrey; color: white; font-family: Courier;"):
            ui.label(f"Score: {player.get_score()}")
            ui.label(f"Questions Answered: {index.get_index()}/{len(memocards)}")
            ui.label(f"Total Questions: {len(memocards)}")

# TODO: handle what happens when the game is over, and the list of memocards is empty
player = Player()
chosen_answer = Answer()
memocards = quiz_backend.generate_cards()
index = Index()
general_view(memocards, chosen_answer, index, player)

ui.run(reload=True, native=True)
