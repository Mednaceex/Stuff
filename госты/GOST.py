class Better:
    def __init__(self, name: str, goals_=0):
        self.name = name
        self.goals = goals_
        self.flags = []

    def find(self, name):
        return True if self.name == name or name in self.flags else False

    def get_flags(self, flags_: list):
        for j in flags_:
            self.flags.append(j)

    def set_goals(self, value):
        self.goals = value


def check_bet(bet1, bet2, score1, score2):
    if score[i] == bets[i]:
        return 2
    elif (bet1 < bet2) and (score1 < score2):
        return 1
    elif (bet1 > bet2) and (score1 > score2):
        return 1
    elif (bet1 == bet2) and (score1 == score2):
        return 1
    else:
        return 0


def split(string: str, sep: str):
    array_ = string.split(sep)
    for j in range(len(array_)):
        array_[j] = array_[j].replace('\n', '')
    return array_


def print_name_error(text: str, file):
    print('Undefined name:', text, file=file)
    print('Undefined name:', text)


n = 10
betters = []
score = [''] * 10
scores = []
none = ('xx', 'хх', '__', '--', '_', '//', '/')

with open('flags.txt', 'r') as flags:
    c = flags.readlines()
    for line in c:
        a = split(line, ' - ')
        flag_array = split(a[1], ', ')
        b = Better(a[0])
        b.get_flags(flag_array)
        betters.append(b)

with open('output.txt', 'w+') as output:
    with open('inputs.txt', 'r') as bets:
        c = bets.readlines()
        for line in range(len(c)):
            array = split(c[line], ' ')
            if line == 0:
                for i in range(0, n, 1):
                    score[i] = array[i]
            else:
                goals = 0
                team = array[0]
                bets = [''] * 10
                for i in range(1, n+1, 1):
                    if array[i] in none:
                        bets[i-1] = 'None'
                    else:
                        bets[i-1] = array[i]

                for i in range(len(bets)):
                    if bets[i] != 'None':
                        goals += check_bet(int(bets[i][0]), int(bets[i][1]), int(score[i][0]), int(score[i][1]))
                scores.append(team + ' ' + str(goals))
                for i in betters:
                    if i.find(team):
                        i.set_goals(goals)

    with open('matches.txt', 'r') as matches:
        c = matches.readlines()
        for line in c:
            array = split(line, ' - ')
            (g1, g2) = (0, 0)
            (name1, name2) = ('', '')
            for i in betters:
                if i.find(array[0]):
                    g1 = i.goals
                    name1 = i.name
                if i.find(array[1]):
                    g2 = i.goals
                    name2 = i.name
            if name1 == '':
                print_name_error(array[0], output)
            elif name2 == '':
                print_name_error(array[1], output)
            else:
                print(name1, str(g1) + '-' + str(g2), name2, file=output)
