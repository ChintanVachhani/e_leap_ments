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

from runAgent import env
from getMaxComboScore import getMaxComboScore
from getMatrix import getMatrix
from takeAction import generate_random
from random import randint
from createActionSpace import createActionSpace


class DQNAgent:
	def __init__(self, env):
		self.state_size = 4 # health of AI & player, agent cumulative wins, player cumulative wins
		self.action_size = 256 # 4^4 combinations
		self.combo_dim = 4 # ex: ABCD
		self.batch_size = 2
		self.num_hidden_layers = 2		
		self.num_neurons = 5
		self.gamma = 0.95    # discount rate
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

	episode_lengths = []
	episode_rewards = []

	for e in range(EPISODES):
		if e > 0:
			env.aciton_space = createActionSpace(agent.state_size)
		else:
			env.aciton_space = aciton_space
		print('as: ', env.aciton_space)
		reset = True
		state = agent.env.reset(e) # state is [self.agent_health, self.player_health, self.agent_wins, self.player_wins]
		state = np.reshape(state, [1, agent.state_size]) # reshapes state dim
		env.state = state
		env.matrix = getMatrix()
		env.max_combo_score = getMaxComboScore(agent.env.matrix) # get max score of new matrix board
		t_start = time.time()
		reward_f = 0
		player_health = 100
		for time_t in range(20):

			action = agent._act(env.state)


			"""
			to be implemented: get player health
			"""
			player_score = random.randint(1,2)
			print('before step ', agent.env.aciton_space)

			next_state, reward, done = agent.env.step(action, player_score, player_health, reset) 
			reset = False

			reward_f += reward

			next_state = np.reshape(next_state, [1, agent.state_size])

			agent._remember(env.state, action, reward, next_state, done)

			state = next_state
			env.state = state # keep env updated 

			if done:
				print("episode: {}/{}, trials in this ep: {}, agent wins: {}"
					  .format(e+1, EPISODES, time_t+1, env.agent_wins+1))
				break
		t_end = time.time()
		length = t_end - t_start

		# if time_t > 4:
		# 	print("Failed to complete in trial {}".format(time_t))
		if e > 5:
			agent._replay()


