

import numpy as np
import matplotlib.pyplot as plt
import copy
from random import random
from matplotlib.colors import ListedColormap
import matplotlib.patches as mPatches
import time


# Define grid size
N = 100


def initializePopulation(N: int):
    # 0 is susceptible
    # 1 is infected
    population = np.zeros((1, N), dtype=int)
    population[0, N//2] = 1
    return population


population = initializePopulation(N)


def updateState(population, gamma):
    newState = copy.deepcopy(population)

    for i in range(len(population[0])):
        # Rule for infected persons
        if population[0, i] == 1 and random() <= gamma:
            newState[0, i] = 0
            continue
        # Rule for susceptible
        # print(f"i: {i}\nvalue: {population[0, i]}")
        if i < N-1:

            if population[0, i-1] == 1 or population[0, i+1] == 1:
                if random() <= 1-gamma:
                    newState[0, i] = 1
                    # print("Infected\n")
        else:
            if population[0, i-1] == 1 or population[0, 0] == 1:
                if random() <= 1-gamma:
                    newState[0, i] = 1
                    # print("Infected\n")
    return newState


cmap = ListedColormap(["white", "red"])
susceptible_patch = mPatches.Patch(color="white", label="Susceptible")
infected_patch = mPatches.Patch(color="red", label="Infected")

# function to plot population


def plotPopulation(population, title, gamma, iteration):
    plt.figure(1)
    plt.title(title)
    plt.legend(handles=[infected_patch, susceptible_patch], loc="lower left")
    plt.imshow(population, vmin=0, vmax=len(cmap.colors), cmap=cmap)
    plt.yticks(color="w")
    plt.show()
    plt.savefig(f"{gamma}_{iteration}.png")

gamma = 0.3
plt.ion()
for i in range(100):
    population = updateState(population, gamma)
    # plotPopulation(population, f"Gamma: {gamma}. Iteration: {i}", gamma, i)
    if i in [10,30,60,90]:
        plotPopulation(population, f"Gamma: {gamma}. Iteration: {i}", gamma, i)
    # plt.pause(.5)


# exit(0)


# # Create gamma dictionary
# gamma = {}
# nmrGammas = 10
# for n in range(nmrGammas):
#     gamma[n/nmrGammas] = 0

# # Define number of simulations and steps for each simulation
# nmrSimulation = 100
# nmrSteps = 100

# for g, survivalCount in gamma.items():

#     for i in range(nmrSimulation):
#         # Create population
#         population = initializePopulation(N)
#         for j in range(nmrSteps):
#             # Update population
#             population = updateState(population, g)
#         if np.any(population[0,:]):
#             survivalCount +=1
#     print(f"Gamma: {g}. Survival percentage: {survivalCount/(nmrSimulation)}")
#     gamma[g] = survivalCount/(nmrSimulation)


# plt.plot(gamma.keys(), gamma.values())
# plt.xlabel("Gamma")
# plt.ylabel("Probability that virus survives")
# plt.title("Probability that virus survives as a function of gamma")
# plt.savefig("gammaSurvives.png")
# plt.show()

