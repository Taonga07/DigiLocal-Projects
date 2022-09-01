import random

def roll():
    my_numbers = []
    
    for number in range(5):
        number = random.randint(1,6)
        my_numbers.append(number)
    print(' 1  2  3  4  5 ')
    print(my_numbers)
    return my_numbers

def check_score(my_numbers):
    score = 'nothing'
#    for i in range
    return score

def reroll(diceToReroll, my_numbers):
    #1, 4, 3
    #the input of what dices we want to roll
    diece_list = diceToReroll.split(',')
#    for dice in range(0, len(diece_list)):
    for dice in diece_list:
            my_numbers[int(dice)-1] = random.randint(1,6)
    print(' 1  2  3  4  5 ')
    print(my_numbers)

def rollAgain():
    while True:
        roll_again = input('Do you want to roll again(Y/n) ')
        if roll_again == 'Y' or roll_again == 'n':
            return roll_again
        else:
            print('You have misstyped somthing plaese try again')
            print(' 1  2  3  4  5 ')
            print(my_numbers)

if __name__ == "__main__":
    my_numbers = roll()
    for i in range(3):
        roll_again = rollAgain()
        if roll_again == 'Y':
            diceToReroll = input('Enter the dice/s number/s you want to reroll(a comma to seperate them) ')
            reroll(diceToReroll, my_numbers)
        elif roll_again == 'n':
            score = check_score(my_numbers)
            break 
    score = check_score(my_numbers)
    print('Finished with', score)