def create_deck():
    """a function serves to creat a deck of 52 cards (without jokers)"""
    suits = ["\u2666", "\u2663", "\u2660", "\u2665"]
    values = ["A", "T", "J", "Q", "K"]
    cards = []
    for num in range(2, 10):
        values.append(str(num))
    
    for suit in suits:
        for value in values:
            cards.append(value + suit)
    
    return cards
        
