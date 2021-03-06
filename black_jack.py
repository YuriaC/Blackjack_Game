import random

class Game:  # an abstract class
    
    def start_game():
        raise NotImplementedError
    
    def play_game():
        raise NotImplementedError
    
    def end_game():
        raise NotImplementedError

class Black_Jack(Game):

    def __init__(self):

        print("Welcome to Blackjack!")
        self.balance = 500
        self.card_deck = []
 
        # player attributes
        self.bet_amount = 0
        self.player_hand = []
        self.player_point = 0

        # dealer attributes
        self.dealer_hand = []
        self.dealer_point = 0

    def start_game(self):
        """Initialization for Blackjack game. User can choose to play a hand or not"""

        print (f"You are starting with ${self.balance}.", end= " ")
        
        if self.balance <= 1:
            print("Sorry, but you don't have enough fund to play...")
            return 0

        choice = input("Would you like to play a hand?(Y/N): ")
        while True: 
            if not type(choice) == str:
                choice = input("Give your response in 'Y' or 'N' only. Please try again: ") 
                    
            else:
                choice = choice.upper()
                if not choice == "Y" and not choice == "N":
                    choice = input("Give your response in 'Y' or 'N' only. Please try again: ")
                        
                else:
                    if choice == "Y":
                        print("Starting round!")
                        return 1

                    if choice == "N":
                        print(f"Do come back!")
                        return 0
                        
    def play_game(self):
        if self.start_game() == 1:
            if self.place_bet() == 1:
                self.card_deck = Black_Jack.create_deck()  
                if self.deal_card() == 1:
                    counter = 1
                    while self.player_term() != 0 and self.dealer_term() != 0:
                        self.player_term()
                        self.dealer_term()
                        counter += 1

                        if counter > 2:  # Seek better implementation in the future. Preferably smart detection of both "stay" decision
                            print("Seems like the game is at an impasse. The one with a higher hand value will win this round. ")
                            result = self.determine_winner()
                            self.dispense_prize(result)
                            break

        self.reset_game()

    def place_bet(self): 
        '''a function ask player to make a bet, and validates the bet amount'''
        
        bet_amount = input("Please place your bet: $")
        
        while True:
            temp = bet_amount.replace(".", "")
            
            if temp.isdigit():
                bet_amount = float(bet_amount)
                
                if bet_amount < 1:
                    bet_amount = input("The minimum bet is $1. Please try again: ")

                elif bet_amount > self.balance:
                    bet_amount = input("You can't afford this bet. Please try again: ")

                else:
                    self.bet_amount = bet_amount
                    self.balance -= bet_amount
                    print(f"You placed ${bet_amount} as bet. Your current balance is ${self.balance}" )
                    return 1

            else:
                bet_amount = input("Invalid input. Please give a positive number only: ")

    def deal_card(self):
        """ a function that initiate the game by serving both players 2 cards and predicts any possible occurrences of natural"""
        
        Black_Jack.shuffle_card(self.card_deck)
        # deal cards
        self.player_hand.append(self.card_deck.pop())
        self.dealer_hand.append(self.card_deck.pop())
        self.player_hand.append(self.card_deck.pop())
        self.dealer_hand.append(self.card_deck.pop())
        # update points
        self.player_point = Black_Jack.point_calculation(self.player_hand)
        self.dealer_point = Black_Jack.point_calculation(self.dealer_hand)
        
        # show dealted cards
        print("You are dealt:", end = " ")
        print(", ".join(self.player_hand)) 
        print(f"The dealer is dealt: {self.dealer_hand[0]}, Unknown")
        
        # check for natural
        if self.player_point == 21 and self.dealer_point == 21:  # in case of both get natural hands
            self.show_dealer_hand()
            print("Both the dealer and the player hit Blackjack!")
            self.dispense_prize(4)  # game ends with a tie
            return 0


        elif self.player_point == 21:    # in case of the player win by natural
            print("You hit the blackjack!")
            self.dispense_prize(1)
            return 0
    
        
        elif self.dealer_point == 21: # in case of the dealer win by natural
            self.show_dealer_hand() 
            print("The dealer hits the blackjack!")
            self.dispense_prize(3)
            return 0
        
        else:  # no natural occurs, game move on to the next phase
            return 1

    def player_term(self):
        """ a function that serves to guide player's action in player's term """

        action = input("Would you like to hit or stay? ")
        while True:
            if not type(action) == str:
                print("This is not a valid option.")
                action = input("Would you like to hit or stay? ")
            
            else:
                action = action.lower()

                if action == "hit":
            
                    if self.player_point < 21:
                        card = self.card_deck.pop()
                        self.player_hand.append(card)
                        self.player_point = Black_Jack.point_calculation(self.player_hand)
                        print(f"You are dealt: {card}")

                        if self.player_point > 21:
                            self.show_player_hand()
                            print(f"Your hand value is over 21.", end = " ")
                            self.dispense_prize(3)
                            return 0
                        
                        elif self.player_point == 21:
                            self.show_player_hand()
                            print("Blackjack!", end = " ")
                            self.dispense_prize(2)                            
                            return 0
                        
                        else:
                            self.show_player_hand()
                            action = input("Would you like to hit or stay? ")                   

                elif action == "stay":
                    self.show_dealer_hand()
                    return 1 
                
                else:
                    print("This is not a valid option.")
                    action = input("Would you like to hit or stay? ")

    def dealer_term(self):
        """ a function that serves to guide dealer's action in dealer's term """
        
        while True: 
            if self.dealer_point > 21:  # in case of dealer busts
                print("Dealer busts.", end = " ") 
                self.dispense_prize(2)
                return 0

            elif self.dealer_point == 21:  # incase of dealer wins
                print("The dealer hits the blackjack!", end = " ")
                self.dispense_prize(3)
                return 0

            elif self.dealer_point >= 17:  # in the case of dealer has point larger than 17 but haven't busted
                print("The dealer stays.")
                return 1
                
            else:  # in the case of dealer has hand <= 16 pts then dealer hits
                card = self.card_deck.pop()
                self.dealer_hand.append(card)
                self.dealer_point = Black_Jack.point_calculation(self.dealer_hand)
                print(f"The dealer hits and is dealt: {card}")
                print("The dealer has:", end = " ")
                print(", ".join(self.dealer_hand))  

    def show_player_hand(self):
        """ a function serves to print out cards on the player's hand """
        print("You now have:", end = " ")
        print(", ".join(self.player_hand)) 

    def show_dealer_hand(self):
        """ a function serves to print out cards on the dealer's hand """
        print("The dealer has:", end = " ")
        print(", ".join(self.dealer_hand)) 

    def dispense_prize(self, value): 
        """ a function serves to dispense appropriate prize to the player per the game result index (value)"""
        
        if value == 1:  # 1 = player win by natural case
            prize = self.bet_amount * 1.5  # reward per the rule
            self.balance += prize  # update player balance
            print(f"You win! You get ${prize}. Your balance is ${self.balance}")

        if value == 2:  # 2 = player win without natural case
            prize = self.bet_amount * 2  # reward per the rule
            self.balance += prize  # update player balance
            print(f"You win! You get ${prize}. Your balance is ${self.balance}")

        if value == 3:  # 3 = dealer win case
            print(f"You lose! You lose ${self.bet_amount}. Your balance is ${self.balance}")

        if value == 4:  # 4 = tie  case
            self.balance += self.bet_amount
            print(f"The game tied. You get ${self.bet_amount}. Your balance is ${self.balance}")

    def determine_winner(self):
        """ a function serves to determine the winner of a round if the round gets into impasse """
        
        print(f"Your hand value is: {self.player_point} points. The dealer's hand value is: {self.dealer_point} points")
        
        if self.player_point == self.dealer_point:# in case of tie
            return 4

        elif self.player_point < self.dealer_point:  # in the case of dealer win
            return 3
        
        else: # in the case of player win
            return 2 
            
    def reset_game(self):
        """ a function for cleaning up residual data"""

        self.card_deck.clear()
        self.bet_amount = 0
        self.player_hand.clear()
        self.player_point = 0
        self.dealer_hand.clear()
        self.dealer_point = 0      

    @staticmethod
    def point_calculation(lst):
        """ a static method that serves to provide point calculation logic """
        # J, Q, K, T all = 10 pts
        # numerical face has value equivalent to their number
        # A can be either 1 or 11
        point = 0 
        deck = sorted(lst, key=Black_Jack.sort_cards)
        for card in deck:
            if card[0] in ["J", "Q", "K", "T"]:
                point += 10
            
            elif card[0] == "A":
                temp = point
                if temp + 11 > 21:
                    point += 1
                
                else: 
                    point += 11

            else:
                point += int(card[0])

        return point 

    @staticmethod
    def sort_cards(card):
        "A function that serves to sort an existing card list. Sort by the order of numerical value, T/J/Q/K, and lastly A. "
        if card[0] in ["J", "Q", "K", "T"]:
            return 1
            
        elif card[0] == "A":
            return 2

        else:
            return 0 

    @staticmethod
    def shuffle_card(lst):
        """a function that shuffles a list of cards"""
        random.shuffle(lst)

    @staticmethod
    def create_deck():
        """a function serves to create a deck of 52 cards (without jokers)"""
        suits = ["\u2666", "\u2663", "\u2660", "\u2665"]
        faces = ["A", "T", "J", "Q", "K"]
        cards = []
        for num in range(2, 10):
            faces.append(str(num))
        
        for suit in suits:
            for face in faces:
                cards.append(face + suit)
        
        return cards
