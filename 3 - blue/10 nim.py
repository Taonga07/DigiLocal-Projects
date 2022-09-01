player_coins = [0, 0]
player = 1
Stacks = [3, 4, 5]

while sum(Stacks) != 0:
    print('Player:', player, 'turn')
    print('Stack 1:', Stacks[0], ',Stack 2:', Stacks[1], ',Stack 3:', Stacks[2])
    Find_Stack = int(input('Chose a stack of coins: '))
    if Find_Stack >= 1 and Find_Stack <= 3 : 
        Stack_Coins = Stacks[Find_Stack-1]
        if Stack_Coins == 0:
            print('No coins here!')
            continue
        if Stack_Coins >= 3:
            Max = 3
        else:
            Max = Stack_Coins
        Coins = int(input(f'Chose your amount(min: 1, max: {Max}): '))
        if (Coins >= 1 and Coins <= 3) and (Stack_Coins-Coins >= 0):
            player_coins[player-1] += Coins
            Stacks[Find_Stack-1] -= Coins
            player = 3 - player
print('player', 3-player, 'wins!')