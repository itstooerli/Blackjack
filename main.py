import random
import math
import copy

class Card:
  def __init__(self, suit, card, value):
    # Stores the suit of the card, e.g. Clubs
    self.suit = suit

    # Stores the number of the card, e.g. K or 3
    self.card = card

    # Stores the value of the card for this game, e.g. K = 10, 3 = 3
    self.value = value

class Hand:
  def __init__(self, cards, score, num_aces):
    # Stores an array of Cards
    self.cards = cards
    
    # Stores the cumulative score
    self.score = score

    # Stores the number of aces, since in Blackjack, Ace = 11 or 1
    self.num_aces = num_aces

class Seat:
  def __init__(self, type):
    # Stores the type of seat this is
    # 0 - Player
    # 1 - AI 
    # 2 - Split
    self.type = type

    # Stores the seat's hand
    self.hand
    
    # If the type is a player, how much money does the player have
    self.money
    
    # If the type is a split hand, what seat is it associated with
    self.splitAssoc

def create_deck(num_decks, suit_values, card_values):
  # Define basic components of a deck
  deck = []
  suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
  cards = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]

  # Create deck with cards based on provided values and total number of decks
  for i in range(num_decks):
    for suit in suits:
      for card in cards:
        deck.append(Card(suit_values[suit], card, card_values[card]))

  return deck

def deal_cards(deck):
  # Initialize variables
  player_cards = []
  dealer_cards = []
  player_hand = Hand(player_cards, 0, 0)
  dealer_hand = Hand(dealer_cards, 0, 0)
  num_cards = 0

  while num_cards < 2:
    # Dealing the player's card
    player_card = random.choice(deck)
    player_hand.cards.append(player_card)
    player_hand.score += player_card.value
    
    if player_card.card == "A":
      player_hand.num_aces += 1
      
    deck.remove(player_card)

    # Dealing the dealer's card
    dealer_card = random.choice(deck)
    dealer_hand.cards.append(dealer_card)
    dealer_hand.score += dealer_card.value

    if dealer_card.card == "A":
      dealer_hand.num_aces += 1
      
    deck.remove(dealer_card)

    num_cards = num_cards + 1

  # If hand receives two aces, treat one of the aces as a 1
  if player_hand.score == 22:
    player_cards[1].value = 1
    player_hand.score = 12

  if dealer_hand.score == 22:
    dealer_cards[1].value = 1
    dealer_hand.score = 12
  
  return player_hand, dealer_hand

def deal_new_card(deck, hand):
  # Deal a new card from the provided deck to the provided cards and update the provided score
  new_card = random.choice(deck)
  hand.cards.append(new_card)
  hand.score += new_card.value
  deck.remove(new_card)

  if new_card.card == "A":
    hand.num_aces += 1

  if hand.score > 21 and hand.num_aces > 0:
    hand.score -= 10
    hand.num_aces -= 1

def display_cards(player_hand, dealer_hand, hidden):
  # Display dealer's cards, if hidden then only first card is shown
  print("Dealer's cards:", end=" ")
  if hidden:
    print(str(dealer_hand.cards[0].card) + str(dealer_hand.cards[0].suit) + " XX", end=" ")
    print("Value: " + str(dealer_hand.cards[0].value))
  else:
    for card in dealer_hand.cards:
      print(str(card.card) + str(card.suit), end=" ")
    print("Value: " + str(dealer_hand.score))

  # Display player's cards
  print("Player's cards:", end=" ")
  for card in player_hand.cards:
    print(str(card.card) + str(card.suit), end=" ")

  print("Value: " + str(player_hand.score))

  print()

def ask_continue_game():
  player_choice = input("Enter Q to quit or any other key to continue: ")
  print()
  return player_choice.upper() != "Q"

def shuffle_deck(new_deck):
  curr_deck = copy.deepcopy(new_deck)
  cutoff = random.randrange(math.floor(len(new_deck) * 0.25), math.floor(len(new_deck) * 0.5))
  return curr_deck, cutoff

