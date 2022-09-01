from math import factorial

anwnser = None

while True:
    num = float(input('Enter your first number: '))
    op = input('Enter the operator: ')
    if op.lower() not in ['', ' ', '!', 'factorial']:
        num1 = float(input('Enter your second number: '))
        calculation = ('This is your calculation:', num,op,num1)
    else:
        calculation = ('This is your calculation:', num)
    confimation = True
    while confimation:
        print(calculation)
        c = input('Please comfirm (Y or n): ')
        if c == 'Y':
            if op.lower() in ['+', 'plus', 'add']:
                anwnser = num + num1
            elif op.lower() in ['-', 'minus', 'subtract']:
                anwnser = num - num1 
            elif op.lower() in ['X', '*', 'times', 'multipled by']:
                anwnser = num * num1
            elif op.lower() in ['', ' ', '!', 'factorial']:
                if num.is_integer():
                    anwnser = factorial(num)
                else:
                    print('The number has to be a whole number!')
            elif op.lower() in ['/', '÷', 'devided by']:
                if num1 != 0:
                    anwnser = num / num1
                else:
                    print('You can not devide by 0!')
            else:
                anwnser = 'That was not a valid operator choice!'
            print('Here is your awnser:', anwnser)
            confimation = False
        elif c == 'n':
            confimation = False
        else:
            print('Not a valid command!')
