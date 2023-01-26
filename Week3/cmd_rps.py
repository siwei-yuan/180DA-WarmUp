import random

if __name__ == "__main__":

    while True:
        user_input = input("Select from ROCK, PAPER, SCISSORS ......")
        user_input = user_input.upper()
        
        comp_output = ["ROCK", "PAPER", "SCISSORS"]

        if user_input not in comp_output:
            print("INVALID INPUT!")
            pass
        
        comp_output = comp_output[random.randint(0,2)]

        print("Computer chose: " + comp_output)

        if user_input == comp_output:
            print("TIE!")
        elif user_input == "ROCK":
            if comp_output == "PAPER":
                print("YOU LOSE!")
            elif comp_output == "SCISSORS":
                print("YOU WIN!")
        elif user_input == "PAPER":
            if comp_output == "SCISSORS":
                print("YOU LOSE!")
            elif comp_output == "ROCK":
                print("YOU WIN!")
        else:
            if comp_output == "ROCK":
                print("YOU LOSE!")
            elif comp_output == "PAPER":
                print("YOU WIN!")