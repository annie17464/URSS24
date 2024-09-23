from pulp import LpMaximize, LpMinimize, LpProblem, LpVariable, lpSum, PULP_CBC_CMD, LpStatus
import numpy as np

class WBbM:
    """Weighted Bipartite b-Matching (WBbM) algorithm"""
    def __init__(self, num_left, num_right, W, lda, uda, ldp, udp, LogToConsole=0):
        self.num_left = num_left
        self.num_right = num_right
        self.W = W
        self.lda = lda
        self.uda = uda
        self.ldp = ldp
        self.udp = udp
        self.LogToConsole = LogToConsole

    def linkmatr(self, num_left, num_right):
        """ Creates link matrix A for constraint satisfaction """
        num_nodes = self.num_left + self.num_right
        str1 = [1] * self.num_right
        str2 = [0] * self.num_right
        A = [None] * num_nodes
        for i in range(self.num_left):
            A[i] = str2 * self.num_left
            idx = self.num_right * i
            A[i][idx:idx + self.num_right] = str1
        for j in range(self.num_right):
            A[self.num_left + j] = str2 * self.num_left
            idx = [j + self.num_right * l for l in range(self.num_left)]
            for k in range(self.num_left):
                A[self.num_left + j][idx[k]] = 1      
        return A
    
    def Bb_matching(self, optimization_mode="max"):
        """ Solves the matching problem """
        if optimization_mode not in ["max", "min"]:
            raise ValueError("Optimization mode not recognized.")
        
        if optimization_mode == "max":
            m = LpProblem(name="naisc_matching", sense=LpMaximize)
        else:
            m = LpProblem(name="naisc_matching", sense=LpMinimize)

        total_nodes = self.num_left + self.num_right
        total_vars = self.num_left * self.num_right
        
        ''''if (self.num_left * self.lda > self.num_right * self.udp) or (self.num_right * self.ldp > self.num_left * self.uda):
            raise Exception("Infeasible Problem")'''
        
        # Maximum Number of authors matched to node paper
        if isinstance(self.udp, int):
            Dmax = [self.udp]* total_nodes
        elif isinstance(self.udp, list):
            Dmax = [0] * self.num_left + self.udp
        else:
            raise Exception("udp value not correct.")
        
        # Minimum Number of authors matched to a paper
        Dmin = [self.ldp] * total_nodes
        
        # Minimum Number of papers matched to an author
        Dmina = [self.lda] * total_nodes
        
        # Maximum number of papers matched to author
        if isinstance(self.uda, int):
            Dmaxa = [1] * total_nodes
        elif isinstance(self.uda, list):
            Dmaxa = self.uda
        else:
            raise Exception("uda value not correct.")
        
        A = self.linkmatr(self.num_left, self.num_right)
        
        x = [LpVariable(f"x{j}", cat="Binary") for j in range(total_vars)]
        
        # objective
        if optimization_mode == "max":
            m += lpSum(self.W[i] * x[i] for i in range(total_vars))
        else:
            m += lpSum(self.W[i] * x[i] for i in range(total_vars))
        
        # constraint on paper cardinality
        for i in range(self.num_left, total_nodes):
            m += lpSum(A[i][j] * x[j] for j in range(total_vars)) <= Dmax[i]
            m += lpSum(A[i][j] * x[j] for j in range(total_vars)) >= Dmin[i]
                
        # constraint on authors
        for i in range(self.num_left):
            m += lpSum(A[i][j] * x[j] for j in range(total_vars)) <= Dmaxa[i]
            m += lpSum(A[i][j] * x[j] for j in range(total_vars)) >= Dmina[i]
        
        m.solve(PULP_CBC_CMD(msg=self.LogToConsole))
        
        res = np.zeros((self.num_left, self.num_right), dtype=int)
        for i in range(self.num_left):
            for j in range(self.num_right):
                idx = self.num_right * i + j
                res[i, j] = x[idx].varValue
           
        status = LpStatus[m.status]
        if status == "Unbounded":
            print('The model cannot be solved because it is unbounded')
        elif status == "Optimal":
            print('The optimal objective is %g' % m.objective.value())
        elif status not in ["Infeasible", "Unbounded"]:
            print('Optimization was stopped with status %d' % status)
            
        return res, m.objective.value()

# The output is formatted in the following manner: 

'''num_left = 6
num_right = 8
W = np.random.rand(num_left * num_right)
lda, uda, ldp, udp = 1, 1, 0, [2, 2, 2, 1, 1, 1, 1, 1]
model = WBbM(num_left, num_right, W, lda, uda, ldp, udp)
result, objective = model.Bb_matching(optimization_mode="max")

# Print results
print(W)
print("Matching result matrix:")
print(result)
print("Optimal objective value:")
print(objective)'''