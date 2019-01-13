from getMaxComboScore import getMaxComboScore
from getReward import getReward
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
	def __init__(self, max_health, max_combo_score):
		self.action_space = [x for x in range(0, len(self.action_space_mappings))]
		self.state = None 
		self.reward = None
		self.episode = None	
		self.fate = None # win: 1 loss: 0
		self.max_health = max_health
		self.agent_health = max_health
		self.player_health = max_health
		self.max_combo_score = max_combo_score
		

	def step(self, action, player_health, reset): # returns next state, reward, done
		no_action = None
		done = False

		if reset == True:
			self.reward = 0

		# calculate damage point
		score = getScore(action)
		
		# calculate rewards
		self.agent_health -= score
		if self.agent_health <= 0:
			self.agent_health = 0
			done = True

		if self.player_score <= 0:
			self.player_health = 0
			done = True

		next_state = [self.agent_health, self.player_health]
		return next_state, reward, done

	def reset(self, episode): # returns new initial raw file and state 
		self.reward = 0
		self.episode = episode

		return self.state # episode = init state vec idx



