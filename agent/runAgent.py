from getMaxComboScore import getMaxComboScore
from getScore import getScore


"""
motivation to use health points in RL agent:

by taking the opponent's health into account, 
the agent inadvertently takes into account of
how its action affects the performance of the player
so this implies the ideal AI will not necessarily always take the action 
which directly max the current reward but the overall cumulative rewards
and gradually learn to counter its opponent - the user 
by manipulating the user's psychological state
this can be achieved by 

1. setting a terminating threshold and a worst penalty
for when the AI's health reaches below a certain threshold 
due to user's inflicted damage points

2. keep track of the user's health points. This helps the AI 
learn how winning and losing at an incremental level affects the user's performance
both players get positive health points 
when their performed action is the max combo possible

"""

class env():
	def __init__(self, max_health, max_combo_score, matrix, action_space):
		self.state = None 
		self.reward = None
		self.episode = 0	
		self.fate = None # win: 1 loss: 0
		self.matrix = matrix 
		self.action_space = action_space
		self.agent_wins, self.player_wins = 0, 0
		self.max_health, self.agent_health, self.player_health = max_health, max_health, max_health
		self.max_combo_score = max_combo_score
		

	def step(self, action, player_score, player_health, reset): # returns next state, reward, done
		no_action = None
		done = False

		if reset == True:
			self.reward = 0 # cumulative rewards in an episode

		# calculate damage point
		print("??????", self.action_space)
		print('max_combo_score ', self.max_combo_score)
		score = getScore(self.action_space[action], self.matrix)
		# print('type of action: ', type(action))
		# print('matrix: ', self.matrix)

		# calculate rewards
		self.agent_health -= player_score
		self.player_health -= score
		if self.agent_health <= 0:
			self.agent_health = 0
			self.agent_wins -= 1
			self.player_wins += 1
			done = True

		if self.player_health <= 0:
			self.player_wins -= 1
			self.agent_wins += 1
			done = True

		# print(self.player_health)
		# print(self.agent_health, '\n')

		next_state = [self.agent_health, self.player_health, self.agent_wins, self.player_wins]
		return next_state, self.reward, done

	def reset(self, episode): # returns new initial raw file and state 
		self.reward = 0
		self.episode = episode	
		self.fate = None # win: 1 loss: 0
		self.agent_health, self.player_health = self.max_health, self.max_health
		self.max_combo_score = None
		self.state = [self.agent_health, self.player_health, self.agent_wins, self.player_wins]
		
		return self.state



