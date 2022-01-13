import black_jack

def ask_if_play_more():
    choice = input("Play another round? (Y/N): ")

    while True: 
        if not type(choice) == str:
            choice = input("Give your response in 'Y' or 'N' only. Please try again: ") 
                    
        else:
            choice = choice.upper()
            if not choice == "Y" and not choice == "N":
                choice = input("Give your response in 'Y' or 'N' only. Please try again: ")
                        
            else:
                if choice == "Y":
                    print("Starting another round!")
                    return 1

                if choice == "N":
                    print("Thank you for playing! Goodbye.")
                    return 0


game1 = black_jack.Black_Jack()

run_check = 1
while run_check == 1:
    game1.play_game()
    run_check = ask_if_play_more()
    