import random
import tkinter as tk
from tkinter import messagebox
root=tk.Tk()
root.title("Guessimg game")
root.geometry("300x200")
label=tk.Label(root,text="Guess a number between 1-20 ",font=("Arial",10))
label.pack(padx=20,pady=20)
guess_entry=tk.Entry(root)
guess_entry.pack()


def play():
    global random_num, n_gueses
    n_gueses = 1
    random_num = random.randint(1, 20)
    guess_entry.delete(0, tk.END)
    label.config(text="Guess a number between 1-20")
    
def start_game():
    global n_gueses
    guess=guess_entry.get()   
        
    if guess.isdigit():
        guess= int(guess)
      
        if guess < 1 or guess > 20:
                messagebox.showwarning("Out of Range", "Please guess a number between 1 and 20.")
        elif guess > random_num:
            n_gueses = n_gueses + 1
            label.config(text="The number is too big")
            
          
        elif guess < random_num:
            n_gueses = n_gueses + 1
            label.config(text="The number is too small")
            
          
        else:
            messagebox.showwarning("You guessed right!", f"Number of guesses it took you is {n_gueses}")    
    else:   #if not digit 
           
            label.config(text="Enter a valid number")
def cheat():
      messagebox.showwarning("Cheater!", f"The number is: {random_num} ")
     
                    
                    
    # messagebox.showwarning(f'you guessed right! number of guesses it took you is {n_gueses}')
    
play()

check_button=tk.Button(root,text="Click to check",command=start_game)
check_button.pack()

cheat_button=tk.Button(root,text="Reavil the number",command=cheat)
cheat_button.pack()

new_game_button=tk.Button(root,text="Start a new game",command=play)
new_game_button.pack()

exit_game=tk.Button(root,text="Exit the game", command=root.destroy)
exit_game.pack()

n_gueses=1
random_num=random.randint(1, 20)

root.mainloop()