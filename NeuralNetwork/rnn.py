import numpy as np


def activation_function_output_layer(x):
    return tanh(x);
def d_activation_function_output_layer(x):
    return 1-np.square(tanh(x));
def activation_function_hidden_layer(x):
    return np.maximum(x,0);
def d_activation_function_hidden_layer(x):
    return int(x>0);
def error(network_output,exact_output):
    return np.mean(np.square(np.array(network_output)-np.array(exact_output)));
def derror(network_output,exact_output):
    return 2*np.mean(np.array(network_output)-np.array(exact_output));

class NeuralNetwork:
    #Constructing The Neural Network's Data Structure
    def __init__(self, Nlayers , Nneurons  ):
        self.Nlayers = Nlayers;#Number of layers
        self.Nneurons = Nneurons;#Number of Neurons
        self.hasBiasNeuron = np.zeros(Nlayers).astype(int);#disabled for now, One bais neuron allowed per layer
        self.LearningRate = 0.1 ; #value of choice
        self.momentum = 0.005; #value of choice
        self.O = [0]*Nlayers;#Output by each layer. It is not calculated for first layer
        self.I = [NAN]*Nlayers;#Input from layer n-1 to n. 
        self.W = [0]*Nlayers;#weight matrix(perception or knowledge)
        self.dEdI = [0]*Nlayers;#Gradient
        self.dW = [0]*Nlayers;#change in weight
        self.dWold = [0]*Nlayers;#This is considered to avoid being trapped in local minima/maxima
        self.factiv = ["Activation function for each layer"]*Nlayers;
        self.dfactiv = ["derivative of Activation function for each layer"]*Nlayers;
        
    #Constructing The Neural Network
    def make_ffnet(self): 
        for layer in range(0,self.Nlayers):
            self.O[layer] = np.zeros([self.Nneurons[layer]+self.hasBiasNeuron[layer],1]);#first layer is input
            self.I[layer] = np.zeros([self.Nneurons[layer]+self.hasBiasNeuron[layer],1]);#first layer is same as O
            self.dEdI[layer] = np.zeros([self.Nneurons[layer]+self.hasBiasNeuron[layer],1]);
            self.factiv[layer] = activation_function_hidden_layer;
            self.dfactiv[layer] = d_activation_function_hidden_layer;
            if layer<self.Nlayers-1:
                self.W[layer] = np.random.normal(0, 2/(self.Nneurons[layer]+self.Nneurons[layer+1]), [self.Nneurons[layer+1],self.Nneurons[layer]]);
                self.dW[layer] =  np.zeros([self.Nneurons[layer+1],self.Nneurons[layer]]);
                self.dWold[layer] = np.zeros([self.Nneurons[layer+1],self.Nneurons[layer]]);
        self.factiv[self.Nlayers-1] = activation_function_output_layer;
        self.dfactiv[self.Nlayers-1] = d_activation_function_output_layer;

    #[Training and Post-Training]Generates output corresponding to input and initial weigths
    def feedforward(self,feed):
        self.I[0] = feed;
        self.O[0] = feed;
        for layer in range(1,self.Nlayers):
            self.I[layer] = self.W[layer-1].dot(self.O[layer-1]);
            self.O[layer] = self.factiv[layer](self.I[layer]);
            
    #[Training The Network] Adjusts weigths based on output from feedforward and excat output already available
    def backprop(self,exact_output):
        self.dWold = self.dW;
        self.dEdI[self.Nlayers-1] = derror(self.O[self.Nlayers-1],exact_output)*(self.dfactiv[self.Nlayers-1](self.I[self.Nlayers-1]));#For Output layer, calculation is a bit different
        for layer in range(self.Nlayers-2,0,-1):
            for i in range(0,self.Nneurons[layer]):
                self.dEdI[layer][i] = np.sum(np.transpose(self.dEdI[layer+1]).dot(np.transpose(self.W[layer])[i]))*(self.dfactiv[layer](self.I[layer][i]));
        for layer in range(self.Nlayers-2,-1,-1):
            self.dW[layer] = - self.LearningRate*(np.outer(self.dEdI[layer+1],self.O[layer]));#storing dw to use in next iteration
            self.W[layer]  = self.W[layer]+ self.dW[layer] + self.momentum*self.dWold[layer];#weight Adjusted
        
        
