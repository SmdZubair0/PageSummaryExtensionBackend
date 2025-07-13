# def solve(N, K, dx, dy, cx, cy, forbidden, dp):
#     if (cx, cy, N) in dp:
#         return dp[(cx, cy, N)]
#     if (cx, cy) in forbidden:
#         return 0
#     if N == 0:
#         return 1
    
#     ans = 0
#     for i in range(K):
#         ans = (ans + solve(N - 1, K, dx, dy, cx + dx[i], cy + dy[i], forbidden, dp)) % 998244353

#     dp[(cx, cy, N)] = ans
#     return ans
        
# def calc(N, M, K, dx, dy, X, Y):
#     forbidden = set(zip(X, Y))

#     return solve(N, K, dx, dy, 0, 0, forbidden, dict())

# print(calc(1, 1, 1, [2], [2], [2], [2]))
# print(calc(2, 2, 2, [1, 1], [1, 2], [2, 3], [1, 2]))
# print(calc(1, 3, 2, [1, 2], [3, 1], [1, 1, 1], [2, 1, 1]))



def min_cost(N, X, A):
    mod = 1000000007

    cost = sum(A)

    mod_map = {0: -1}
    s = 0

    prefix_sums = [0] * (N + 1)
    for i in range(N):
        prefix_sums[i + 1] = prefix_sums[i] + A[i]

    for i in range(N + 1):
        mod = prefix_sums[i] % X
        if mod in mod_map:
            j = mod_map[mod]
            ss = prefix_sums[i] - prefix_sums[j + 1]
            if ss > s:
                s = ss
        else:
            mod_map[mod] = i - 1
    return cost - s

# print(min_cost(2, 2, [1, 1]))
# print(min_cost(3, 2, [1, 1, 1]))
print(min_cost(4, 3, [2, 2, 3, 4]))