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
        self.playing = True
        self.hand = []
        self.restart = False
        self.bot = bot
        self.name = ''
        self.get_name()

    def get_name(self):
        if self.bot:
            print('Buscando um Robo que seja um oponente a sua altura...')
            self.name = str(self.bot_names())
            print('\t %s na área !!' % (self.name))
        else:
            self.name = str(input('Qual o seu nome? ').capitalize())

    def __repr__(self):
        return self.name

    def isHuman(self):
        return not self.bot

    def bot_names(self):
        '''
        Metodo fanfarrão que pesquisa nomes de robos na wikipedia #SempreAtualizado.rsrsrsr
        '''
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
        for card in self.hand:
            value = card[0]
            if type(value) is str and value is not 'A':
                value = 10
            if value == 'A' and self.score + 11 <= 21:
                value = 11
            elif value == 'A' and self.score + 11 > 21:
                value = 1

            score += value
        self.score = score

        return self.score

    def play(self, deck):
        while self.playing:
            r = input('vc esta com %d pontos, deseja mais cartas? S ou N \n'  % (self.score)).lower()
            if r.startswith('s'):
                self.get_card(deck.pick_card())
            else:
                print('OK, Vamos ver se vc tem as melhores cartas!')
                self.playing = False

    def reset(self):
        self.more = True
        self.hand = []
        self.score = 0

    def get_card(self,card):
        self.hand.append(card)
        self.sum_score()

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
        return self.deck

    def pick_card(self, pos = 0):
        if len(self.deck) >= 1:
            card = self.deck.pop(pos)
        else:
            # print('Deck Vazio') prints devem ocorrer somente no jogo
            card = None

        '''
        Retornar a carta para manter modularidade. As cartas são tuplas e devem permancecer assim, seja no deck ou na mão.
        A classe Deck pode ser usada em qualquer jogo (modularidade)
        '''
        return card

    def pick_random_card(self):
        rand = random.randint(len(self.deck) - 1)
        return self.pick_card(rand)

    def shuffle(self):
        random.shuffle(self.deck)


class Game(object):
    def __init__(self):
        self.runing = True
        self.total_pot = 0
        #self.turn = ('p1')
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

    def msg(self,msg = ''):
        print('\n%s\n' % msg)

    def order_players(self):
        random.shuffle(self.players)

    def run(self):
        self.msg('Bem vindo ao BlackJack!')
        #self.msg('SEU SCORE: %d\t BOT SCORE: %d' % (p1.score,Bot.score))
        self.order_players()
        players_names = ', '.join(str(p) for p in self.players)
        msg = 'Ordem dos jogadores: %s' % players_names
        self.msg(msg)

        b = Deck()
        for p in self.players:
            p.reset()
            p.get_card(b.pick_card())

        while self.is_runing():
            for p in self.players:
                if p.isHuman():
                    msg = 'Vamos la %s,  até agora vc tem %d cartas. Totalizando %d pontos. São elas: %s' % (p.name, len(p.hand), p.sum_score(), p.hand)
                    self.msg(msg)
                    self.total_pot += 1
                    p.play(b)
                else:
                    self.msg('Agora e a vez do %s...' % p.name)
                    if p.score < 15:
                        p.bet += self.total_pot / 2
                        p.pot -= p.bet
                        p.get_card(b.pick_card())
                        p.sum_score()
                    else:
                        p.more = False
            self.check_win()

    def is_runing(self):
        if not p1.more and not Bot.more:
            self.runing = False
        return self.runing

p1 = Player()
bot = Player(True)

game = Game()
game.addPlayer(p1)
game.addPlayer(bot)
game.run()