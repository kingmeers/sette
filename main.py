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
        self.dealer_chips_amount = 0
        self.number_of_players = 5
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
            "hand": pydealer.Stack(),
            "chips": self.initial_chips
        }

        for id in range(1, number_of_players + 1):
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

        print(
            """

        ===================================
        ||                               ||
        ||    Picking a new dealer...    ||
        ||                               ||
        ===================================


          _____
         |A .  | _____
         | /.\ ||A ^  | _____
         |(_._)|| / \ ||A _  | _____
         |  |  || \ / || ( ) ||A_ _ |
         |____V||  .  ||(_'_)||( v )|
                |____V||  |  || \ / |
                       |____V||  .  |
                              |____V|


          The dealer is now Player {}

            """.format(self.dealer_id)
        )

    def handOutCards(self):
        temp_players = []

        for player in self.players:
            if player["id"] is not self.dealer_id:
                if self.deck.size is 0:
                    self.rebuild()

                hand = pydealer.Stack()

                card = self.deck.deal()

                hand.add(card)

                temp_players.append(pydash.assign(
                    {},
                    player,
                    {
                        "hand": hand
                    }
                ))

        for player in self.players:
            if player["id"] is self.dealer_id:
                if self.deck.size is 0:
                    self.rebuild()

                hand = pydealer.Stack()

                card = self.deck.deal()

                hand.add(card)

                temp_players.append(pydash.assign(
                    {},
                    player,
                    {
                        "hand": hand
                    }
                ))

        self.players = temp_players

    def count(self, player_id, extra_cards = []):
        count = 0

        if extra_cards:
            for player in self.players:
                if player_id is player["id"]:
                    hand = pydealer.Stack()

                    hand.add(player["hand"])

                    for card in extra_cards:
                        hand.add(card)

                    for card in hand:
                        count += self.ranks["sette"][card.value]
        else:
            for player in self.players:
                if player_id is player["id"]:
                    for card in player["hand"]:
                        count += self.ranks["sette"][card.value]

        return count

    def cards(self, player_id, is_dealer, nonDealerHand):
        strNonDealerHand = []
        for index, card in enumerate(nonDealerHand):
            nonDealerCard = """
     ┌─────────┐
     │{}        │
     │         │
     │         │
     │    {}    │
     │         │
     │         │
     │        {}│
     └─────────┘""".format(card[0], card[1], card[0]).split('\n')
            strNonDealerHand.append(nonDealerCard)

        if is_dealer:
            print("    # ===================== Player {} ===================== #".format(player_id))
            print("                           The Dealer                       ")
        else:
            print("")
            print("    # ===================== Player {} ===================== #".format(player_id))

        for i in zip(*strNonDealerHand):
            print(" ".join(i))

    def suit_emoji(self, suit):
        emojis = {
            "C": "♧",
            "D": "♢",
            "H": "♡",
            "S": "♤"
        }

        return emojis[suit]

    def cards_list(self, cards):
        hand = []

        for card in cards._cards:
            hand.append([
                card.abbrev[0],
                self.suit_emoji(card.abbrev[1])
            ])

        return hand

    def isPlayerBroken(self, player_id, extra_cards):
        for player in self.players:
            if player["id"] is player_id:
                return self.count(player_id, extra_cards) > 7.5

    def outcome(self):
        round_outcome = {}
        temp_players = self.players
        dealer_count = 0
        player_counts = {}
        extra_cards = {}

        for player in self.players:
            extra_cards[player["id"]] = []

        for player in temp_players:
            player_counts[player["id"]] = {}

            if self.dealer_id is player["id"]:
                dealer_count = self.count(player["id"])

        for player in temp_players:
            if self.dealer_id is not player["id"]:
                player_option = ""
                count = self.count(player["id"])
                cards = self.cards_list(player["hand"])

                self.cards(player["id"], False, cards)

                print(
                    """
     They placed a bet of {} chips
                    """.format(self.bet(player["id"], count))
                )

                print("""

    ============================================================
            HERE YOU CAN SELECT IF YOU WANT MORE CARDS

                    (h) for HIT, (p) for PASS
    ============================================================

                """)

                is_broken = self.isPlayerBroken(player["id"], extra_cards[player["id"]])

                while player_option is not "p" and not is_broken:
                    player_option = input("Player >> ")

                    if player_option is "p":
                        pass
                    elif player_option is "h":
                        card = self.deck.deal()

                        extra_cards[player["id"]].append(card)

                        hand = pydealer.Stack()

                        hand.add(player["hand"])

                        for card in extra_cards[player["id"]]:
                            hand.add(card)

                        self.cards(player["id"], False, self.cards_list(hand))

                        is_broken = self.isPlayerBroken(player["id"], extra_cards[player["id"]])

                        if is_broken:
                            self.broken(player["id"])

                count = self.count(player["id"], extra_cards[player["id"]])

                player_counts[player["id"]]["count"] = count
                player_counts[player["id"]]["is_broken"] = is_broken

        for player in temp_players:
            if self.dealer_id is player["id"]:
                player_option = ""
                dealer_count = self.count(player["id"])
                cards = self.cards_list(player["hand"])

                self.cards(player["id"], True, cards)

                print("""

    ============================================================
             THE DEALER IS NOW DECIDING TO HIT OR PASS

                    (h) for HIT, (p) for PASS
    ============================================================

                """)

                is_dealer_broken = self.isPlayerBroken(player["id"], extra_cards[player["id"]])

                while player_option is not "p" and not is_dealer_broken:
                    player_option = input("Dealer >> ")

                    if player_option is "p":
                        pass
                    elif player_option is "h":
                        card = self.deck.deal()

                        extra_cards[player["id"]].append(card)

                        hand = pydealer.Stack()

                        hand.add(player["hand"])

                        for card in extra_cards[player["id"]]:
                            hand.add(card)

                        self.cards(player["id"], False, self.cards_list(hand))

                        is_dealer_broken = self.isPlayerBroken(player["id"], extra_cards[player["id"]])

                        if is_dealer_broken:
                            self.broken(player["id"])

                for opponent in self.players:
                    if self.dealer_id is not opponent["id"]:
                        if (
                            player_counts[opponent["id"]]["is_broken"] or
                            dealer_count >= player_counts[opponent["id"]]["count"]
                        ) and not is_dealer_broken:
                            print(opponent["id"], "Recorded LOSS")
                            outcome = self.OUTCOMES["LOSS"]
                        else:
                            print(opponent["id"], "Recorded WIN")
                            outcome = self.OUTCOMES["WIN"]

                        round_outcome[opponent["id"]] = outcome

        return round_outcome

    def validateBet(self, bet):
        if bet > 0:
            return bet
        else:
            return 0

    def round(self):
        outcome = self.outcome()
        temp_players = []
        need_new_dealer = False

        self.dealer_chips_amount = self.dealer_chips()

        print(
        """
    ||==============||
    || GAME RESULTS ||
    ||==============||
        """
        )


        for player in self.players:
            if self.dealer_id is not player["id"]:
                bet = self.bet(player["id"], self.count(player["id"]))

                if outcome[player["id"]] is self.OUTCOMES["WIN"]:
                    self.stats[player["id"]]["dealer_losses"] += 1

                    new_chips = player["chips"] + self.validateBet(self.dealer_return(self.dealer_chips_amount, bet))

                    print("    🃏  Player {} won {} chips and now has {} in total.".format(player["id"], self.validateBet(self.dealer_return(self.dealer_chips_amount, bet)), new_chips))

                    self.dealer_chips_amount -= self.validateBet(self.dealer_return(self.dealer_chips_amount, bet))

                    temp_players.append(pydash.assign(
                        {},
                        player,
                        {
                            "chips": new_chips
                        }
                    ))
                elif outcome[player["id"]] is self.OUTCOMES["LOSS"]:
                    self.stats[player["id"]]["dealer_wins"] += 1

                    new_chips = player["chips"] - bet

                    self.dealer_chips_amount += bet

                    print("    🃏  Player {} lost {} chips and now has {} in total.".format(player["id"], bet, new_chips))

                    if new_chips > 0:
                        temp_players.append(pydash.assign(
                            {},
                            player,
                            {
                                "chips": new_chips
                            }
                        ))
                    else:
                        self.goodbye(player["id"], False)

        for player in self.players:
            if self.dealer_id is player["id"]:
                new_dealer_chips = self.validateBet(self.dealer_chips_amount)

                if new_dealer_chips > 0:
                    temp_players.append(pydash.assign(
                        {},
                        player,
                        {
                            "chips": new_dealer_chips
                        }
                    ))
                else:
                    need_new_dealer = True

                    self.goodbye(player["id"], True)

        if self.dealer_chips_amount > 0:
            self.dealer_winnings(self.dealer_chips_amount)

        self.players = temp_players

        if need_new_dealer:
            self.chooseDealer()

    def dealer_return(self, dealer_chips_amount, bet_amount):
        bet_amount = bet_amount

        if bet_amount <= dealer_chips_amount:
            bet_amount = bet_amount
        else:
            bet_amount = dealer_chips_amount

        return bet_amount

    def dealer_chips(self):
        for player in self.players:
            if player["id"] is self.dealer_id:
                return player["chips"]

    def game_header(self, game_number):
        print(
            """
# ============================================================================================ #
                                        Game {}
# ============================================================================================ #
            """.format(game_number + 1)
        )

    def queen_of_hearts(self):
        print(
            """
                                                            .
                                  .       |         .    .
                            .  *         -*-          *
                                 \        |         /   .
                .    .            .      /^\     .              .    .
                   *    |\   /\    /\  / / \ \  /\    /\   /|    *
                 .   .  |  \ \/ /\ \ / /     \ \ / /\ \/ /  | .     .
                         \ | _ _\/_ _ \_\_ _ /_/_ _\/_ _ \_/
                           \  *  *  *   \ \/ /  *  *  *  /
                            ' ~ ~ ~ ~ ~  ~\/~ ~ ~ ~ ~ ~ '

                              The Queen of Hearts came!


                                Rebuilding the deck...

                              _____
                             |A .  | _____
                             | /.\ ||A ^  | _____
                             |(_._)|| / \ ||A _  | _____
                             |  |  || \ / || ( ) ||A_ _ |
                             |____V||  .  ||(_'_)||( v )|
                                    |____V||  |  || \ / |
                                           |____V||  .  |
                                                  |____V|

            """
        )

    def title(self):
        print("""

                                       _____
           _____                _____ |6    |
          |2    | _____        |5    || o o |
          |  o  ||3    | _____ | o o || o o | _____
          |     || o o ||4    ||  o  || o o ||7    |
          |  o  ||     || o o || o o ||____9|| o o | _____
          |____Z||  o  ||     ||____S|       |o o o||8    | _____
                 |____E|| o o |              | o o ||o o o||9    |
                        |____h|              |____L|| o o ||o o o|
                                    _____           |o o o||o o o|
                            _____  |K  WW|          |____8||o o o|
                    _____  |Q  ww| | /\\{)|                 |____6|
             _____ |J  ww| | /\\{(| | \\/%%| _____
            |10 o || /\\{)| | \\/%%| |  %%%||A ^  |
            |o o o|| \\/% | |  %%%| |_%%%>|| / \\ |
            |o o o||   % | |_%%%O|        | \\ / |
            |o o o||__%%[|                |  .  |
            |___0I|                       |____V|


                    Welcome to Sette e Mezzo in Python!

        """)

    def broken(self, player_id):
        print("""

         ____________________
        /                    \\
        |     Player {}       |
        |     has broken!     |
        \\____________________/
                 !  !
                 !  !
                 L_ !
                / _)!
               / /__L
         _____/ (____)
                (____)
         _____  (____)
              \\_(____)
                 !  !
                 !  !
                 \\__/

        """.format(player_id))

    def leaderboard(self):
        print(
            """
# ============================================================================================ #
                                        LEADERBOARD

                                  THE WINNER is PLAYER {}

                                      WITH {} CHIPS
# ============================================================================================ #
            """.format(self.players[0]["id"], self.players[0]["chips"])
        )

    def goodbye(self, player_id, is_dealer):
        if is_dealer:
            print("""
                            ,     \\    /      ,
               / \\    )\\__/(     / \\
              /   \\  (_\\  /_)   /   \\
         ____/_____\\__\\@  @/___/_____\\____
        |             |\\../|              |
        |              \\VV/               |
        |       The Dealer has fallen     |
        |_________________________________|
         |    /\\ /      \\\\       \\ /\\    |
         |  /   V        ))       V   \\  |
         |/     `       //        '     \\|
         `              V                '
            """)
        else:
            print("""
                       ,  ,
                       \\\\ \\\\
                       ) \\\\ \\\\    _p_
                       )^\\))\\))  /  *\\
                        \\_|| || / /^`-'
               __       -\\ \\\\--/ /
             <'  \\\\___/   ___. )'
                  `====\\ )___/\\\\
                       //     `"
                       \\\\    /  \\
                       `" +==============+
                          |  Player      |
                          |  {}           |
                          |  has been    |
                          |  disqualied  |
                          +==============+
            """.format(player_id))

    def dealer_winnings(self, chips):
        print(
            """

                               .------.
                              (        )
                              |~------~|
                              |        | .----.
                              |         (      )
                              |        ||~----~|
                              |        ||      |
                              |        ||  .-----.
                              |        || |._____.'
                              |        || |       |
                              |   .------.|       |
                              |  (        |       |
                              |  |~------~|       |
                              |  |        |       |
               _..----------..|  |  _.-----._     |
            .-~                ~-..-         -.   |
            |.                  .||-_       _-|   |
            |"-..____________..-"||  ~-----~  |   |
            |                   .`|           |--"
             "-..____________..-" `._       _.'
                                     "-----"

                    💰  The dealer now has {} chips

            """.format(chips)
        )

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
        self.chooseDealer()

        for game in range(games + 1):
            if len(self.players) > 1:
                self.game_header(game)

                if not self.QHStillInPlay():
                    self.queen_of_hearts()
                    self.rebuild()

                self.handOutCards()
                self.round()

                input("ROUND COMPLETE")

    def run(self, games):
        self.title()
        self.getPlayers(self.number_of_players)
        self.play(games)
        self.leaderboard()

sette = Sette()
sette.run(10000)
