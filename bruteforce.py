import copy

n = 5
L = 2.5
Vinit = 10
td = int(L * Vinit)
tb = int((L - 1) * Vinit)

m = [1.7, 1.45, 1.3, 1.22, 1.21]
ba = [0.5, 2.25, 4, 3.95, 3.55]
da = [0, 0, 0, 0.08, 0.01]


def bf(tv, pn):
    all_list = []

    def recursion(value, product, l, idx):
        if product == 0:
            l[idx] = value
            all_list.append(copy.deepcopy(l))
            return
        for i in range(value + 1):
            l[idx] = i
            recursion(value - i, product - 1, l, idx + 1)

    l = [0 for i in range(0, pn)]
    recursion(tv, pn - 1, l, 0)
    return all_list


deposit_list = bf(tv=td, pn=5)
borrow_list = bf(tv=tb, pn=5)


def check_available(dep, bor, m):
    available = 1
    for i in range(len(dep)):
        if not dep[i] / m[i] >= bor[i]:
            available = 0
    return available


def bf_cost(dep, bor):
    return sum(ba[i] * bor[i] - da[i] * dep[i] for i in range(n))


minimum = float("inf")
for dep in deposit_list:
    for bor in borrow_list:
        if check_available(dep, bor, m):
            cost = bf_cost(dep, bor)
            if cost <= minimum:
                minimum = cost
                print(f"minimum cost={minimum}, dep={dep}, bor={bor}")

