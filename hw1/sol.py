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

class NatureWithObs:
    def get_observation(self):
        return [-1 if random.random() <= 0.5 else 1,
                -1 if random.random() <= 0.5 else 1]
    """Observation = [Weather, Location]
       Weather: 0=bad 1=good
       Location: 0=away 1=home
    """
    def get_stoch_y(self, observations):
        yt = self.get_determ_y(observations)
        if random.random() <= 0.5:
            return 1 if yt == -1 else 1
        else:
            return yt

    def get_determ_y(self, observations):
        if observations[0]==0 and observations[1]==0:
            yt=-1
        elif observations[0]==1 and observations[1]==0:
            yt=-1
        elif observations[0]==0 and observations[1]==1:
            yt=1
        else:
            yt=1
        return yt

    def get_adver_y(self, xt, w):
        """Send aversarial output"""
        yt_hat = 1 if sum(i[0]*i[1] for i in zip(w,xt)) <= 0 else -1
        return yt_hat

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
        """One Obervation Expert"""
        if observations[0]==1:
            yt_hat=1
        else:
            yt_hat=-1
        return yt_hat

    def get_expert_five_advice(self, t, observations):
        if observations[0]==0 and observations[1]==0:
            yt_hat=-1
        elif observations[0]==1 and observations[1]==0:
            yt_hat=-1
        elif observations[0]==0 and observations[1]==1:
            yt_hat=-1
        else:
            yt_hat=1
        return yt_hat

    def get_x(self, t):
        return (self.get_expert_one_advice(),
                self.get_expert_two_advice(),
                self.get_expert_three_advice(t))

    def get_x_with_obs(self, t, observations):
        return (self.get_expert_one_advice(),
                self.get_expert_two_advice(),
                self.get_expert_three_advice(t),
                self.get_expert_four_advice(t, observations),
                self.get_expert_five_advice(t, observations))

class Algorithm:
    def __init__(self):
        self.expert = Expert()
        self.nature = Nature()
        self.nature_with_obs = NatureWithObs()

    def wma(self, use_obs=0):
        fig1 = plt.figure(1)
        plt.xlabel('Time')
        plt.ylabel('Avg Regret')
        fig2 = plt.figure(2)
        plt.xlabel('Expert Loss')
        plt.ylabel('Online Learner Loss')
        color=['ro-','go-','bo-','yo-','mo-','co-']
        legend=['Always Yes','Always No','Alternate','Obs1','Obs2','Policy']
        if use_obs == 0:
            x = self.expert.get_x(0)
        else:
            observations = self.nature_with_obs.get_observation()
            x = self.expert.get_x_with_obs(0, observations)
        w = np.ones(len(x))
        eta = 0.1
        learner_loss = 0
        expert_loss = np.zeros(len(x))
        for t in range(100):
            if use_obs == 0:
                xt = self.expert.get_x(t)
                #yt = self.nature.get_stoch_y()
                #yt = self.nature.get_determ_y(t)
                yt = self.nature.get_adver_y(xt, w)
            else:
                observations = self.nature_with_obs.get_observation()
                xt = self.expert.get_x_with_obs(t, observations)
                #yt = self.nature_with_obs.get_stoch_y(observations)
                #yt = self.nature_with_obs.get_determ_y(observations)
                yt = self.nature_with_obs.get_adver_y(xt, w)

            yt_hat = -1 if sum(i[0]*i[1] for i in zip(w,xt)) <= 0 else 1
            learner_loss = learner_loss + (0 if yt == yt_hat else 1)
            for i in range(len(xt)):
                expert_loss[i] = expert_loss[i] + (0 if yt == xt[i] else 1)
                w[i] = w[i]*(1 - eta * (0 if yt == xt[i] else 1))
                plt.figure(2)
                """Plot legend only for first time"""
                if t==0:
                    plt.plot(expert_loss[i], learner_loss, color[i],
                         label=legend[i])
                    if i==len(xt)-1:
                        plt.plot(t, learner_loss, color[-1], label="Policy")
                else:
                    plt.plot(t,expert_loss[i], color[i])
                print "xt=" + str(xt) + " yt=" + str(yt) +  " yt_hat=" + \
                    str(yt_hat) + " w=" + str(w) + " ll=" + str(learner_loss) + " el=" + str(expert_loss)
                plt.plot(t, learner_loss, color[-1])
            plt.figure(1)
            plt.plot(t, (learner_loss - min(expert_loss))/(t+1), 'ro-')
        fig1.show()
        plt.figure(2)
        plt.legend(loc='upper left')
        fig2.show()
        raw_input()

    def rwma(self, use_obs=0):
        fig1 = plt.figure(1)
        plt.xlabel('Time')
        plt.ylabel('Avg Regret')
        fig2 = plt.figure(2)
        plt.xlabel('Expert Loss')
        plt.ylabel('Online Learner Loss')
        color=['ro-','go-','bo-','yo-','mo-','co-']
        legend=['Always Yes','Always No','Alternate','Obs1','Obs2','Policy']
        if use_obs == 0:
            x = self.expert.get_x(0)
        else:
            observations = self.nature_with_obs.get_observation()
            x = self.expert.get_x_with_obs(0, observations)
        w = np.ones(len(x))
        eta = 0.1
        learner_loss = 0
        expert_loss = np.zeros(len(x))
        for t in range(100):
            eta = 1/math.sqrt(t+1)
            if use_obs == 0:
                xt = self.expert.get_x(t)
                #yt = self.nature.get_stoch_y()
                #yt = self.nature.get_determ_y(t)
                yt = self.nature.get_adver_y(xt, w)
            else:
                observations = self.nature_with_obs.get_observation()
                xt = self.expert.get_x_with_obs(t, observations)
                #yt = self.nature_with_obs.get_stoch_y(observations)
                #yt = self.nature_with_obs.get_determ_y(observations)
                yt = self.nature_with_obs.get_adver_y(xt, w)
            rand_no = random.random()
            norm_w = math.sqrt(sum([i*i for i in w]))
            cum_prob = 0
            for i in range(len(xt)):
                cum_prob = cum_prob + w[i]/norm_w
                if rand_no <= cum_prob:
                    yt_hat = xt[i]
            learner_loss = learner_loss + (0 if yt == yt_hat else 1)
            for i in range(len(xt)):
                expert_loss[i] = expert_loss[i] + (0 if yt == xt[i] else 1)
                w[i] = w[i]*(1 - eta * (0 if yt == xt[i] else 1))
                plt.figure(2)
                """Plot legend only for first time"""
                if t==0:
                    plt.plot(expert_loss[i], learner_loss, color[i],
                         label=legend[i])
                    if i==len(xt)-1:
                        plt.plot(t, learner_loss, color[-1], label="Policy")
                else:
                    plt.plot(t,expert_loss[i], color[i])
                print "xt=" + str(xt) + " yt=" + str(yt) +  " yt_hat=" + \
                    str(yt_hat) + " w=" + str(w) + " ll=" + str(learner_loss) + " el=" + str(expert_loss)
                plt.plot(t, learner_loss, color[-1])
            plt.figure(1)
            plt.plot(t, (learner_loss - min(expert_loss))/(t+1), 'ro-')
        fig1.show()
        plt.figure(2)
        plt.legend(loc='upper left')
        fig2.show()
        raw_input()

def main():
    algorithm = Algorithm()
    # 1 = with Observation
    # 0 = without Observation
    # select stoch/determ/adver by uncommenting relevant lines in the functions wma/rwma
    algorithm.wma(0)
    #algorithm.wma(1)
    #algorithm.rwma(0)

if __name__ == "__main__":
    main()
