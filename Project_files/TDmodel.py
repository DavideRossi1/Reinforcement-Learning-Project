import numpy as np
import Constants as C
import numpy as np
class TDControl():
    def __init__(self,space_size,action_size,gamma=C.GAMMA,learning_rate=C.LEARNING_RATE,algorithm='SARSA'):
        """
        Calculate optimal policy using in-policy Temporal Difference control
        Evaluate Q-value for (S,A) pairs, using one-step updates.
        """
        
        assert algorithm in ['SARSA','Qlearning','ExpectedSARSA'], "Algorithm not recognized"
        
        self.gamma = gamma                  # discount factor
        self.space_size = space_size        # size of system
        self.action_size = action_size      # number of possible actions
        self.learning_rate = learning_rate  # learning rate
        self.algorithm = algorithm          # algorithm to be used: SARSA, Qlearning, ExpectedSARSA
        self.get_policy()                   # where to save returns
        
        
        
    def get_policy(self): 
        """
        Initialize Qvalues array that represents the policy
        """
        
        # if no policy is imported, initialize Qvalues to 0
        if C.IMPORTPOLICY==0:
            self.Qvalues = np.zeros( (*self.space_size, self.action_size) )
            
        # otherwise, import the policy from a txt file
        else:
            onedimension_Qvalues = np.loadtxt(C.IMPORTPOLICY)
            self.Qvalues = np.reshape(onedimension_Qvalues, (*self.space_size, self.action_size))
    
    
    
    def single_step_update(self, state, action, reward, new_state, new_action, gameover, eps):
        """
        Update the policy for the current state and action, using the TDControl algorithm
        """
        if gameover:
            deltaQ= reward - self.Qvalues[(*state, action)]
        else:
            
            # SARSA: delta=R+gamma*Q(S',A')-Q(S,A)
            if self.algorithm=='SARSA':
                deltaQ= reward + self.gamma*self.Qvalues[(*new_state, new_action)] - self.Qvalues[(*state, action)] 
                
            # Qlearning: delta=R+gamma*max_a(Q(S',a))-Q(S,A)
            elif self.algorithm=='Qlearning':
                deltaQ= reward + self.gamma*np.max(self.Qvalues[(*new_state,)]) - self.Qvalues[(*state, action)]
                
            # ExpectedSARSA: delta=R+gamma*sum_a(pi(a|S')*Q(S',a))-Q(S,A)
            elif self.algorithm=='ExpectedSARSA':
                deltaQ= reward + self.gamma*np.dot(self.Qvalues[(*new_state,)],self.policy(new_state,eps)) - self.Qvalues[(*state, action)]
                
        # update the policy with TD(0)
        self.Qvalues[(*state, action)] += self.learning_rate*deltaQ
        
        
        
    def policy(self,state,eps): 
        """
        Return the policy for the given state
        """
        # start with a uniform probability of choosing each action
        policy = np.ones(self.action_size)*eps/self.action_size
        
        # select the action(s) with the highest Qvalue for the given state
        best_value=np.max(self.Qvalues[(*state,)])
        best_actions= (self.Qvalues[ (*state,) ] == best_value)
        
        # update the policy
        policy+=best_actions*(1-eps)/np.sum(best_actions)
        return policy
    
    
    # not used
    # def greedy_policy(self):
    #     """
    #     Returns the greedy policy
    #     """
    #     pol=np.argmax(self.Qvalues,axis=2)
    #     return pol
    
    
    
    def getact_eps_greedy(self,state,eps): 
        """
        Return the action to be taken for the given state, using an epsilon-greedy policy
        """
        if np.random.rand()<eps: 
            # random action, with uniform probability, with probability eps
            prob_actions=np.ones(self.action_size)/self.action_size
            
        else:
            # choose the best action, with probability 1-eps
            best_value=np.max(self.Qvalues[(*state,)]) 
            best_actions= (self.Qvalues[ (*state,) ] == best_value) # in case there is more than one best action...
            prob_actions=best_actions/np.sum(best_actions)
        action=np.random.choice(self.action_size,p=prob_actions)         #...choose one of them randomly
        return action
       
       
            
    def save_policy(self): 
        """
        Save the learned policy in a txt file
        """
        
        # A header is added to the file, containing the parameters used for training
        comments="Algorithm: {}, Speed: {}, Boost: {}, PM: {}, Env size: {}, Car size: {}, Counter: {}, Nsteps: {}, Gamma: {}, LearnRate: {}, Eps: {}, Epsdecay: {}".format(C.AGENT,C.SPEED,C.BOOST,C.PACMAN,C.ENVSIZE,C.CARSIZE,C.COUNTER,C.NSTEPS,C.GAMMA,C.LEARNING_RATE,C.EPSILON,C.EPSDECAY)
        onedimension_Qvalues=np.reshape(self.Qvalues,C.QSIZE)
        np.savetxt(C.EXPORTPOLICY,onedimension_Qvalues,header=comments)
        