def blackjack_game(num_decks):
  # TODO: Provide option to decide num_decks as input, initial money, how often cards are cleared
  # TODO: Provide option to add more AI players
  # TODO: Implement Betting (Insurance, Double Down, Split)
  # TODO: Import time to space out displays

  # Define suit values for blackjack
  suit_values = {"Spades":"\u2664", "Hearts":"\u2661", "Clubs":"\u2667", "Diamonds":"\u2662"}

  # Define card values for blackjack
  card_values = {"A":11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "J":10, "Q":10, "K":10}

  # Create a new deck for blackjack
  new_deck = create_deck(num_decks, suit_values, card_values)
  curr_deck, cutoff = shuffle_deck(new_deck)  

  # Initialize buy-in
  player_money = 1000
  
  # Play Game
  while(True):
    # print("Number of cards left: " + str(len(curr_deck)))
    
    # Reshuffle deck if we're at the cutoff point
    if len(curr_deck) < cutoff:
      curr_deck, cutoff = shuffle_deck(new_deck)  

    while (True):
      print("Current cash pool: " + str(player_money))
      player_bet = input("Enter bet: ")

      try:
        player_bet = float(player_bet)
        if player_bet < 0 or player_bet > player_money:
          print("Not enough money. Please try again.")
          continue
      except ValueError:
        print("Not a valid input. Please try again.")
        continue

      if player_bet % 0.5 != 0:
        player_bet = round(player_bet * 2) / 2
      
      break
      
    # Deal the new hand
    player_hand, dealer_hand = deal_cards(curr_deck)
    display_cards(player_hand, dealer_hand, True)

    # Check if player has blackjack
    if player_hand.score == 21:
      display_cards(player_hand, dealer_hand, False)
      if dealer_hand.score == 21:
        print("Stand-off!")
        if ask_continue_game():
          continue
        else:
          break
      else:
        print("Blackjack!")
        player_money += player_bet * 1.5
        if ask_continue_game():
          continue
        else:
          break

    # Check if dealer has blackjack
    if dealer_hand.score == 21:
      display_cards(player_hand, dealer_hand, False)
      print("Dealer has blackjack! Player loses.")
      player_money -= player_bet
      if ask_continue_game():
        continue
      else:
        break

    # Player plays
    while player_hand.score < 21:
      if len(player_hand.cards) == 2:
        player_choice = input("Enter H to hit, D to double down, S to stand: ")
        if (len(player_choice) != 1 or player_choice.upper() not in ("H", "D", "S")):
          print("Invalid Choice.")
          continue
      else:
        player_choice = input("Enter H to hit, S to stand: ")
        if (len(player_choice) != 1 or player_choice.upper() not in ("H", "S")):
          print("Invalid Choice.")
          continue

      # Player Hits
      if player_choice.upper() == "H":
        deal_new_card(curr_deck, player_hand)
        display_cards(player_hand, dealer_hand, True)
      # Player Doubles Down
      elif player_choice.upper() == "D":
        player_bet *= 2
        deal_new_card(curr_deck, player_hand)
        display_cards(player_hand, dealer_hand, True)
        break
      # Player Stands
      elif player_choice.upper() == "S":
        break

    # Player Busts
    if player_hand.score > 21:
      display_cards(player_hand, dealer_hand, False)
      print("Player Busts! Player loses.")
      player_money -= player_bet
      if ask_continue_game():
        continue
      else:
        break

    # Dealer Hits
    while dealer_hand.score < 17:
      deal_new_card(curr_deck, dealer_hand)
      display_cards(player_hand, dealer_hand, False)

    # Determine Winners/Payouts
    display_cards(player_hand, dealer_hand, False)
    if dealer_hand.score > 21:
      print("Dealer Busts! Player Wins.")
      player_money += player_bet
    elif player_hand.score == dealer_hand.score:
      print("Stand-off!")
    elif player_hand.score > dealer_hand.score:
      print("Player Wins!")
      player_money += player_bet
    else:
      print("Player loses.")
      player_money -= player_bet

    print("Player: " + str(player_money))
      
    if ask_continue_game():
      continue
    else:
      break

blackjack_game(6)