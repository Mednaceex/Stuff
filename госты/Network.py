import numpy as np


class Sigmoid:
    @staticmethod
    def sigmoid(x):
        # Сигмоидная функция активации: f(x) = 1 / (1 + e^(-x))
        return 1 / (1 + np.exp(-x))

    @staticmethod
    def deriv(x):
        # Производная сигмоиды: f'(x) = f(x) * (1 - f(x))
        fx = Sigmoid.sigmoid(x)
        return fx * (1 - fx)


def mse_loss(y_true, y_pred):
    # y_true и y_pred - массивы numpy одинаковой длины.
    return ((y_true - y_pred) ** 2).mean()


class Neuron:
    def __init__(self, weights: list, bias, input_count=None):
        if input_count is not None and input_count < len(weights):
            self.input_count = input_count
            self.weights = weights[:input_count]
        else:
            self.input_count = len(weights)
            self.weights = weights
        self.bias = bias

    def __getitem__(self, item):
        return self.weights[item]

    def sum(self, x: list):
        value = self.bias
        for i in range(self.input_count):
            value += self.weights[i] * x[i]
        return value

    def function(self, x: list):
        return Sigmoid.sigmoid(self.sum(x))

    def derivative(self, x: list):
        return Sigmoid.deriv(self.sum(x))


class Layer:
    def __init__(self, neurons_list: list, count_in_layer=None):
        if count_in_layer is not None and count_in_layer < len(neurons_list):
            self.count_in_layer = count_in_layer
            self.neurons_list = neurons_list[:count_in_layer]
        else:
            self.count_in_layer = len(neurons_list)
            self.neurons_list = neurons_list

    def __getitem__(self, item):
        return self.neurons_list[item]

    def feedforward(self, x: list):
        output = []
        for neuron in self.neurons_list:
            output.append(neuron.function(x))
        return output


class NeuralNetwork:
    """
    Нейронная сеть с:
      - 2 входами
      - скрытым слоем с 2 нейронами (h1, h2)
      - выходной слой с 1 нейроном (o1)
    """
    def __init__(self, layer_count, neuron_count, weight_count=None):
        self.layers = []
        self.layer_count = layer_count
        self.neuron_count = neuron_count
        if weight_count is None:
            self.weight_count = neuron_count
        else:
            self.weight_count = weight_count

        for i in range(self.layer_count - 1):
            neurons_list = []
            for j in range(self.neuron_count):
                neuron = Neuron([0.6] * self.weight_count, 0.6)
                neurons_list.append(neuron)
            layer = Layer(neurons_list)
            self.layers.append(layer)
        self.output_neuron = Neuron([0.6] * self.weight_count, 0.6)
        self.layers.append(Layer([self.output_neuron]))

    def feedforward(self, x):
        # x is a numpy array with 2 elements
        array = np.array(x)
        for layer in self.layers:
            array = layer.feedforward(array)
        return array[0]

    def train(self, data, all_y_trues):
        """
        - data - массив numpy (n x 2) numpy, n = к-во наблюдений в наборе.
        - all_y_trues - массив numpy с n элементами.
          Элементы all_y_trues соответствуют наблюдениям в data.
        """
        learn_rate = 0.1
        epochs = 1000  # сколько раз пройти по всему набору данных

        for epoch in range(epochs):
            for x, y_true in zip(data, all_y_trues):
                # --- Прямой проход (эти значения нам понадобятся позже)
                sum_h1 = self.layers[0][0].sum(x)
                h1 = self.layers[0][0].function(x)

                sum_h2 = self.layers[0][1].sum(x)
                h2 = self.layers[0][1].function(x)

                sum_o1 = self.output_neuron.sum(self.layers[0].feedforward(x))
                o1 = self.output_neuron.function(self.layers[0].feedforward(x))
                y_pred = o1

                # --- Считаем частные производные.
                # --- Имена: d_L_d_w1 = "частная производная L по w1"
                d = 2 * (y_pred - y_true)

                d_L_d_w = [[[0] * self.weight_count] * self.neuron_count] * self.layer_count
                d_L_d_b = [[0] * self.neuron_count] * self.layer_count
                # Нейрон o1

                for layer_index, layer in enumerate(self.layers):
                    length = len(self.layers)
                    if layer_index == length - 1:
                        for neuron_index, neuron in enumerate(layer):
                            for index, weight in enumerate(neuron):
                                d_L_d_w[layer_index][neuron_index][index] = d * h0 * neuron.derivative()

                # --- Обновляем веса и пороги
                # Нейрон h1
                for layer_index, layer in enumerate(self.layers):
                    for neuron_index, neuron in enumerate(layer):
                        for index, weight in enumerate(neuron):
                            neuron.weights[index] -= learn_rate * d_L_d_w[layer_index][neuron_index][index]
                        neuron.bias -= learn_rate * d_L_d_b[layer_index][neuron_index]

            # --- Считаем полные потери в конце каждой эпохи
            if epoch % 10 == 0:
                y_preds = np.apply_along_axis(self.feedforward, 1, data)
                loss = mse_loss(all_y_trues, y_preds)
                print("Epoch %d loss: %.3f" % (epoch, loss))


# Определим набор данных
data = np.array([
    [-2, -1],  # Алиса
    [25, 6],   # Боб
    [17, 4],   # Чарли
    [-15, -6],  # Диана
])
all_y_trues = np.array([
    1,  # Алиса
    0,  # Боб
    0,  # Чарли
    1,  # Диана
])

aboba = [[60, 20], [12, 10], [-1, -2], [-2, -3]]
# Обучаем нашу нейронную сеть!
network = NeuralNetwork(2, 2)
network.train(data, all_y_trues)
print(network.feedforward(aboba[0]))
print(network.feedforward(aboba[1]))
print(network.feedforward(aboba[2]))
print(network.feedforward(aboba[3]))
