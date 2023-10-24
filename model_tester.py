import torch
import copy
import random
import keyboard

import os

import neural_network as Flappy_NN

folder = "insane-model"
filename = "best_model_gen_1.pth"

model = Flappy_NN.NeuralNetworkFlappy()

model.load_state_dict(torch.load(os.path.join(folder, filename)))

print(model.evaluate())
