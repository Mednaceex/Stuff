from PyQt5 import QtWidgets
from modules.window import Ui_MainWindow
import sys

none = ('xx', 'хх', 'ХХ', 'XX', '__', '--', '_', '//', '/', 'None')
n = 10
player_count = 20
seps = (':', '-', '—')
numbers = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '0')


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


def get_goals(name, bets_list, scores_list, betters_list):
    """
    Рассчитывает количество забитых игроком голов

    :param name: название команды
    :param bets_list: список ставок игрока
    :param scores_list: список счетов матчей
    :param betters_list: список игроков (объектов класса Better)
    """
    goals = 0
    bets = ['None'] * n
    for i, bet in enumerate(bets_list):
        if bet in none:
            bets[i] = 'None'
        else:
            bets[i] = bet
    for i, bet in enumerate(bets):
        if bet != 'None' and scores_list[i] != 'None':
            goals += check_bet(int(bet[0]), int(bet[1]), int(scores_list[i][0]), int(scores_list[i][1]))
    for i in betters_list:
        if i.find(name):
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


def find_bet(text: str):
    """
    Ищет ставки игрока в тексте госта, возвращает массив с ними
    Каждый элемент возвращаемого массива - список из 2 чисел - ставок на 1 и 2 команды)
    """
    array = []
    for i, character in enumerate(text):
        if character in seps and 0 < i < len(text)-1:
            if text[i-1] in numbers and text[i+1] in numbers:
                (bet1, bet2) = ('', '')
                (left, right) = (1, 1)
                while i - left > 1 and text[i - left - 1] in numbers:
                    left += 1
                while i + right < len(text) - 2 and text[i + right + 1] in numbers:
                    right += 1
                for j in range(left):
                    bet1 += text[i - left + j]
                for j in range(right):
                    bet2 += text[i + j + 1]
                array.append([int(bet1), int(bet2)])
    return array


def config_bets_array(text: str, missing: list):
    """
    Считывает ставки из текста госта, присланного игроком

    :param text: текст госта
    :param missing: массив из n элементов - True (ставка отсутствует) или False (ставка есть)
    :return: None в случае ошибки в госте, иначе массив ставок игрока
    """
    bets_array = find_bet(text)
    array = []
    error = False
    length = len(bets_array)
    if n <= length:
        for i in range(n):
            array.append(bets_array[i])
        for i, missing_match in enumerate(missing):
            if missing_match:
                array[i] = 'None'
    else:
        k = 0
        for i, missing_match in enumerate(missing):
            if missing_match:
                array.append('None')
            else:
                if k >= length:
                    error = True
                    break
                else:
                    array.append(bets_array[k])
                    k += 1
    if error:
        return None
    else:
        return array


def get_missing(name):
    return [False] * 10


def print_name_error(text: str, file):
    """
    Выводит сообщение об ошибке в имени в файл и в консоль

    :param text: имя (строка)
    :param file: путь к файлу вывода
    """
    print('Undefined name:', text, file=file)
    print('Undefined name:', text)


class BetText:
    def __init__(self, name, text):
        self.name = name
        self.text = text


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.bet_texts = []
        self.score = []
        with open('flags.txt', 'r') as flags:
            self.betters = get_flags(flags)
        self.set_names(get_names(self.betters))

        self.ui.Save_Button.clicked.connect(self.save)
        self.ui.Count_Button.clicked.connect(self.count)
        self.ui.Reset_Button.clicked.connect(self.clear)

    def save(self):
        with open('saved.txt', 'w'):
            pass
        with open('saved.txt', 'a') as saved:
            print(self.ui.score_line.text(), file=saved)
            for bet_text in self.bet_texts:
                text = bet_text.text.toPlainText()
                print(bet_text.name, file=saved)
                print(text, file=saved)
                print('', file=saved)
        if self.ui.Check_1_1.isChecked():
            print('True')
        else:
            print('False')

    def count(self):
        with open('saved.txt', 'w'):
            pass
        with open('saved.txt', 'a') as saved:
            self.score = get_scores(self.ui.score_line.text())
            for bet_text in self.bet_texts:
                text = bet_text.text.toPlainText()
                missing = get_missing(bet_text)
                bets_array = config_bets_array(text, missing)
                if bets_array is None:
                    print('error')
                else:
                    get_goals(bet_text.name, bets_array, self.score, self.betters)
                print(bet_text.name, file=saved)
                print(text, file=saved)
                print('', file=saved)

        with open('output.txt', 'w+') as output:
            with open('matches.txt', 'r') as matches:
                text = matches.readlines()
                for line in text:
                    get_matches(line, output, self.betters)

    def clear(self):
        for bet_text in self.bet_texts:
            bet_text.text.setPlainText('')

    # noinspection PyMethodMayBeStatic
    def set_names(self, name_array):
        for i, elem in enumerate(name_array):
            exec(f'self.ui.Name_{i + 1}.setText(elem)')
            exec(f'self.bet_texts.append(BetText(elem, self.ui.Text_{i + 1}))')


def main2():

    app = QtWidgets.QApplication([])
    application = Window()
    application.show()

    sys.exit(app.exec())


def main3():
    print(config_bets_array('1:2 ' * 10, [False] * 10))


if __name__ == '__main__':
    main2()
