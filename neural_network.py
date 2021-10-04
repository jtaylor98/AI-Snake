import numpy as np
#20 x 3 = 60 inputs neurons
#60 x 16 = 960 weights for layer 1
#16 x 16 = 256 weights for layer 2
#16 x 2 = 32 weights for last layer
#16 + 16 + 2 = 34 biases
#960 + 256 + 32 + 34 = 1282 total coefficients

class DenseLayer:
    def __init__(self, n_inputs, n_output_neurons, coeff):
        #creates an array of specified size and fills w/ random values per std normal distribution (-1 to 1)
        #n_inputs is size of sample (# of edges into one neuron)
        #each row represents the output for a neuron
        #each column represents the different weights for that neuron
        self.weights = [[coeff.pop(0) for _ in range(n_output_neurons)] for i in range(n_inputs)]
        self.weights = np.array(self.weights)
        self.biases = np.array(coeff[:])

    def forward(self, inputs):
        #first row of inputs x first column of weights
        #first row of inputs x second column of weights and so on...
        #then second row of inputs x first column of weights
        self.output = np.dot(inputs, self.weights) + self.biases #(inputs x weights) + biases

def sigmoid(input):
    return 1 / (1 + np.exp(-input))

class Network:
    def __init__(self, structure, coeff):
        self.n_layers = len(structure)-1
        self.layers = [] #will hold each layer in network
        self.coeff_per_layer = []
        for i in range(self.n_layers): #calculating number of all coefficients (all weights and biases) per layer    
            self.coeff_per_layer.append((structure[i] * structure[i+1]) + structure[i+1])  

        start = 0
        for i in range(self.n_layers): #adding each network layer to list
            end = start+self.coeff_per_layer[i]
            self.layers.append(DenseLayer(structure[i], structure[i+1], coeff[start:end])) #giving coeff to layer if specified by parameters
            start = end     
            
    def think(self, input):
        for layer in self.layers:
            layer.forward(input) #calculating weighted sums and biases of given layer
            y = sigmoid(layer.output) #applying activation function
            input = y
        if len(np.shape(y)) == 1: input = [y]
        else: input = y
        direction = round((input[0][0] - input[0][1]) * 100)#taking product of differences of two outputs and rounding it to use as change in angle value that will be added on to current line angle
        return direction
