from nicegui import ui
import quiz_backend

class Index():
    def __init__(self, val=0):
        self.val = val
    def increment(self):
        self.val = self.val + 1
    def reset_index(self):
        self.val = 0
    def get_index(self):
        return self.val

class Answer():
    def __init__(self):
        self.answer = ""
    def set(self, answer):
        self.answer = answer
    def get(self):
        return self.answer

#TODO: implement player name and functionality to save scores of players somewhere.
class Player():
    def __init__(self):
        self.score = 0
        self.name = "" # add player name functionality
    def increment(self):
        self.score = self.score + 1
    def get_score(self):
        return self.score 
    def reset_score(self):
        self.score = 0
    def set_player_name(self,name):
        self.name = name
    def get_player_name(self):
        return self.name

# sets global variable for the memocard index and refreshes the general view
def handle_next_question(index: Index, memocard: quiz_backend.Memocard, chosen_answer: Answer | None, player: Player) -> None:
    if memocard.is_last: 
        player.reset_score()
        index.reset_index()
        general_view.refresh()
    else:
        print(f"{chosen_answer.get()} == {memocard.correct_answer}")
        if memocard.is_correct_answer(chosen_answer.get()):
            player.increment()
            ui.notify("Correct!", color="green")
        else:
            ui.notify("Incorrect!", color="red")
        index.increment()
        general_view.refresh()

#TODO: implement what to do if question has picture
@ui.refreshable
def general_view(memocards: list[quiz_backend.Memocard], chosen_answer: Answer, index: Index, player: Player) -> None:
    memocard = memocards[index.get_index()]
    with ui.row().style("border: 2px solid black; padding: 10px; margin: 10px;"):

        # question, answers and picture:
        with ui.column().style("flex: 2; padding: 10px;"):
            if memocard.get_is_last():
                ui.image(memocard.picture).style("width: 629px; height: 252px; object-fit: scale-down;")
                ui.button("Play Again", on_click=lambda: handle_next_question(index,memocard,None,player))
            else:
                if memocard.has_picture:
                    ui.image(memocard.picture).style("width: 550px; height: 400px; object-fit: scale-down;")
                ui.label(memocard.question).style("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
                answer_list = memocard.get_answer_list()
                radio = ui.radio(answer_list, value=answer_list[0], on_change=lambda: chosen_answer.set(radio.value))
                chosen_answer.set(radio.value) # ensures that chosen answer is set even though radio is not changed
                ui.button("Next Question", on_click=lambda: handle_next_question(index, memocard, chosen_answer, player))
        
        # Scoreboard
        with ui.card().style("background-color: lightgrey; color: white; font-family: Courier;"):
            ui.label(f"Score: {player.get_score()}").style(LABEL_STYLE)
            ui.label(f"Questions Answered: {index.get_index()}/{len(memocards)-1}")
            ui.label(f"Total Questions: {len(memocards)-1}")

# Define a reusable style for labels
LABEL_STYLE = "background-color: lightgrey; color: white; font-family: Courier;"

def main() -> None:
    player = Player()
    chosen_answer = Answer()
    try:
        memocards = quiz_backend.generate_cards()
    except (FileNotFoundError, ValueError) as e:
        ui.notify(f"Error loading quiz data: {e}", color="red")
        memocards = []
    index = Index()
    general_view(memocards, chosen_answer, index, player)
    ui.run()


main()
