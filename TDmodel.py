import numpy as np
import Constants as C
import numpy as np
class TDControl():
    def __init__(self,space_size,action_size,gamma=1,lr=0.01,algorithm='SARSA'):
        """
        Calculates optimal policy using in-policy Temporal Difference control
        Evaluates Q-value for (S,A) pairs, using one-step updates.
        """
        
        assert algorithm in ['SARSA','Qlearning','ExpectedSARSA'], "Algorithm not recognized"
        
        self.gamma = gamma             # discount factor
        self.space_size = space_size   # size of system
        self.action_size = action_size # number of actions
        self.lr = lr                   # learning rate
        self.algorithm = algorithm     # algorithm to be used: SARSA, Qlearning, ExpectedSARSA
        self.get_policy()              # where to save returns
        
    def get_policy(self): # returns the policy to be used
        if C.IMPORTPOLICY==0:
            self.Qvalues = np.zeros( (*self.space_size, self.action_size) )
        else:
            oneDQval = np.loadtxt(C.IMPORTPOLICY)
            self.Qvalues = np.reshape(oneDQval, (*self.space_size, self.action_size))
    
    def single_step_update(self, state, action, reward, new_state,new_action, done, eps):
        if done:
            deltaQ= reward - self.Qvalues[(*state, action)]
        else:
            if self.algorithm=='SARSA':
                deltaQ= reward + self.gamma*self.Qvalues[(*new_state, new_action)] - self.Qvalues[(*state, action)]
            elif self.algorithm=='Qlearning':
                deltaQ= reward + self.gamma*np.max(self.Qvalues[(*new_state,)]) - self.Qvalues[(*state, action)]
            elif self.algorithm=='ExpectedSARSA':
                deltaQ= reward + self.gamma*np.dot(self.Qvalues[(*new_state,)],self.policy(new_state,eps)) - self.Qvalues[(*state, action)]
        self.Qvalues[(*state, action)] += self.lr*deltaQ
        
    def policy(self,state,eps): # returns the possible actions with their probabilities
        policy = np.ones(self.action_size)*eps/self.action_size
        best_value=np.max(self.Qvalues[(*state,)])
        best_actions= (self.Qvalues[ (*state,) ] == best_value)
        policy+=best_actions*(1-eps)/np.sum(best_actions)
        return policy
    
    def greedy_policy(self):
        pol=np.argmax(self.Qvalues,axis=2)
        return pol
    
    def getact_eps_greedy(self,state,eps): # returns the single action to take
        if np.random.rand()<eps: # random action, with uniform probability, with probability eps
            prob_actions=np.ones(self.action_size)/self.action_size
        else:
            best_value=np.max(self.Qvalues[(*state,)]) # choose the best action, with probability 1-eps
            best_actions= (self.Qvalues[ (*state,) ] == best_value) # in case there is more than one best action...
            prob_actions=best_actions/np.sum(best_actions)
        a=np.random.choice(self.action_size,p=prob_actions)         #...choose one of them randomly
        return a
            
    def save_policy(self): # saves the policy in a txt file
        comments="Algorithm: {}, Speed: {}, Boost: {}, PM: {}, Environment size: {}, Car size: {}, Counter: {}, Nsteps: {}".format(C.AGENT,C.SPEED,C.BOOST,C.PACMAN,C.ENVSIZE,C.CARSIZE,C.COUNTER,C.NSTEPS)
        oneDQval=np.reshape(self.Qvalues,C.QSIZE)
        np.savetxt(C.EXPORTPOLICY,oneDQval,header=comments)
        