import random


class Player(object):
    def __init__(self):
        self.name = ''
        self.pot = 10
        self.score = 0
        self.bet = 1
        self.more = True
        self.hand = []
        self.restart = False

    def get_name(self):
        self.name = input('Qual o seu nome? ').capitalize()

    def get_bet(self):
        _bet = 'a'
        while type(_bet) == str or _bet is None:
            try:
                _bet = int(input('quanto quer apostar? '))
                while self.bet is None:
                    _bet = int(input('Digite um valor valido (apenas numeros !!\nQuanto quer apostar? '))
                    self.bet += _bet
                self.pot -= _bet
                self.bet = _bet
            except TypeError:
                print('Tenso!!!!!!!!!!\n\t Somente numeros, plz!')

    def sum_score(self):
        aces = 0
        ace = 0
        _score = 0
        for valor in self.hand:
            _score += valor
        self.score = _score

        for x in self.hand:
            if x == 'A':
                ace += 10
                aces += 1

        if aces > 0 and ((self.score) + ace) <= 21:
            self.score = ((self.score) + ace)

        return self.score

    def more_card(self):
        if self.more:
            r = input('vc esta com %d , deseja mais cartas? S ou N \n'  % (self.score)).lower()
            if r.startswith('s'):
                self.hand.append(Baralho().pick_card())
            else:
                print('OK, Vamos ver se o Bot tem melhores cartas que vc!')
                self.more = False


class Baralho(object):

    def __init__(self):
        self.naipes = 'paus copas espadas ouro'.split()
        self.cartas = 'A J Q k'.split() + [x for x in range(2, 11)]
        self.deck = [(c, n) for n in self.naipes for c in self.cartas]

    def __len__(self):
        return len(self.deck)

    def __repr__(self):
        print(self.deck)

    def pick_card(self):
        if len(self.deck) >= 1:
            self.carta = self.deck.pop(random.randint(0, len(self.deck) - 1))
            if type(self.carta[0]) == str:
                self.valor = 10
            else:
                self.valor = self.carta[0]
        else:
            print('Deck Vazio')
            self.valor = 0
            self.carta = 'Nehuma'
        return self.valor

    def dist_cards(self):
        p1.hand = self.pick_card()
        Bot.hand = self.pick_card()

    def embaralhar(self):
        random.shuffle(self.deck)


class Jogo(object):
    def __init__(self):
        self.runing = True
        self.total_pot = 0
        self.turn = ('p1')
        self.win = False

    def check_win(self):

        self.win = False
        if p1.score == 21 or (p1.score - 21) < (Bot.score - 21):
            self.win = True
            print(" VC GANHOU !!!")
            p1.pot += self.total_pot
            exit()
        elif Bot.score == 21 or (Bot.score - 21) < (p1.score - 21):
            print(" O BOT Ganhou!!!\n\n vc perdeu %d " % (self.total_pot / 2))
            Bot.pot += self.total_pot

    def restart(self):
        if p1.restart is True:
            self.runing = False
            Bot.win = True
            self.check_win()

    def run(self):

        print('\n\tBem vindo ao BlackJack!\n')

        b = Baralho()
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
        if not p1.more and not Bot.more:
            self.runing = False
        return self.runing


p1 = Player()
p1.get_name()
Bot = Player()
p1.hand.append(Baralho().pick_card())
Bot.hand.append(Baralho().pick_card())

Jogo().run()
