#–––––– 7 & a half ––––––#
import pydealer

from pydealer.const import POKER_RANKS
from pprint import pprint
import pydash
import random

class Sette:
    def __init__(self):
        self.ranks = {"sette": {"Ace": 1,"King": .5,"Queen": .5,"Jack": .5,"7": 7,"6": 6,"5": 5,"4": 4,"3": 3,"2": 2}}
        self.deck = self.generateDeck()
        self.players = []
        self.dealer_id = 0
        self.number_of_players = 9
        self.has_QH_been_played = False
        self.bet = 10
        self.initial_chips = 100
        self.STATS = {
            "dealer_wins": 0,
            "dealer_losses": 0
        }
        self.CONSTANTS = {
            "QUEEN_OF_HEARTS": "QH"
        }
        self.OUTCOMES = {
            "WIN": "win",
            "LOSS": "loss",
            "DOUBLE": "double"
        }

    def generateDeck(self):
        cards = pydealer.Deck(ranks=self.ranks['sette'])
        cards.shuffle()
        deck = pydealer.Stack()

        cards_to_remove = ["8", "9", "10"]

        playing_cards = []

        for card in cards:
            if str(card.value) not in cards_to_remove:
                playing_cards.append(card)

        deck.add(playing_cards, end="top")

        deck.shuffle()

        return deck

    def getPlayers(self, number_of_players):
        player = {
            "hand": None,
            "chips": self.initial_chips
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

    def chooseDealer(self):
        self.dealer_id = random.choice(pydash.pluck(self.players, "id"))

        print("––")
        print(pydash.pluck(self.players, "id"))

        print("Chose the dealer, player {}".format(self.dealer_id))

    def handOutCards(self):
        print("–––––––––––––– Handing out cards ––––––––––––––")
        temp_players = []

        for player in self.players:
            if player["id"] is not self.dealer_id:
                if self.deck.size is 0:
                    self.rebuild()

                card = self.deck.deal()
                print("Handing out card ({}) to player {}, {} cards left in the deck".format(card, player["id"], self.deck.size))
                temp_players.append(pydash.assign(
                    {},
                    player,
                    {
                        "hand": card
                    }
                ))

        for player in self.players:
            if player["id"] is self.dealer_id:
                if self.deck.size is 0:
                    self.rebuild()

                card = self.deck.deal()
                print("Handing out card ({}) to dealer with id: {}, {} cards left in the deck".format(card, player["id"], self.deck.size))
                temp_players.append(pydash.assign(
                    {},
                    player,
                    {
                        "hand": card
                    }
                ))

        self.players = temp_players

    def count(self, player_id):
        count = 0

        for player in self.players:
            if player_id is player["id"]:
                for card in player["hand"]._cards:

                    count += self.ranks["sette"][card.value]


        return count

    def outcome(self):
        print("–––––––– Checking everyones card VS dealer ––––––––")
        round_outcome = {}
        dealer_count = 0

        for player in self.players:
            if self.dealer_id is player["id"]:
                dealer_count = self.count(player["id"])
                print("The dealer has {}".format(dealer_count))

        for player in self.players:
            if self.dealer_id is not player["id"]:
                count = self.count(player["id"])

                print("Player {} has {}".format(player["id"], count))

                if dealer_count >= count:
                    outcome = self.OUTCOMES["LOSS"]
                else:
                    outcome = self.OUTCOMES["WIN"]

                round_outcome[player["id"]] = outcome

        return round_outcome

    def round(self):
        outcome = self.outcome()
        print("–––––––– Exchanging money –––––––– ")
        temp_players = []
        dealer_pot = 0
        need_new_dealer = False

        for player in self.players:
            if self.dealer_id is not player["id"]:

                if outcome[player["id"]] is self.OUTCOMES["WIN"]:
                    self.STATS["dealer_losses"] += 1

                    dealer_pot -= self.bet
                    print(player["chips"], "Player {} won {} chips".format(player["id"], self.bet))

                    new_chips = player["chips"] + self.bet

                    if new_chips > 0:
                        temp_players.append(pydash.assign(
                            {},
                            player,
                            {
                                "chips": player["chips"] + self.bet
                            }
                        ))
                elif outcome[player["id"]] is self.OUTCOMES["LOSS"]:
                    # TODO: If player has no more chips, remove him from temp_players
                    self.STATS["dealer_wins"] += 1

                    dealer_pot += self.bet
                    print(player["chips"], "Player {} lost {} chips".format(player["id"], self.bet))

                    new_chips = player["chips"] - self.bet
                    if new_chips > 0:
                        temp_players.append(pydash.assign(
                            {},
                            player,
                            {
                                "chips": player["chips"] - self.bet
                            }
                        ))
                else:
                    dealer_pot += 0

        for player in self.players:
            if self.dealer_id is player["id"]:
                # TODO: If dealer has no more chips,
                # remove him from temp_players and choose new dealer
                new_dealer_chips = player["chips"] + dealer_pot

                if new_dealer_chips > 0:
                    temp_players.append(pydash.assign(
                        {},
                        player,
                        {
                            "chips": player["chips"] + dealer_pot
                        }
                    ))
                else:
                    need_new_dealer = True

        self.players = temp_players

        if need_new_dealer:
            self.chooseDealer()

    def bets(self):
        print("––––––––––– Placing bets –––––––––––")

    def rebuild(self):
        self.deck = self.generateDeck()

    def QHStillInPlay(self):
        return self.deck.find("Queen of Hearts")

    def play(self, games):
        for game in range(games + 1):
            if len(self.players) > 1:
                print(
                    """
    # ======================================================================== #
    #                                 Game {}                                  #
    # ======================================================================== #
                    """.format(game)
                )

                if not self.QHStillInPlay():
                    print("The Queen of Hearts came, rebuilding the deck.....")
                    self.rebuild()

                self.handOutCards()
                self.round()

    def run(self):
        self.getPlayers(self.number_of_players)
        self.chooseDealer()

        self.play(1000)

        print("––––––––––– STATS –––––––––––")
        pprint(self.STATS)
        pprint(self.players)


print("–––––––– Initialising Sette e Mezzo –––––––– ")
sette = Sette()
sette.run()
