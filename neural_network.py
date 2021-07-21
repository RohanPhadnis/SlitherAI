import random
from abc import ABC, abstractmethod


class Neuron:

    def __init__(self, num_inputs: int):
        self.weights = [random.random() * random.choice([-5, 5]) for _ in range(num_inputs)]
        self.bias = random.randint(-5, 5)

    def output(self, inputs: list):
        return sum([inputs[n] * self.weights[n] for n in range(len(self.weights))]) + self.bias


class Layer(ABC):

    def __init__(self, input_len: int):
        self.input_len = input_len

    @abstractmethod
    def output(self, inputs: list) -> list:
        pass


class DenseLayer(Layer):

    def __init__(self, input_len: int, units: int):
        super().__init__(input_len=input_len)
        self.units = units
        self.neurons = [Neuron(num_inputs=self.input_len) for _ in range(self.units)]

    def output(self, inputs: list) -> list:
        return [n.output(inputs) for n in self.neurons]


class Sequential:

    def __init__(self, layers: list):
        self.layers = layers

    def calc(self, inputs: list):
        outputs = []
        for i in inputs:
            temp = i
            for layer in self.layers:
                temp = layer.output(temp)
            outputs.append(temp)
        return outputs


model = Sequential([
    DenseLayer(units=32, input_len=5),
    DenseLayer(units=16, input_len=32),
    DenseLayer(units=8, input_len=16),
    DenseLayer(units=1, input_len=8)
])

inputs = [[n+m for n in range(5)] for m in range(10)]
print(model.calc(inputs))
