# Hongfei Jiang's submission for mini project
#
# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random

# helper functions

def number_to_name(number):
    name = 'undef'
    if 0 == number :
        name = 'rock'
    elif 1 == number :
        name = 'Spock'
    elif 2 == number :
        name = 'paper'
    elif 3 == number :
        name = 'lizard'
    elif 4 == number :
        name = 'scissors'
    else :
        print 'Warning: the number input should be a integer in [0,4]'
        
    return name

def name_to_number(name):
    number = -1
    name = name.lower()
    
    if  'rock' == name :
        number = 0
    elif 'spock' == name :
        number = 1
    elif 'paper' == name :
        number = 2
    elif 'lizard' == name :
        number = 3
    elif 'scissors' == name :
        number = 4
    else :
        print 'Warning: the name input should be a string of (rock,Spock,paper,lizard,scissors)'
        
    return number

def rpsls(name): 

    winner = 'Player'
    # convert name to player_number using name_to_number
    player_number = name_to_number(name)
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(5)
    # compute difference of player_number and comp_number modulo five
    diff = (comp_number - player_number) % 5
    # use if/elif/else to determine winner
    if 1 == diff or 2 == diff:
        winner = 'Computer'
    elif 3 == diff or 4 == diff:
        winner = 'Player'
    elif 0 == diff:
        winner = 'tie'
    else:
        winner = 'undef'
    
    
    # convert comp_number to name using number_to_name
    comp_name = number_to_name(comp_number)
    
    # print results
    print 'Player chooses', name
    print 'Computer chooses', comp_name
    if 'tie' == winner:
        print 'Player and computer tie!\n'
    elif 'undef' == winner:
        print 'The game goes wrong, replay plz\n'
    else:
        print winner, 'wins!\n'

# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric