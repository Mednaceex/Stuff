for layer_ind, layer in enumerate(reversed(self.layers)):
    length = len(self.layers)
    layer_index = length - layer_ind - 1
    if layer_index == length - 1:
        h = self.feedforward_to_layer(layer_index, x)
        for neuron_index, neuron in enumerate(layer):
            for index, weight in enumerate(neuron):
                d_L_d_h[layer_index][neuron_index][index] = d * neuron.derivative(h) * weight
                d_L_d_w[layer_index][neuron_index][index] = d * neuron.derivative(h) * h[index]
            d_L_d_b[layer_index][neuron_index] = d * neuron.derivative(h)
    else:
        h = self.feedforward_to_layer(layer_index, x)
        for neuron_index, neuron in enumerate(layer):
            for index, weight in enumerate(neuron):
                dldh = 0
                for i, past_neuron in enumerate(self.layers[layer_index + 1]):
                    dldh += d_L_d_h[layer_index + 1][i][neuron_index] * weight * neuron.derivative(h)
                d_L_d_h[layer_index][neuron_index][index] = dldh
                dldw = 0
                for i, past_neuron in enumerate(self.layers[layer_index + 1]):
                    dldw += d_L_d_h[layer_index + 1][i][neuron_index] * h[index] * neuron.derivative(h)
                d_L_d_w[layer_index][neuron_index][index] = dldw
            d_L_d_b[layer_index][neuron_index] = d * neuron.derivative(h)