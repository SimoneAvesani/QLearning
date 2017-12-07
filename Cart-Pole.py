# coding=utf-8
import gym
import random
import math
import numpy as np
import operator
from math import pi
from numpy import interp
#import matplotlib.pyplot as plt

# CONST 

NUM_EP = 2000
NUM_T = 200
DIM_P = 100 # Matrix dimension ----> Precision
MAX_REWARD = 100
env = gym.make('CartPole-v0')
list_value = list()


class Q_learning:

    def __init__(self, r, q):

        self.r = r #(DIM_P, DIM_P, DIM_P, DIM_P, 2)
        self.q = q

    def gen_matrix(self, cart_pos, cart_speed, angle, angle_speed, action):
        '''
        Generzione matrice r dei reward 
        '''
        DIM_P = cart_pos        #inizializzazione DIM_P a 100
        matrix = np.zeros((cart_pos, cart_speed, angle, angle_speed, action))  
        matrix = matrix - 1;       #inizializzazione matrice a -1
        optimal = DIM_P / 2        #inizializzazione ottimo a 50
        matrix[optimal, optimal, optimal, optimal, :] = MAX_REWARD   #inizializzazione stato ottimo
        suboptimal = [DIM_P / 4, DIM_P / 4 * 2 - 1, DIM_P / 4 * 2 + 1, DIM_P / 4 * 3]    
        matrix[:, :, suboptimal[0]:suboptimal[1], :, 0] = MAX_REWARD / 3
        matrix[:, :, suboptimal[2]:suboptimal[3], :, 1] = MAX_REWARD / 3
        matrix[:, :, suboptimal[0] - DIM_P / 6: suboptimal[0] - 1, :, 0] = MAX_REWARD / 10
        matrix[:, :, suboptimal[3] + 1: suboptimal[3] + DIM_P / 6, :, 1] = MAX_REWARD / 10
        matrix[optimal, optimal, suboptimal[2]:optimal, optimal+1:suboptimal[3], 1] = MAX_REWARD/2
        matrix[optimal, optimal, optimal:suboptimal[3], suboptimal[2]:optimal-1, 0] = MAX_REWARD/2
        return matrix   #matrice dei reward


    def alg_q(self, state): 
        '''
        alg_q riceve in ingresso lo stato presente, al suo interno viene scelta l'azione prossima,
        vengono aggiornati i reward nella matrice.
        Il metodo ritorna il nuovo stato, l'angolo d'inclinazione del pole e la posizione del cart. 
        '''
        alpha = 0.9
        learning_rate = 1   #inizializzazione learning rate

        action = self.exploration(state)  # invocazione exploration
        observation, reward, done, info = env.step(action)     #passo futuro
        max_env = env.observation_space.high    # inizializzazione limite maggiore observation
        min_env = env.observation_space.low     # inizializzazione limite inferiore observation
        # inizializzazione posizione Cart
        cart_pos = observation[0]  
        cart_pos = int(interp(cart_pos,[min_env[0], max_env[0]], [0,DIM_P - 1]))   #interpolazione posizione del Cart
        # inizializzazione angolo di inclinazione del Pole
        angle = observation[2]
        angle = int(interp(angle,[-pi / 2, pi / 2], [0,DIM_P - 1]))    #interpolazione angolo di inclinazione
        # inizializzazione velocità angolare del Pole
        angle_speed = observation[3]  
        angle_speed = int(interp(angle_speed,[min_env[3],max_env[3]], [0,DIM_P - 1]))    #interpolazione velocità angolare
        # inizializzazione velocità del Cart
        cart_speed = observation[1]
        cart_speed = int(interp(cart_speed,[min_env[1],max_env[1]], [0,DIM_P - 1]))    #interpolazione velocità Cart

        print("angle rad: ", observation[2], "\nangle interp:", angle)
        state = (cart_pos, cart_speed, angle, angle_speed)     # inizializzazione stato presente
        av = self.r[cart_pos][cart_speed][angle][angle_speed][action]        #assegnamento ad av del reward della matrice r nello stato presente
        pv = self.q[cart_pos][cart_speed][angle][angle_speed][action]        #assegnamento a pv del reward della matrice q nello stato presente

        self.q[cart_pos][cart_speed][angle][angle_speed][action] = pv + learning_rate * (av + alpha * max(self.q[cart_pos, cart_speed, angle, angle_speed, :]) - pv)  # aggiornamento matrice dei reward      
    
        return state, angle, cart_pos  

    def exploration(self, state): 
        '''
         Riceve in ingresso lo stato presente e ritorna l'azione prossima 
        '''
        actions = [0,1]       #lista azioni eseguibili
        epsilon = 0.3
        random_state = random.random()
        i = int()
        if random_state < epsilon:    #se un numero random è minore di epsilon
            random.shuffle(actions)   #scelgo un'azione random
            i = actions[0]
            epsilon = epsilon - 0.001
        else:
            i = np.argmax(self.q[state])       #scelgo l'azione che porta ad un reward maggiore
        return i  #azione da compiere


r = np.zeros((DIM_P, DIM_P, DIM_P, DIM_P, 2))   #inizializzazione matrice r a 0
q = np.zeros_like(r)       #inizializzazione matrice q a 0
agent = Q_learning(r,q)    #creazione oggetto agent
agent.r = agent.gen_matrix(DIM_P, DIM_P, DIM_P, DIM_P, 2)  #inizializzazione matrice r dell'oggetto agent
agent.q = np.zeros_like(agent.r)        #inizializzazione matrice q dell'oggeto agent
state_temp = (0, 0, 0, 0)  #stato iniziale


for i in range(NUM_EP):
    observation = env.reset() 
    print("Episode #" + str(i));
    for z in range(NUM_T):
        env.render()
        state_temp, angle, position = agent.alg_q(state_temp)  #invocazione metodo alg_q  
        if angle >= DIM_P / 5 * 4 or angle <= DIM_P / 5 or position <= DIM_P / 3 +10 or position >= DIM_P / 4*3 - 10:  #condizione di stop
            break 
env.close()    


