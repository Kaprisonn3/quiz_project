import csv
from random import shuffle

class Memocard:
    def __init__(self, id: int, question: str, correct_answer: str, incorrect_answers=[], picture=None) -> None:
        self.id = id
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answers
        self.picture = picture
        # answer_list is a randomized list of possible answers
        self.answer_list = [self.correct_answer] + self.incorrect_answers
        shuffle(self.answer_list)
    # returns list of possible answers.
    # if no incorrect answers are given, (i.e. it is an actuual memocard) this returns a list with only the correct answer.
    def get_answer_list(self):
        return self.answer_list
    # returns true if user_answer == answer
    def is_correct_answer(self, answer):
        return answer == self.correct_answer
    def __str__(self):
        answers = "\n".join([f"{i+1}: {answer}" for i, answer in enumerate(self.answer_list)])
        return f"Question: {self.question}\n{answers}\nid: {self.id}"

# takes a csv file with a question on each line and possible answers seperated by comma, the first possible answer has to be the correct one
# parameter csv_file = "input_questions_and_answers_cisco.csv", if nothing else is specified.
# returns a list of Memocard objects each with a unique ID
def generate_cards(csv_file="input_questions_and_answers_cisco.csv") -> list[Memocard]:
    memocards = []  # init list for storing all memocards read from .csv file
    id = 0
    with open(csv_file, newline='') as questions_and_answers:
        memocard_generator = csv.reader(questions_and_answers)
        for row in memocard_generator:
            question = row[0]
            correct_answer = row[1]
            # All entries between the correct answer and the last entry are incorrect answers
            incorrect_answers = row[2:-1]
            # Check if the last entry is a picture or asetrisk '*' which indicates no picture.
            picture = None if row[-1] == '*' else row[-1]
            memocards.append(Memocard(id, question, correct_answer, incorrect_answers, picture))
            id += 1
    return memocards

################## FOLLOWING FUNCTIONS ARE FOR TESTING PURPOSES AND SHOULD BE REMOVED (or commented out;)) WHEN IMPLEMENTED IN FRONTEND ###################


# range is the length of the list with possible answers. ie. if 3 possible answers range is 3
# returns an int in rangge(0,max_answers)
def input_answer(max_answers) -> int:
    while True:
        try:
            answer_string = input("What is your answer:")
            answer = int(answer_string)
        except ValueError:
            print(f"Please enter an integer from 1 to {max_answers}")
            continue
        if answer < 0 or answer > max_answers:
            print(f"Please enter an integer from 1 to {max_answers}")
            continue
        break
    return answer

def play_game_test(memocards) -> None:
    shuffle(memocards)

    for memocard in memocards:
        #TODO: shuffle the questions and make sure that the answer is not always located as first option
        print(memocard.question)
        possible_answers = memocard.get_answer_list()
        for i, answer in enumerate(possible_answers):
            print(f"{i+1}: {answer}")
        answer = input_answer(len(possible_answers))
        answer_list = memocard.get_answer_list()
        if memocard.is_correct_answer(answer_list[answer-1]):
            print("Answer is correct!")
        else:
            print("Answer is incorrect!")

