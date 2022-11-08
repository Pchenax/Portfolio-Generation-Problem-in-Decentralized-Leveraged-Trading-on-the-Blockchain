import numpy as np
import copy
import matplotlib.pyplot as plt
import random


class Leveraged:
    def __init__(self):
        pass

    def set_paras(self, n, L, F):
        self.n = n
        self.L = L
        self.F = F
        self.td = L * F
        self.tb = (L - 1) * F
        self.td = int(L * F + 0.5)
        self.tb = int((L - 1) * F + 0.5)
        if self.td - self.tb != self.F:
            breakpoint()

    def set_data(self, m, da, ba):
        self.m = m
        self.da = da
        self.ba = ba

    def dp(self):
        dp_cost = [[[float('inf') for k in range(self.tb + 1)] for j in range(self.td + 1)] for i in range(self.n)]
        dp_detail = [[[[[0 for d in range(self.n)], [0 for b in range(self.n)]] for k in range(self.tb + 1)] for j in range(self.td + 1)] for i in range(self.n)]

        for j in range(self.td + 1):
            for k in range(self.tb + 1):
                if j / self.m[0] >= k:
                    dp_cost[0][j][k] = k * self.ba[0] - j * self.da[0]
                    dp_detail[0][j][k][0][0] += j
                    dp_detail[0][j][k][1][0] += k

        for i in range(1, self.n):
            for j in range(self.td + 1):
                for k in range(min(int(j // self.m[i]) + 1, self.tb + 1)):
                    if j == 0 and k == 0:
                        dp_cost[i][j][k] = 0
                        continue

                    all_available = (k == 0) or (j / k >= min(self.m[0:i + 1]))

                    minimum = float("inf")
                    for pre_j in range(j + 1):
                        for pre_k in range(k + 1):
                            if dp_detail[i - 1][pre_j][pre_k][0][i] + (j - pre_j) // self.m[i] >= dp_detail[i - 1][pre_j][pre_k][1][i] + (k - pre_k):
                                cost = dp_cost[i - 1][pre_j][pre_k] - self.da[i] * (j - pre_j) + self.ba[i] * (k - pre_k)
                                if cost < minimum:
                                    minimum = cost
                                    dp_cost[i][j][k] = minimum
                                    dp_detail[i][j][k] = copy.deepcopy(dp_detail[i - 1][pre_j][pre_k])
                                    dp_detail[i][j][k][0][i] += j - pre_j
                                    dp_detail[i][j][k][1][i] += k - pre_k

                    if all_available:
                        if dp_cost[i][j][k] > 99999999:
                            breakpoint()

        print(f"dp alg, cost={dp_cost[self.n - 1][self.td][self.tb]}, detail={dp_detail[self.n - 1][self.td][self.tb]}")
        return dp_cost[self.n - 1][self.td][self.tb]

    def greedy(self):
        dep = [0 for _ in range(self.n)]
        bor = [0 for _ in range(self.n)]
        min_cost = float("inf")
        for i in range(self.n):
            if self.td / self.m[i] >= self.tb:
                cost = self.ba[i] * self.tb - self.da[i] * self.td
                if cost < min_cost:
                    min_cost = cost
                    min_idx = i
        dep[min_idx] = self.td
        bor[min_idx] = self.tb
        print(f"greedy alg, cost={min_cost}, detail={[dep, bor]}")
        return min_cost

    def algRandom(self, repeat=20):
        total_cost = 0
        for i in range(repeat):
            rank = [r for r in range(self.n)]
            random.shuffle(rank)
            for k in rank:
                if self.td / self.m[k] >= self.tb:
                    cost = self.ba[k] * self.tb - self.da[k] * self.td
                    break
            total_cost += cost
        print(f"random alg, avg cost={total_cost / repeat}")
        return total_cost / repeat

    def run(self):
        if self.L / (self.L - 1) < min(self.m):
            return -1, -1
        else:
            return self.algRandom(), self.greedy(), self.dp()

    def save(self):
        pass


if __name__ == "__main__":
    leveraged = Leveraged()
    F_init = 10
    leveraged.set_paras(n=5, L=2, F=F_init)
    leveraged.set_data(
        m=[1.7, 1.45, 1.3, 1.22, 1.21],
        da=[0, 0, 0, 0.08, 0.01],
        ba=[0.5, 2.25, 4, 3.95, 3.55])

    leverage = []
    random_list, greedy_list, dp_list = [], [], []
    for i in range(22, 45):
        leverage.append(i / 10)
        leveraged.set_paras(n=5, L=i / 10, F=F_init)
        random_, greedy, dp = leveraged.run()
        random_list.append(random_ / F_init)
        greedy_list.append(greedy / F_init)
        dp_list.append(dp / F_init)
        print(random_, greedy, dp)
        # leveraged.save()
    print(f"random list={random_list}")
    print(f"greedy list={greedy_list}")
    print(f"dp list2={dp_list}")
    print([100 * (1 - dp_list[i] / greedy_list[i]) for i in range(len(dp_list))])

    plt.plot(leverage, random_list, label="random")
    plt.plot(leverage, greedy_list, label="greedy")
    plt.plot(leverage, dp_list, label="dp")
    plt.xlabel("Leverage ratio")
    plt.ylabel("Average stability fee")
    plt.legend()
    plt.show()
