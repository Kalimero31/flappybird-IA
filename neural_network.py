import torch
import torch.nn as nn
import torch.optim as optim

import flappy_bird as Flappy


class NeuralNetworkFlappy(nn.Module):
    def __init__(self):
        super(NeuralNetworkFlappy, self).__init__()
        self.fc1 = nn.Linear(3, 32)
        self.fc2 = nn.Linear(32, 32)
        self.fc3 = nn.Linear(32, 1)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = torch.sigmoid(self.fc3(x))
        return x
    
    def get_action(self, state):
        tensor = torch.FloatTensor(state)
        prediction = self.forward(tensor).item()

        if prediction > 0.5:
            return 1
        else:
            return 0
    
    def evaluate(self):
        game = Flappy.Game()
        state = game.get_state()
        done = False
        total_reward = 0 # Score de la simulation

        while not done:
            action = self.get_action(state)
            next_state, reward, done = game.step(action)
            state = next_state
            total_reward += reward
            game.render()
            # print(state)
            # print(self.forward(torch.FloatTensor(state)))
            # print(action)
    
        return total_reward


    
# Peut servir mais à réparer
if __name__=='__main__':
    MyNN = NeuralNetworkFlappy()
    print(MyNN.evaluate())

    # L = []
    # for i in range(2000):
    #     model = NeuralNetworkFlappy()
    #     L.append(model.forward(torch.FloatTensor([170, 2800, -180])).item())

    # import statistics
    # print("min : ", min(L))
    # print("max: ", max(L))
    # print("mean", statistics.mean(L))




if __name__=='__main1__':
    pass

# Instanciation du modèle
    # model = NeuralNetworkFlappy()

    # # Exemple de données (distance au tuyau, hauteur de l'oiseau, hauteur du tuyau)
    # input_data = torch.FloatTensor([40, 100, 150])

    # # Prédiction
    # output = model(input_data)
    # action = "JUMP" if output.item() > 0.5 else "DO NOT JUMP"

    # print(f"Action à prendre : {action}")

    # # Entrainnement du modèle
    # for episode in range(1000):
    #     state = get_current_state()  # Tu dois implémenter cette fonction
    #     state_tensor = torch.FloatTensor(state).unsqueeze(0)  # Convertir l'état en tenseur

    #     # Passe avant
    #     output = model(state_tensor)
    #     action = torch.argmax(output).item()  # Prendre l'action ayant la plus grande valeur

    #     # Jouer l'action et obtenir la nouvelle récompense et le nouvel état
    #     new_state, reward = play_action(action)  # Tu dois implémenter cette fonction

    #     # Calculer la perte
    #     new_state_tensor = torch.FloatTensor(new_state).unsqueeze(0)
    #     reward_tensor = torch.FloatTensor([reward])

    #     criterion = nn.MSELoss()

    #     loss = criterion(output, reward_tensor)

    #     # Passe arrière
    #     optimizer = optim.Adam(model.parameters(), lr=0.001)
    #     optimizer.zero_grad()
    #     loss.backward()
    #     optimizer.step()
