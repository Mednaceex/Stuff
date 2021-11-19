from PyQt5 import QtWidgets
from modules.window import Ui_MainWindow
import sys

none = ('xx', 'хх', 'ХХ', 'XX', '__', '--', '_', '//', '/')
n = 10
player_count = 20


class Better:
    def __init__(self, name: str, flags=None, goals=0):
        """
        Конструктор класса игроков

        :param name: название команды игрока
        :param flags: список флагов (сокращённых названий команды)
        :param goals: количество голов, забитых игроком
        """
        self.name = name
        self.goals = goals
        if flags is None:
            self.flags = []
        else:
            self.flags = flags

    def find(self, name):
        """
        Определяет, соответствует ли строка name названию команды игрока или одному из её флагов (сокращённых названиц)
        """
        return True if self.name == name or name in self.flags else False

    def set_goals(self, value):
        """
        Изменяет количество голов игрока на заданное параметром value
        """
        self.goals = value


def check_bet(bet1, bet2, score1, score2):
    """
    Определяет и возвращает количество голов, забитых на конкретной ставке

    :param bet1: инд. тотал 1 команды в ставке
    :param bet2: инд. тотал 2 команды в ставке
    :param score1: реальный инд. тотал 1 команды
    :param score2: реальный инд. тотал 2 команды
    """
    if (bet1 == score1) and (bet2 == score2):
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
    """
    Разделяет строку на список по данной разделительной строке, удаляет символы перехода на новую строку

    :param string: строка, которую необходимо разделить
    :param sep: разделительная строка
    :return: список строк
    """
    array = string.split(sep)
    for j, elem in enumerate(array):
        array[j] = elem.replace('\n', '')
    return array


def get_flags(file):
    """
    Считывает названия и флаги команд из файла, создаёт список объектов класса Better с этими данными

    :param file: путь к файлу
    :return: список объектов класса Better
    """
    array = []
    text = file.readlines()
    for line in text:
        a = split(line, ' - ')
        flag_array = split(a[1], ', ')
        b = Better(a[0], flag_array)
        array.append(b)
    return array


def get_names(betters_array):
    array = []
    for better in betters_array:
        array.append(better.name)
    return array

def get_scores(line):
    """
    Создаёт и возвращает список счетов матчей из данной строки
    (в строке счета матчей должны быть представлены двузначными числами, разделёнными пробелом)
    """
    score_list = split(line, ' ')
    scores = ['None'] * n
    for i, elem in enumerate(score_list):
        if elem not in none:
            scores[i] = elem
    return scores


def get_goals(bets_list, scores_list, betters_list):
    """
    Рассчитывает количество забитых игроком голов

    :param bets_list: список ставок игрока
    :param scores_list: список счетов матчей
    :param betters_list: список игроков (объектов класса Better)
    """
    goals = 0
    team = bets_list[0]
    bets = ['None'] * n
    for i in range(len(bets_list) - 1):
        if bets_list[i + 1] in none:
            bets[i] = 'None'
        else:
            bets[i] = bets_list[i + 1]
    for i, bet in enumerate(bets):
        if bet != 'None' and scores_list[i] != 'None':
            goals += check_bet(int(bet[0]), int(bet[1]), int(scores_list[i][0]), int(scores_list[i][1]))
    for i in betters_list:
        if i.find(team):
            i.set_goals(goals)


def get_matches(line, output_file, betters_list):
    """
    Считывает матч из строки расписания и выводит его счёт в файл вывода

    :param line: строка с матчем из расписания
    :param output_file: путь к файлу вывода
    :param betters_list: список игроков (объектов класса Better)
    """
    array = split(line, ' - ')
    g = [0] * 2
    name = [''] * 2
    for i in betters_list:
        for k in range(2):
            if i.find(array[k]):
                g[k] = i.goals
                name[k] = i.name
    for k in range(2):
        if name[k] == '':
            print_name_error(array[k], output_file)
    else:
        print(name[0], f'{g[0]}-{g[1]}', name[1], file=output_file)


def print_name_error(text: str, file):
    """
    Выводит сообщение об ошибке в имени в файл и в консоль

    :param text: имя (строка)
    :param file: путь к файлу вывода
    """
    print('Undefined name:', text, file=file)
    print('Undefined name:', text)


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.Left_Button.clicked.connect(self.proceed)
        self.ui.Right_Button.clicked.connect(self.deny)

    def proceed(self):
        text = self.ui.Text_1.toPlainText()
        print(text)

    def deny(self):
        print("Член мошонка муравей я жевал говно гусей")

    def set_names(self, name_array):
        for i, elem in enumerate(name_array):
            exec(f'self.ui.Name_{i + 1}.setText(elem)')


def main():
    with open('flags.txt', 'r') as flags:
        betters = get_flags(flags)

    with open('output.txt', 'w+') as output:
        with open('bets.txt', 'r') as bets:
            text = bets.readlines()
            for j, line in enumerate(text):
                if j == 0:
                    score = get_scores(line)
                else:
                    input_array = split(line, ' ')
                    get_goals(input_array, score, betters)
        with open('matches.txt', 'r') as matches:
            text = matches.readlines()
            for line in text:
                get_matches(line, output, betters)

    app = QtWidgets.QApplication([])
    application = Window()
    names = get_names(betters)
    application.set_names(names)
    application.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    main()
