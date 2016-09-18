import random

class Nature:
    def get_stoch_y(self):
        """Send random y"""
        return -1 if random.random() <= 0.5 else 1
    def get_determ_y(self,t):
        """Send deterministic y"""
        return -1 if t%2==1 else 1
    def get_adver_y(self,t):
        """Send aversarial output"""
        return -1 if t%2==0 else 1

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

    def get_x(self, t):
        return (self.get_expert_one_advice(),
                self.get_expert_two_advice(),
                self.get_expert_three_advice(t))

class Algorithm:
    def __init__(self):
        self.expert = Expert()
        self.nature = Nature()

    def wma(self):
        self.regret = [0,0,0]
        w = [1.0,1.0,1.0]
        eta = 0.4
        for t in range(10):
            xt = self.expert.get_x(t)
            yt_hat = -1 if sum(i[0]*i[1] for i in zip(w,xt)) <= 0 else 1
            yt = self.nature.get_determ_y(t)
            for i in range(len(xt)):
                w[i] = w[i]*(1 - eta * (0 if yt == xt[i] else 1))
                self.regret[i] = self.regret[i] + (0 if yt == yt_hat else 1) - (0 if yt == xt[i] else 1)
            print "xt=" + str(xt) + " yt=" + str(yt) +  " yt_hat=" + str(yt_hat) + " w=" + str(w)

def main():
    algorithm = Algorithm()
    algorithm.wma()
    print algorithm.regret

if __name__ == "__main__":
    main()
