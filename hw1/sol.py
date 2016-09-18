class Nature:
    def get_stoch_output():
        """Send random y"""
    def get_determ_output():
        """Send deterministic y"""
    def get_adver_output():
        """Send aversarial output"""

class Expert:
    def get_expert_one_advice(xt):

    def get_expert_two_advice(xt):

    def get_expert_three_advice(xt):

    def get_x(xt):
        return (get_expert_one_advice(xt),
                get_expert_two_advice(xt),
                get_expert_three_advice(xt))


