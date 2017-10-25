import random


class Player(object):
    def __init__(self, bot=False):
        self.pot = 10
        self.score = 0
        self.bet = 1
        self.more = True
        self.hand = []
        self.restart = False
        self.bot = bot
        self.get_name()

    def get_name(self):
        if self.bot:
            # TODO: pensar em algum sistema de nomes aleatórios e tal
            self.name = 'Superbot2017'
        else:
            self.name = input('Qual o seu nome? ').capitalize()

    def get_bet(self):
        bet = 'a'
        while type(bet) == str or bet is None:
            try:
                bet = int(input('quanto quer apostar? '))
                while self.bet is None:
                    bet = int(input('Digite um valor valido (apenas numeros !!)\nQuanto quer apostar? '))
                    self.bet += bet
                self.pot -= bet
                self.bet = bet
            except TypeError:
                print('Tenso!!!!!!!!!!\n\t Somente numeros, plz!')

    def sum_score(self):
        aces = 0
        ace = 0
        score = 0
        for value in self.hand:
            score += value
        self.score = score

        for card in self.hand:
            if card == 'A':
                ace += 10
                aces += 1

        if aces > 0 and self.score + ace <= 21:
            self.score = self.score + ace

        return self.score

    def more_card(self):
        if self.more:
            r = input('vc esta com %d , deseja mais cartas? S ou N \n'  % (self.score)).lower()
            if r.startswith('s'):
                self.hand.append(Deck().pick_card())
            else:
                print('OK, Vamos ver se o Bot tem melhores cartas que vc!')
                self.more = False


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
        #pick_card() retorna a carta
        return card

    '''
    Este método deve ser do Jogo e não do baralho!
    def dist_cards(self):
        p1.hand = self.pick_card()
        Bot.hand = self.pick_card()
    '''

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
        if p1.score == 21 or (p1.score - 21) < (bot.score - 21):
            self.win = True
            print(" VC GANHOU !!!")
            p1.pot += self.total_pot
            exit()
        elif bot.score == 21 or (bot.score - 21) < (p1.score - 21):
            print(" O BOT Ganhou!!!\n\n vc perdeu %d " % (self.total_pot / 2))
            bot.pot += self.total_pot

    def restart(self):
        if p1.restart is True:
            self.runing = False
            bot.win = True
            self.check_win()

    def run(self):

        print('\n\tBem vindo ao BlackJack!\n')

        b = Deck()
        p1 = Player()
        p1.get_name()
        Bot = Player()
        Bot.name = 'ibot'
        p1.hand.append(b.pick_card())
        Bot.hand.append(b.pick_card())

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
                if Bot.score > 15:

                    Bot.bet += self.total_pot / 2
                    Bot.pot -= Bot.bet
                    Bot.hand.append(b.pick_card())
                    Bot.sum_score()
                    self.check_win()
                    self.turn = 'p1'
                    self.is_runing()

                else:
                    Bot.more = False
                    self.is_runing()

    def is_runing(self):
        if not p1.more and not bot.more:
            self.runing = False
        return self.runing


p1 = Player()
bot = Player(True)

game = Game()
game.addPlayer(p1)
game.addPlayer(bot)
game.run()