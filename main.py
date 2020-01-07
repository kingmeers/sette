#–––––– 7 & a half ––––––#
import pydealer

from pydealer.const import POKER_RANKS
from pprint import pprint
import pydash

class Sette:
    def __init__(self):
        self.new_ranks = {"sette": {"Ace": 1,"King": .5,"Queen": .5,"Jack": .5,"7": 7,"6": 6,"5": 5,"4": 4,"3": 3,"2": 2}}
        self.deck = self.generateDeck()
        self.players = []

    def generateDeck(self):
        cards = pydealer.Deck(ranks=self.new_ranks['sette'])
        cards.shuffle()
        deck = pydealer.Stack()

        cards_to_remove = ["8", "9", "10"]

        playing_cards = []

        for card in cards:
            if str(card.value) not in cards_to_remove:
                playing_cards.append(card)
            else:
                print("Remove all cards matching: {} from the deck...".format(str(card.value)))

        deck.add(playing_cards, end="top")

        deck.shuffle()

        return deck

    def getPlayers(self, number_of_players):
        player = {
            "hand": None,
            "dealer": False
        }

        for id in range(1, number_of_players + 1):
            print("Adding player {}...".format(id))
            self.players.append(pydash.assign(
                {},
                player,
                {
                    "id": id
                }
            ))

    def handOutCards(self):
        # TODO: Make sure to always hand out the dealer's card LAST
        temp_players = []

        for player in self.players:
            card = self.deck.deal()
            print("Handing out card ({}) to player {}, {} cards left in the deck".format(card, player["id"], self.deck.size))
            temp_players.append(pydash.assign(
                {},
                player,
                {
                    "hand": card
                }
            ))

        self.players = temp_players

number_of_players = 3
print("–––––––– Initialising Sette e Mezzo –––––––– ")
s = Sette()
print("–––––––– Adding {} players to the game –––––––– ".format(number_of_players))
s.getPlayers(number_of_players)
# TODO: Pick dealer by dealing cards and seeing who gets the first ACE!
print("–––––––– Handing out cards to all the players –––––––– ")
s.handOutCards()
