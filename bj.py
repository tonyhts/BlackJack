# coding: utf-8

import random
import re
import urllib.request
from os import system


class Player(object):
    def __init__(self, bot = False):
        self.pot = 10
        self.score = 0
        self.bet = 1
        self.more = True
        self.hand = []
        self.restart = False
        self.bot = bot
        self.name = ''
        self.get_name()

    def get_name(self):
        if self.bot:
            print('Buscando um Robo que seja um oponente a sua altura...')
            self.name = self.bot_names()
            print('\t %s na área !!' % (self.name))
        else:
            self.name = input('Qual o seu nome? ').capitalize()

    def __repr__(self):
        return str(self.name)

    def bot_names(self):

        '''Metodo fanfarrão que pesquisa nomes de robos na wikipedia #SempreAtualizado.rsrsrsr '''

        robolandia = 'https://en.wikipedia.org/wiki/List_of_fictional_robots_and_androids'
        u = urllib.request.urlopen(robolandia)
        result = u.readlines()
        nbolds = re.findall(r'<b>\w*</b>', str(result))
        bots = []
        for i in nbolds:
            bots.append(re.sub(r'<b>|</b>', '', i))

        return random.choice(bots)
    #TODO: implentar direito essa joça, exibir o caixa na tela e tals
    def get_bet(self):
        bet = ''
        while type(bet) is not int:
            try:
                bet = int(input('quanto quer apostar? '))
                if bet is None:
                    print('Digite um valor valido (apenas numeros !!)\nQuanto quer apostar? ')
                else:
                    self.bet += bet
                    self.pot -= bet

            except TypeError:
                print('Tenso!!!!!!!!!!\n\t Somente numeros, plz!')

    def sum_score(self):
        score = 0
        for value in self.hand:
            if type(value) is str and value is not 'A':
                value = 10
            if value == 'A' and self.score + 11 <= 21:
                value = 11
            elif value == 'A' and self.score + 11 > 21:
                value = 1

            score += value
        self.score = score

        return self.score

    def more_card(self):
        self.sum_score()
        if self.more:
            r = input('vc esta com %d , deseja mais cartas? S ou N \n'  % (self.score)).lower()
            if r.startswith('s'):
                self.hand.append(Deck().pick_card())
            else:
                print('OK, Vamos ver se o Bot tem melhores cartas que vc!')
                p1.more = False


class Deck(object):

    def __init__(self):
        self.naipes = 'paus copas espadas ouro'.split()
        self.cartas = 'A J Q k'.split() + [x for x in range(2, 11)]
        self.deck = [(c, n) for n in self.naipes for c in self.cartas]
        #baralho já começa embaralhado
        self.shuffle()

    def __len__(self):
        return len(self.deck)

    def __repr__(self):
        print(self.deck)

    def pick_card(self):
        if len(self.deck) >= 1:
            card = self.deck.pop(random.randint(0, len(self.deck) - 1))
        else:
            print('Deck Vazio')
            card = None

        return card[0]

    def shuffle(self):
        random.shuffle(self.deck)


class Game(object):
    def __init__(self):
        self.runing = True
        self.total_pot = 0
        self.turn = ('p1')
        self.win = False
        self.players = []

    def addPlayer(self,player):
        if type(player) is Player:
            self.players.append(player)
        else:
            print('Jogador inválido')

    def check_win(self):
        self.win = False
        if p1.score == 21 or Bot.score > 21:
            self.win = True
            self.cls()
            print('\033[31m' + "\n\n\t\t VC GANHOU !!!" + '\033[0;0m')
            p1.pot += self.total_pot
            self.restart()
        elif Bot.score == 21 or p1.score > 21:
            self.cls()
            print('\033[31m' + " \n\n\t\tO BOT Ganhou!!!\n\n vc perdeu $ %d " % (self.total_pot / 2) + '\033[0;0m')
            Bot.pot += self.total_pot
            self.restart()
        if not self.is_runing():
            if abs(p1.score - 21) < abs(Bot.score - 21):
                self.win = True
                self.cls()
                print('\033[31m' + "\n\n\t\t VC GANHOU !!!" + '\033[0;0m')
                p1.pot += self.total_pot
                self.restart()
            elif p1.score == Bot.score:
                self.cls()
                print('\033[31m' + '\n\n\t Caraca! EMPATOU!!!!\n\n' + '\033[0;0m')
                self.restart()
            else:
                self.cls()
                print('\033[31m' + " \n\n\t\tO BOT Ganhou!!!\n\n vc perdeu $ %d " % (self.total_pot / 2) + '\033[0;0m')
                Bot.pot += self.total_pot
                self.restart()

    def restart(self):
        print('\n\n\tNova Rodada!\n\n')
        self.runing = True
        game.run()

    def cls(self):
        system("clear")

    def run(self):
        print('\n\nSEU SCORE: %d\t BOT SCORE: %d\n\n' % (p1.score,Bot.score))
        #TODO: tirar essa gambzinha de init pro restart.
        p1.more = True
        Bot.more = True
        p1.hand, p1.score = [], 0
        Bot.hand, Bot.score = [], 0
        b = Deck()
        p1.hand.append(b.pick_card())
        Bot.hand.append(b.pick_card())
        if random.randint(0,1) == 0:
            self.turn = 'p1'
        else:
            self.turn = 'Bot'

        while self.is_runing():
            if self.turn == 'p1':
                print('Vamos la %s,  até agora vc tem %d cartas. Totalizando %d pontos. São elas: %s' % (p1.name, len(p1.hand), p1.sum_score(), p1.hand))
                self.total_pot += 1
                p1.more_card()
                p1.sum_score()
                self.check_win()
                self.turn = 'Bot'
            else:
                print('Agora e a vez do PC..')
                if Bot.score < 15:

                    Bot.bet += self.total_pot / 2
                    Bot.pot -= Bot.bet
                    Bot.hand.append(b.pick_card())
                    Bot.sum_score()
                    self.check_win()
                    self.turn = 'p1'
                    self.is_runing()
                else:
                    Bot.more = False
                    self.turn = 'p1'
                    self.check_win()
                    self.is_runing()

    def is_runing(self):
        if not p1.more and not Bot.more:
            self.runing = False
        return self.runing

Game().cls()
print('\n\tBem vindo ao BlackJack!\n')

p1 = Player()
Bot = Player(True)
game = Game()
game.addPlayer(p1)
game.addPlayer(Bot)
game.run()