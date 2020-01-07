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
        remove = ["8", "9", "10"]
        playing_cards = []

        for card in cards:
            if str(card.value) not in remove:
                playing_cards.append(card)

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

s = Sette()
s.getPlayers(3)
s.handOutCards()
