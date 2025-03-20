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

# sets global variable for the memocard index and refreshes the general view
def handle_next_question(index: Index):
    index.increment()
    general_view.refresh()
    print("hej")
    pass

@ui.refreshable
def general_view(memocards: list[CiscoAT.Memocard], chosen_answer: Answer, index: Index):
    memocard = memocards[index.get_index()]
    ui.label(memocard.question)
    answer_list = memocard.get_answer_list()
    radio = ui.radio(answer_list, value=answer_list[0], on_change=lambda: chosen_answer.set(radio.value))
    ui.button("tryk her:", on_click=lambda: handle_next_question(index))

chosen_answer = Answer()
memocards = CiscoAT.generate_cards()
index = Index()
general_view(memocards, chosen_answer, index)

ui.run(native=True)