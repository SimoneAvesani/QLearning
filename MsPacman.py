# coding=utf-8
import gym
import random
import math
import numpy as np
import operator
#from hashable import hashable 
from math import pi
from numpy import interp, uint8
from hashlib import sha1


# CONST
NUM_EP = 1000
NUM_T = 999999
counter = 0
future_action = 0
env = gym.make('MsPacman-v0')
list_decision = list()
action = int()
counter = 0

class Q_learning:
	
	def __init__(self, r_dict, dict_action):

		self.r_dict = r_dict 
		self.dict_action = dict_action

	def alg_q(self, state, init):
		counter = int()
		alpha = 0.9
		learning_rate = 1		

		action = self.exploration(state,init)  # invocazione exploration
		observation, reward, done, info = env.step(action)     #prossimo step
		#state = hashable(observation)    # inizializzazione stato presente
		state = int(sha1(observation.view(uint8)).hexdigest(), 16) # hashing dell'oggetto state
		list_keys = dict_action.keys()
		
		if state not in list_keys:		# se lo stato non è nella lista delle chiavi di un'azione lo aggiungo
			self.dict_action[state] = [0.,0.,0.,0.,0.,0.,0.,0.,0.]

		max_reward = max(dict_action[state]) 
		self.dict_action[state][action] = dict_action[state][action] + learning_rate * (reward + alpha * max_reward - dict_action[state][action]) 	  

		return state, done


	def exploration(self, state, init): 
		actions =[0, 1, 2, 3, 4, 5, 6, 7, 8]
		random_state = random.random()
		epsilon = 0.3
	  	i = int()
		if random_state < epsilon or init == 0:
		    init = 1
		    random.shuffle(actions)
		    i = actions[0]
		    epsilon = epsilon - 0.001
		else:
				i = index(max(dict_action[state]))
		return i  # azione prossima

r_dict = {}
dict_action = {}
text_file = open("Output2.txt","w")
state_temp = int()
agent = Q_learning(r_dict, dict_action)
for i in range(NUM_EP):
    init = 0
    observation = env.reset()
    text_file.write("Episode #" + str(i) + "\n")
    print("Episode #" + str(i))
    for z in range(NUM_T):
        env.render()
        state_temp, done = agent.alg_q(state_temp,0) 
        if done:
        	break
text_file.close()
env.close()    


