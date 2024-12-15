# #imports
import random
#computer guesses num 1-20
def play():
    random_num=random.randint(1, 20)
    #user input num
    guess=input("guess a number between 1-20: ")
    #comp tells if <>=
    n_gueses=0
    while guess!=random_num:
        n_gueses=n_gueses+1
        # if >:/<
        if guess.isdigit():
            guess= int(guess)
            if guess>random_num:
                guess=(input("The number is too big: "))
            elif guess<random_num:
                guess=(input("The number is too small: "))
        else:   #if not digit 
            if guess== "x":    #exit the gane
                return
            elif guess== "s":    #uncover the nuber
                print(f'cheating, the number is {random_num}')
                return
            elif guess == "n":      #start anew game
                if input("Do want to start a new game? answer yes/no: ") == "yes":
                    play() #calling the function again 
                else:
                    return
                
    print(f'you guessed right! number of guesses it took you is {n_gueses}')

play()
    

