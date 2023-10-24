import torch
import copy
import random
import keyboard

import requests

import neural_network as Flappy_NN
# import flappy_bird as Flappy


# méthode à implémenter snipets
def crossover(parent1, parent2):
    child = copy.deepcopy(parent1)
    
    crossover_point = random.randint(0, len(parent1.fc1.weight.flatten()) - 1)
    
    flat_weights_p1_1 = parent1.fc1.weight.flatten()
    flat_weights_p2_1 = parent2.fc1.weight.flatten()

    flat_weights_p1_2 = parent1.fc2.weight.flatten()
    flat_weights_p2_2 = parent2.fc2.weight.flatten()

    flat_weights_p1_3 = parent1.fc3.weight.flatten()
    flat_weights_p2_3 = parent2.fc3.weight.flatten()
    
    child.fc1.weight = torch.nn.Parameter(torch.cat((flat_weights_p1_1[:crossover_point], flat_weights_p2_1[crossover_point:])).reshape(parent1.fc1.weight.shape))
    child.fc2.weight = torch.nn.Parameter(torch.cat((flat_weights_p1_2[:crossover_point], flat_weights_p2_2[crossover_point:])).reshape(parent1.fc2.weight.shape))
    child.fc3.weight = torch.nn.Parameter(torch.cat((flat_weights_p1_3[:crossover_point], flat_weights_p2_3[crossover_point:])).reshape(parent1.fc3.weight.shape))

    return child

def mutate(agent, mutation_rate):
    mutation_scale = 0.2
    
    for param in agent.parameters():
        if random.random() < mutation_rate:
            noise = torch.randn_like(param) * mutation_scale
            param = param + noise


    return agent

if __name__=='__main__':
        
    # Initialisation
    population_size = 30
    population = [Flappy_NN.NeuralNetworkFlappy() for _ in range(population_size)]

    # Paramètres
    num_generations = 150
    top_k = 5  # Nombre d'agents à sélectionner pour le croisement
    mutation_rate = 0.15

    # Boucle sur les générations
    for generation in range(num_generations):
        
        # Évaluation
        scores = []
        for agent in population:
            score = agent.evaluate()
            scores.append(score)
        
        # Sélection
        sorted_indices = sorted(range(len(scores)), key=lambda k: scores[k])
        top_indices = sorted_indices[-top_k:]
        top_agents = [population[i] for i in top_indices]
        
        # Croisement et Mutation
        new_population = []
        while len(new_population) < population_size:
            parent1, parent2 = random.choices(top_agents, k=2)  # Selection aléatoire de deux parents parmi les meilleurs
            # parent1, parent2 = top_agents[0:2]  # Selection aléatoire de deux parents parmi les meilleurs
            child = crossover(parent1, parent2)  # Implemente cette fonction pour faire le croisement
            mutate(child, mutation_rate)  # Implemente cette fonction pour faire la mutation
            new_population.append(child)
        
        # Remplacement
        population = new_population

        if keyboard.is_pressed('q'):  # q est la touche que j'ai choisie, tu peux choisir n'importe quelle touche.
            print("Stopping and saving best model.")
            torch.save(top_agents[0].state_dict(), f"best_model_final.pth")

            break
        str_to_send = f"Generation {generation} complete. Best score: {max(scores)}"
        print(str_to_send)
        torch.save(top_agents[0].state_dict(), f"best_model_gen_{generation}.pth")

