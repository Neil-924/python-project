import random

class Quiz:
    def __init__(self):
        self.score = 0
    
    def start(self):
        print("This is a 10 questions math quiz, GOODLUCK!")
        print()
        for i in range(1, 11):
            num1 = self.getNum()
            num2 = self.getNum()
            correctAnswer, operation = self.getCorrectAnswer(random.randint(1, 4), num1, num2)
            userAnswer = int(input(f"{i}. {num1} {operation} {num2} = "))

            if userAnswer == correctAnswer:
                self.score += 1
                print("Congratulations you gained 1 point")
                print()
            else:
                print("Wrong, you gained 0 point for that one")
                print()
        
        print(f"Final score: {self.score} / 10")

    def getNum(self):
        return int(random.random() * 100)
    
    def getCorrectAnswer(self, ope, num1, num2):
        match ope:
            case 1:
                return num1 + num2, "+"
            case 2:
                return num1 - num2, "-"
            case 3:
                return num1 * num2, "*"
            case 4:
                if num2 == 0:
                    return "cannot divide", "//"
                else:
                    return num1 // num2, "//"
            case _:
                return "Unknown operation"
    
quiz = Quiz()
quiz.start()