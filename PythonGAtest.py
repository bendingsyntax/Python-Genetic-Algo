from fuzzywuzzy import fuzz #fuzzywuzzy is for string comparison, used pip to install fuzzywuzzy, fuzz is a specific function in fuzzywuzzy library
import random #for random numbers
import string #string library
from datetime import datetime
import os

class Agent:  #creates a class called agent (object)
    def __init__(self, length): #initial constructor, self is always first, uses length to define it
        self.string = ''.join(random.choice(string.ascii_letters) for j in range(length))#creates self.string as a member of the agent class and then add a random letter with a for loop until the lenght is filled.
        self.fitness = -1 #creates a scale to compare individuals
    def __str__(self): #creates string contrsuctor for output.
        return 'String: ' + str(self.string) + ' Fitness ' + str(self.fitness) # returns the entire random string we created.

in_str = None  #creates a variable for initial string.
in_str_len = None #creates a variable for initial string length
population = 10000 #creates population variable and sets to a size
generations = 10000 #creates generation variable and sets to a size
outputfile = open(r'~\output.txt', "w+")

def GeneticAlgo(): #genetic algorithm function
    agents = init_agents(population, in_str_len)#fetches value from function init_agents
    for generation in range(generations): #creates a loop to cycle through the generations
        #outputfile.write('\nGeneration: ' + str(generation) + '\n')#prints out the current generation
        agents = fitness(agents) #fetches value from fitness function
        agents = selection(agents) #fetches value from selection function
        agents = crossover(agents) #fetches value from crossover function
        agents = mutation(agents) #fetches value from mutation function

        if any(agent.fitness >= 100 for agent in agents): #creates a condition to check if a specified fitness level is reached
            end_time = datetime.now()
            outputfile.write('\n' + 'Duration: {}'.format(end_time - start_time) + '\n')
            outputfile.write('\nFitness level achieved at Generation :' + str(generation) + '!\n') #output reaching fitness level
            outputfile.write('\n'.join(map(str, agents)))
            exit(0) #exits program entirely

def init_agents(population, length): #initial agents function with two parameters
    return [Agent(length) for _ in range(population)] #creates a number of agents based on populaiton variable

def fitness(agents): # defines fitness function
    for agent in agents: # creates a for loop for the number of agents
        agent.fitness = fuzz.ratio(agent.string, in_str) #sets the fitness level of each agent

    return agents

def selection(agents): #defines selection function
    agents = sorted(agents, key=lambda agent: agent.fitness, reverse=True) #sorts the list and reverse the order because sort default asending
    #outputfile.write('\n'.join(map(str, agents))) #outputs a map or list of the agents
    agents = agents[:int(0.01 * len(agents))] #marks the cut off for selection to next generation to the top 20%

    return agents

def crossover(agents): #defines crossover function
    offspring = [] #creates an empty array for offspring
    pairs = int(round(population - len(agents)) / 2) #divides the population in pairs for creating new genetic combinations

    for _ in range(pairs): #creates a for loop for the whole number of pairs
        p1 = random.choice(agents) # defines a first parent with a random string
        p2 = random.choice(agents) # defines a second parent with a random string
        c1 = Agent(in_str_len) # defines a first child with a set length
        c2 = Agent(in_str_len) # defines a second child with a set length
        split = random.randint(0, in_str_len) #sets the single point crossover value between zero and the maximum length
        c1.string = p1.string[0:split] + p2.string[split:in_str_len] #cross over the first half of the first parent and the second half of the second parent and set the childs value
        c2.string = p2.string[0:split] + p1.string[split:in_str_len] #cross over the first half of the second parent and the first half of the first parent and set the second childs value

        offspring.append(c1)# adds the first child to the offspring list
        offspring.append(c2)# adds the second child to the offspring list

    agents.extend(offspring)# adds the offspring list to the end of agents list

    return agents

def mutation(agents): #mutation function
    for agent in agents: #for loop for each agent
        k = 0
        stringLength = len(agent.string)
        while k < stringLength:
            if random.uniform(0.0, 1.0) <= .0063: #picks a random number between 0.0 and 1.0 and checks if it is less than .1
                agent.string = agent.string[0:k] + random.choice(string.ascii_letters) + agent.string[k:in_str_len]#the value at idx in the string will be replaced with a random letter
            k += 1
    return agents

if __name__ == '__main__':#main function
    start_time = datetime.now()
    in_str = "rTaOcTiq5bkpqLs3WjCAyHwJHl9htQih0DQUjcojCOlHKBqcL3X5DemZ4HsQL7lKcVzEqwKGD5x6ztztGKA4q78Evw8Wk5XMV62cWwULmt8cdMzZplB5GxkYbSJ8PD85" #random generated string.
    in_str_len = len(in_str) #gets the length of the random string
    GeneticAlgo() #calls the GeneticAlgo function
    outputfile.close()