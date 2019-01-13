from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model
from keras.optimizers import Adam 
import numpy as np
import tensorflow as tf
# import matplotlib.pyplot as plt

from collections import deque
from pathlib import Path
import argparse
import random
import math
import time
import csv
import sys
import os

from agent.runAgent import *
from agent.getMaxComboScore import getMaxComboScore
from agent.getMatrix import getMatrix
from agent.takeAction import generate_random
from random import randint
from agent.createActionSpace import createActionSpace
from agent.codeToLetter import codeToLetter

sys.path.append("../")
from calculate_score import calculate_score


class DQNAgent:
    def __init__(self, env):
        self.state_size = 4  # health of AI & player, agent cumulative wins, player cumulative wins
        self.action_size = 256  # 4^4 combinations
        self.combo_dim = 4  # ex: ABCD
        self.batch_size = 2
        self.num_hidden_layers = 2
        self.num_neurons = 5
        self.gamma = 0.95  # discount rate
        self.epsilon = 1.0  # exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.memory = deque(maxlen=100)
        self.env = env
        self.model = self._build_model()

    def _build_model(self):
        model = Sequential()
        model.add(Dense(self.num_neurons, input_dim=self.state_size, activation='relu'))
        model.add(Dense(self.num_neurons, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))

        model.compile(loss='mse',
                      optimizer=Adam(lr=self.learning_rate))
        return model

    def _replay(self):
        minibatch = random.sample(self.memory, self.batch_size)
        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = reward + self.gamma * \
                         np.amax(self.model.predict(next_state)[0])

                # print('\n')
                # print('self.model.predict(next_state) is')
                # print(self.model.predict(next_state))
                # print('self.model.predict(next_state)[0]')
                # print(self.model.predict(next_state)[0])
                # print('target is')
                # print(target)
                target_f = self.model.predict(state)
                # print('target_f is')
                # print(target_f)
                # print("target_f[0] is")
                # print(target_f[0])
                target_f[0][action] = target

				self.model.fit(state, target_f, epochs=1, verbose=0)
			if self.epsilon > self.epsilon_min:
				self.epsilon *= self.epsilon_decay

	def _act(self, state):
		if np.random.rand() <= self.epsilon:
			return generate_random(self.combo_dim)
		act_vals = self.model.predict(state)
		# print(np.argmax(act_vals[0]), type(np.argmax(act_vals[0])))
		print(act_vals)
		return np.argmax(act_vals[0])

	def _remember(self, state, action, reward, next_state, done):
		return self.memory.append((state, action, reward, next_state, done))

	def load(self, name):
		# self.model.load_weights(name)
		self.model = load_model(name)

	def save(self, name):
		# self.model.save_weights(name)
		self.model.save(name)

if __name__ == "__main__":
	max_health = 10 # initial health
	EPISODES = 20 # number of times we change matrix
	state_size = 4

	aciton_space = createActionSpace(state_size)
	env = env(max_health, None, None, aciton_space) # create an instance of the e-leap-ments AI
	agent = DQNAgent(env)
	agent.state_size = state_size
	done = False

	# load saved file if written. creates new file if does not exist
	saved_model_path = Path('saved_model')
	if saved_model_path.is_file():
		if not (os.stat(saved_model_path).st_size == 0):
			print("<---saved model detected, loading saved model--->")
			agent.load('saved_model')
	else:
		open('saved_model', 'w').close()

	open('actions.txt', 'w').close()

	for e in range(EPISODES):
		if e > 0:
			env.aciton_space = createActionSpace(agent.state_size)
		else:
			env.aciton_space = aciton_space

		reset = True
		state = agent.env.reset(e) # state is [self.agent_health, self.player_health, self.agent_wins, self.player_wins]
		state = np.reshape(state, [1, agent.state_size]) # reshapes state dim
		env.state = state
		env.matrix = getMatrix()
		env.max_combo_score = getMaxComboScore(agent.env.matrix) # get max score of new matrix board
		t_start = time.time()
		reward_f = 0
		player_health = 100
		for time_t in range(200):

			action = agent._act(env.state)

			# write curr action to file
			act_out = codeToLetter(env.aciton_space[action])

			with open('action_output.txt', 'w') as f:
			    writer = csv.writer(f)
			    writer.writerow(act_out)

			"""
			to be implemented: get player action
			store player action in a global file actions.txt
			"""
			player_action_file = Path('actions.txt')
			print('exists??? ', player_action_file.is_file())
			while True: # code puts on a halt while waiting for the user to perform an action
				if player_action_file.is_file():
					if not (os.stat(player_action_file).st_size == 0):
						print("<---player action detected, prompting AI to take action now--->")
						break

			open('actions.txt', 'w').close()

			# retrieves player's action and convert action string to score
			with open('actions.txt', 'r') as r:
				temp = r.read().splitlines()
				for line in temp:
					player_action += line
					break
				print('player_action: ', player_action)

			# print('player_action is ', player_action)
			player_score = 0
			player_score = calculate_score(player_action, env.matrix)

			next_state, reward, done = agent.env.step(action, player_score, player_health, reset) 
			reset = False

			reward_f += reward

			next_state = np.reshape(next_state, [1, agent.state_size])

			agent._remember(env.state, action, reward, next_state, done)

			state = next_state
			env.state = state # keep env updated 

			if (time_t % 10) == 0: # save model every 10 epochs
				open('saved_model', 'a').close()
				agent.save('saved_model')

			if done:
				print("episode: {}/{}, trials in this ep: {}, agent wins: {}"
					  .format(e+1, EPISODES, time_t+1, env.agent_wins+1))
				break
			if len(agent.memory) > agent.batch_size:
				print('<---memory size reaches batch_size, time to _replay--->')
				agent._replay()
		t_end = time.time()
		length = t_end - t_start



