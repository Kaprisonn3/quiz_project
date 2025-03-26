import csv
from random import shuffle

class Memocard:
    def __init__(self, id: int, question: str, correct_answer: str="", incorrect_answers: list[str]=[], picture: str='*', is_last: bool=False) -> None:
        self.id = id
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answers
        self.picture = picture
        self.is_last = is_last
        self.answer_list = [self.correct_answer] + self.incorrect_answers
        # randomize answer list
        shuffle(self.answer_list)
        self.has_picture = False if picture == '*' else True
    # returns list of possible answers.
    # if no incorrect answers are given, (i.e. it is an actuual memocard) this returns a list with only the correct answer.
    def get_answer_list(self):
        return self.answer_list
    def is_correct_answer(self, answer):
        return answer == self.correct_answer
    def get_is_last(self):
        return self.is_last
    def __str__(self):
        answers = "\n".join([f"{i+1}: {answer}" for i, answer in enumerate(self.answer_list)])
        return f"Question: {self.question}\n{answers}\nid: {self.id}\nhas_picture: {self.has_picture}"

# takes a csv file with a question on each line and possible answers seperated by comma, the first possible answer has to be the correct one
# parameter csv_file = "input_questions_and_answers_cisco.csv", if nothing else is specified.
# returns a list of Memocard objects each with a unique ID
def generate_cards(csv_file="input_questions_and_answers_cisco.csv") -> list[Memocard]:
    memocards = []  # init list for storing all memocards read from .csv file
    id = 0
    with open(csv_file, newline='', encoding='utf-8') as questions_and_answers:
        memocard_generator = csv.reader(questions_and_answers)
        for id, row in enumerate(memocard_generator):
            if len(row) >= 2:  # Ensure at least a question and a correct answer exist
                question = row[0].strip()
                correct_answer = row[1].strip()
                incorrect_answers = [ans.strip() for ans in row[2:-1]]
                picture = row[-1].strip()
                memocards.append(Memocard(id, question, correct_answer, incorrect_answers, picture))
    # Adding last question to handle end of quiz and out-of-bounds errors
    memocards.append(Memocard(-1,"LAST QUESTION TEXT", "", picture="quiz_done.jpg", is_last=True))
    return memocards 

################## FOLLOWING FUNCTIONS ARE FOR TESTING PURPOSES AND SHOULD BE REMOVED (or commented out;)) WHEN IMPLEMENTED IN FRONTEND ###################

# range is the length of the list with possible answers. ie. if 3 possible answers range is 3
# returns an int in rangge(0,max_answers)
# def input_answer(max_answers) -> int:
#     while True:
#         try:
#             answer_string = input("What is your answer:")
#             answer = int(answer_string)
#         except ValueError:
#             print(f"Please enter an integer from 1 to {max_answers}")
#             continue
#         if answer < 0 or answer > max_answers:
#             print(f"Please enter an integer from 1 to {max_answers}")
#             continue
#         break
#     return answer

# def play_game_test(memocards) -> None:
#     shuffle(memocards)

#     for memocard in memocards:
#         #TODO: shuffle the questions and make sure that the answer is not always located as first option
#         print(memocard.question)
#         possible_answers = memocard.get_answer_list()
#         for i, answer in enumerate(possible_answers):
#             print(f"{i+1}: {answer}")
#         answer = input_answer(len(possible_answers))
#         answer_list = memocard.get_answer_list()
#         if memocard.is_correct_answer(answer_list[answer-1]):
#             print("Answer is correct!")
#         else:
#             print("Answer is incorrect!")
