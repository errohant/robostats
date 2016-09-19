import matplotlib.pyplot as plt
import random
import math
import numpy as np

class Nature:
    def get_stoch_y(self):
        """Send random y"""
        return -1 if random.random() <= 0.5 else 1
    def get_determ_y(self,t):
        """Send deterministic y"""
        return -1 if t%3==1 else 1
    def get_adver_y(self, xt, w):
        """Send aversarial output"""
        yt_hat = 1 if sum(i[0]*i[1] for i in zip(w,xt)) <= 0 else -1
        return yt_hat

    def get_observation():
        return [-1 if random.random() <= 0.5 else 1,
                -1 if random.random() <= 0.5 else 1]

    """Observation = [Weather, Location]
       Weather: 0=bad 1=good
       Location: 0=away 1=home
    """
    def get_y_from_observation(self, observation):
        if observation[0]==0 and observation[1]==0:
            yt_hat=-1
        elif observation[0]==1 and observation[1]==0:
            yt_hat=-1
        elif observation[0]==0 and observation[1]==1:
            yt_hat=1
        else:
            yt_hat=1

class Expert:
    def get_expert_one_advice(self):
        """Always Win"""
        return 1
    def get_expert_two_advice(self):
        """Always Loose"""
        return -1

    def get_expert_three_advice(self, t):
        """Odd Even"""
        return -1 if t%2==1 else 1

    def get_expert_four_advice(self, t, observations):
        """Perceptron Learning Algorithm"""
        return 1
    def get_x(self, t):
        return (self.get_expert_one_advice(),
                self.get_expert_two_advice(),
                self.get_expert_three_advice(t))

class Algorithm:
    def __init__(self):
        self.expert = Expert()
        self.nature = Nature()

    def wma(self):
        fig1 = plt.figure(1)
        plt.xlabel('Time')
        plt.ylabel('Avg Regret')
        fig2 = plt.figure(2)
        plt.xlabel('Expert Loss')
        plt.ylabel('Online Learner Loss')
        color=['ro','go','bo']
        legend=['Always Yes','Always No','Alternate']
        x = self.expert.get_x(0)
        w = np.ones(len(x))
        eta = 0.1
        learner_loss = 0
        expert_loss = np.zeros(len(x))
        for t in range(100):
            xt = self.expert.get_x(t)
            yt_hat = -1 if sum(i[0]*i[1] for i in zip(w,xt)) <= 0 else 1
            yt = self.nature.get_stoch_y()
            #yt = self.nature.get_determ_y(t)
            #yt = self.nature.get_adver_y(xt, w)
            learner_loss = learner_loss + (0 if yt == yt_hat else 1)
            for i in range(len(xt)):
                expert_loss[i] = expert_loss[i] + (0 if yt == xt[i] else 1)
                w[i] = w[i]*(1 - eta * (0 if yt == xt[i] else 1))
                plt.figure(2)
                """Plot legend only for first time"""
                if t==0:
                    plt.plot(expert_loss[i], learner_loss, color[i],
                         label=legend[i])
                else:
                    plt.plot(expert_loss[i], learner_loss, color[i])
            print "xt=" + str(xt) + " yt=" + str(yt) +  " yt_hat=" + \
                    str(yt_hat) + " w=" + str(w) + " ll=" + str(learner_loss)
            plt.figure(1)
            plt.plot(t, (learner_loss - min(expert_loss))/(t+1), 'ro')
        fig1.show()
        plt.figure(2)
        plt.legend(loc='upper left')
        fig2.show()
        raw_input()

    def rwma(self):
        fig1 = plt.figure(1)
        plt.xlabel('Time')
        plt.ylabel('Avg Regret')
        fig2 = plt.figure(2)
        plt.xlabel('Expert Loss')
        plt.ylabel('Online Learner Loss')
        color=['ro','go','bo']
        legend=['Always Yes','Always No','Alternate']
        x = self.expert.get_x(0)
        w = np.ones(len(x))
        eta = 0.4
        learner_loss = 0
        expert_loss = np.zeros(len(x))
        for t in range(100):
            xt = self.expert.get_x(t)
            """Roulette Wheel"""
            rand_no = random.random()
            norm_w = math.sqrt(sum([i*i for i in w]))
            cum_prob = 0
            for i in range(len(xt)):
                cum_prob = cum_prob + w[i]/norm_w
                if rand_no <= cum_prob:
                    yt_hat = xt[i]
            yt = self.nature.get_stoch_y()
            #yt = self.nature.get_determ_y(t)
            #yt = self.nature.get_adver_y(xt, w)
            learner_loss = learner_loss + (0 if yt == yt_hat else 1)
            for i in range(len(xt)):
                expert_loss[i] = expert_loss[i] + (0 if yt == xt[i] else 1)
                w[i] = w[i]*(1 - eta * (0 if yt == xt[i] else 1))
                plt.figure(2)
                """Plot legend only for first time"""
                if t==0:
                    plt.plot(expert_loss[i], learner_loss, color[i],
                         label=legend[i])
                else:
                    plt.plot(expert_loss[i], learner_loss, color[i])
            print "xt=" + str(xt) + " yt=" + str(yt) +  " yt_hat=" + \
                    str(yt_hat) + " w=" + str(w) + " ll=" + str(learner_loss) + " el=" + str(expert_loss)
            plt.figure(1)
            plt.plot(t,(learner_loss - min(expert_loss))/(t+1),'ro')
        fig1.show()
        plt.figure(2)
        plt.legend(loc='upper left')
        fig2.show()
        raw_input()

def main():
    algorithm = Algorithm()
    #algorithm.wma()
    algorithm.rwma()

if __name__ == "__main__":
    main()
