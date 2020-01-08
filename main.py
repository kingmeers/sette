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
        self.initial_chips = 100
        self.stats = {}
        self.CONSTANTS = {
            "QUEEN_OF_HEARTS": "QH"
        }
        self.OUTCOMES = {
            "WIN": "win",
            "LOSS": "loss",
            "DOUBLE": "double"
        }
        self.bets = [
            {
                "count": 0.5,
                "chips": 10
            },
            {
                "count": 1,
                "chips": 10
            },
            {
                "count": 2,
                "chips": 10
            },
            {
                "count": 3,
                "chips": 10
            },
            {
                "count": 4,
                "chips": 10
            },
            {
                "count": 5,
                "chips": 30
            },
            {
                "count": 6,
                "chips": 50
            },
            {
                "count": 7,
                "chips": 70
            }
        ]

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

            self.stats[id] = {
                "dealer_wins": 0,
                "dealer_losses": 0
            }

    def chooseDealer(self):
        self.dealer_id = random.choice(pydash.pluck(self.players, "id"))

        print("Chose the dealer, player {}".format(self.dealer_id))

    def handOutCards(self):
        print("–––––––––––––– Handing out cards ––––––––––––––")
        temp_players = []

        for player in self.players:
            if player["id"] is not self.dealer_id:
                if self.deck.size is 0:
                    self.rebuild()

                card = self.deck.deal()

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
                    self.stats[player["id"]]["dealer_losses"] += 1

                    dealer_pot -= self.bet(player["id"], self.count(player["id"]))

                    print(player["chips"], "Player {} won {} chips".format(player["id"], self.bet(player["id"], self.count(player["id"]))))

                    new_chips = player["chips"] + self.bet(player["id"], self.count(player["id"]))

                    if new_chips > 0:
                        temp_players.append(pydash.assign(
                            {},
                            player,
                            {
                                "chips": player["chips"] + self.bet(player["id"], self.count(player["id"]))
                            }
                        ))
                elif outcome[player["id"]] is self.OUTCOMES["LOSS"]:
                    self.stats[player["id"]]["dealer_wins"] += 1

                    dealer_pot += self.bet(player["id"], self.count(player["id"]))

                    print(player["chips"], "Player {} lost {} chips".format(player["id"], self.bet(player["id"], self.count(player["id"]))))

                    new_chips = player["chips"] - self.bet(player["id"], self.count(player["id"]))
                    if new_chips > 0:
                        temp_players.append(pydash.assign(
                            {},
                            player,
                            {
                                "chips": player["chips"] - self.bet(player["id"], self.count(player["id"]))
                            }
                        ))
                else:
                    dealer_pot += 0

        for player in self.players:
            if self.dealer_id is player["id"]:
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

    def bet(self, player_id, count):
        player_chips = 0
        bet_amount = 0

        for player in self.players:
            if player_id is player["id"]:
                player_chips = player["chips"]

        for bet in self.bets:
            if count == bet["count"]:
                if player_chips >= bet["chips"]:
                    bet_amount = bet["chips"]
                else:
                    bet_amount = player_chips

        return bet_amount

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

    def run(self, games):
        self.getPlayers(self.number_of_players)
        self.chooseDealer()

        self.play(games)

        print("––––––––––– STATS –––––––––––")
        pprint(self.stats)
        pprint(self.players)


print("–––––––– Initialising Sette e Mezzo –––––––– ")
sette = Sette()
sette.run(20)
