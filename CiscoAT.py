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
    # TODO: if only one possible answer, is memocard not question
    def get_answer_list(self):
        return self.answer_list

    def possible_answers(self):
        return [answer for answer in self.answer_list if answer != None]
    # TODO: check if user_inputted answer is correct answer
    # returns true if user_answer == answer
    def is_correct_answer(self, answer):
        return answer == self.correct_answer

    def __str__(self):
        return f"{self.question}\n1: {self.correct_answer}\n2: {self.wrong0}\n3: {self.wrong1}\n4: {self.wrong2}\nid: {self.id}"

# takes a csv file with a question on each line and possible answers seperated by comma, the first possible answer has to be the correct one
# parameter csv_file = "input_questions_and_answers_cisco.csv", if nothing else is specified.
# returns a list of Memocard objects each with a unique ID
def generate_cards(csv_file="input_questions_and_answers_cisco.csv") -> list[Memocard]:
    memocards = [] # init list for storing all memocards read from .csv file
    id = 0
    with open(csv_file, newline='') as questions_and_answers:
        memocard_generator = csv.reader(questions_and_answers)
        for row in memocard_generator:
            #TODO: change class memocard and this function to take unlimited amount of possible answers:
            # could be done quiite easily with the correct answer as a variable for it self, and then a list of wrong answers that is as long
            # as the rest of the line in the .csv file
            memocards.append(Memocard(id, row[0],row[1],row[2],row[3],row[4]))
            id = id + 1
    return memocards

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
        possible_answers = memocard.get_random_answer_list()
        for i, answer in enumerate(possible_answers):
            print(f"{i+1}: {answer}")
        answer = input_answer(len(memocard.possible_answers()))
        answer_list = memocard.get_answer_list()
        if memocard.is_correct_answer(answer_list[answer-1]):
            print("Answer is correct!")
        else:
            print("Answer is incorrect!")
            
if __name__ == "__main__":
    memocards = generate_cards()
    play_game_test(memocards)
    