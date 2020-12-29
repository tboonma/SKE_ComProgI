from card_deck import *
from player import *
from player_list import *

class Blackjack:
    '''This class describes the game of Blackjack itself 
    '''

    def __init__(self):
        deck = CardDeck()
        deck.shuffle()
        self.bj_deck = deck
        self.player = []
        self.computer_hand = []
        self.computer_hand_value = []  # can have multiple values when hand involves Aces
        self.computer_hand_status = ''  # [stay or dead or can_stay or must_draw_more]
        self.computer_score = 0
        self.central_money = 0

    def add_player(self, name, budget):
        self.player.append(Player(name, budget))

    def start(self):
        '''This method starts the game by drawing from the card deck 
        (represented by self.bj_deck) two cards for player and two cards 
        for computer; then it proceed to update all the values and statuses for both hands
        >>> b = Blackjack()
        >>> b.start()
        <BLANKLINE>
        '''
        print()
        for i in range(2):
            for j in range(len(self.player)):
                self.adjust_player_hand(j)
            self.adjust_computer_hand()
        for i in range(len(self.player)):
            self.central_money += 100
            self.player[j].pay(100)
        self.central_money += 100

    def adjust_player_hand(self, index):
        '''This method draws an additional card and reevalute the value and status 
        of the player hand
        '''
        card_draw = self.bj_deck.draw_cards(1)
        self.player[index].adjust_hand(card_draw)

    def check_all_player_value(self):
        self.__all_value = []
        for player in self.player:
            value = sum(player.value)
            if value > 21:
                value = 0
            self.__all_value.append(value)
        return self.__all_value

    def adjust_computer_hand(self):
        '''This method draws an additional card and reevalute the value and status of the
        computer hand
        '''
        card_draw = self.bj_deck.draw_cards(1)
        self.computer_hand += card_draw
        if card_draw[0][0] == 'J' or card_draw[0][0] == 'Q' or card_draw[0][0] == 'K' or card_draw[0][0] == '1':
            self.computer_hand_value.append(10)
        elif card_draw[0][0] != 'A':
            self.computer_hand_value.append(int(card_draw[0][0]))
        else:
            if sum(self.computer_hand_value) <= 10:
                self.computer_hand_value.append(11)
            else:
                self.computer_hand_value.append(1)
        if sum(self.computer_hand_value) > 21 and 11 in self.computer_hand_value:
            self.computer_hand_value.remove(11)
            self.computer_hand_value.append(1)
        if sum(self.computer_hand_value) < 16:
            self.computer_hand_status = 'must_draw_more'
        elif sum(self.computer_hand_value) < 21:
            self.computer_hand_status = 'can_stay'
        elif sum(self.computer_hand_value) == 21:
            self.computer_hand_status = 'stay'
        else:
            self.computer_hand_status = 'dead'

    def display_player_hand(self, index):
        '''This method reveals the player hand'''
        player = self.player[index]
        SUITS_sym = ["\u2663", "\u2666", "\u2660", "\u2665"]
        print(f"{player.name} hand", end=": ")
        for card in player.hand:
            print(f'{card[0]}', end='')
            if card[0] == '1':
                print(f'{card[1]}', end='')
            if 'Clubs' in card:
                print(f'{SUITS_sym[0]}', end=' ')
            elif 'Diamonds' in card:
                print(f'{SUITS_sym[1]}', end=' ')
            elif 'Spades' in card:
                print(f'{SUITS_sym[2]}', end=' ')
            elif 'Hearts' in card:
                print(f'{SUITS_sym[3]}', end=' ')
        print()

    def display_computer_hand(self):
        '''This method reveals the computer hand '''
        SUITS_sym = ["\u2663", "\u2666", "\u2660", "\u2665"]
        print("Computer hand:", end=" ")
        index = len(self.player) - 1
        for card in self.computer_hand:
            print(f'{card[0]}', end='')
            if card[0] == '1':
                print(f'{card[1]}', end='')
            if 'Clubs' in card:
                print(f'{SUITS_sym[0]}', end=' ')
            elif 'Diamonds' in card:
                print(f'{SUITS_sym[1]}', end=' ')
            elif 'Spades' in card:
                print(f'{SUITS_sym[2]}', end=' ')
            elif 'Hearts' in card:
                print(f'{SUITS_sym[3]}', end=' ')
            if self.player[index].status == 'must_draw_more' or self.player[index].status == 'can_stay':
                break
        print()

    def decision(self, all_players):
        '''This method makes a decision if the player wins, looses, or ties with the
        computer 
        '''
        print()
        computer_win = False
        all_winner = []
        com_value = sum(self.computer_hand_value)
        if com_value > 21:
            com_value = 0
        for player in self.player:
            sum_value = sum(player.value)
            if sum_value > 21:
                sum_value = 0
            if sum_value > com_value:
                print(f"{player.name} wins")
                player.update_score(1)
                self.computer_score -= 1
                self.update_win_lose(player.name, 'win', all_players)
                all_winner.append(player.name)
            elif sum_value < com_value:
                print(f"{player.name} looses")
                player.update_score(-1)
                self.computer_score += 1
                self.update_win_lose(player.name, 'lose', all_players)
                computer_win = True
            else:
                print(f"{player.name} ties")
        print()
        for player in self.player:
            print(f"{player.name} scores {player.score}")
        print(f"Computer scores {self.computer_score}")
        self.update_winner_money(all_winner, all_players, computer_win)

    def update_win_lose(self, name, result, all_players):
        for player in all_players:
            if player.name == name:
                if result == 'win':
                    player.add_one_win()
                else:
                    player.add_one_lose()
                break
    
    def update_winner_money(self, all_winner, all_players, computer_win):
        split = len(all_winner)
        if computer_win:
            split += 1
        amount = self.central_money/split
        if len(all_winner) == 0 and computer_win == False:
            for player in self.player:
                for p in all_players:
                    if player.name == p.name:
                        p.budget += 100
                        player.add_budget(100)
                        break
        for winner in all_winner:
            for player in all_players:
                if player.name == winner:
                    player.budget += amount
                    break
        for player in self.player:
            if player.name in all_winner:
                player.add_budget(amount)
        self.central_money = 0

    def clear(self):
        for p in self.player:
            p.hand = []
            p.value = []
            p.status = ''
        self.computer_hand = []
        self.computer_hand_value = []  # can have multiple values when hand involves Aces
        self.computer_hand_status = ''  # [stay or dead or can_stay or must_draw_more]

if __name__ == "__main__":
    import doctest
    doctest.testmod()
