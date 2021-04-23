def recursive_change(money, coins):
    if money == 0:
        return 0
    min_num_coins = 1000000000
    for i in range(len(coins)):
        if money >= coins[i]:
            num_coins = recursive_change(money - coins[i], coins)
            if num_coins + 1 < min_num_coins:
                min_num_coins = num_coins + 1
    return min_num_coins

def dp_change(money, coins):
    min_num_coins = {0: 0}
    for i in range(1, money + 1):
        min_num_coins[i] = 9999999999
        for j in range(len(coins)):
            if i >= coins[j]:
                if min_num_coins[i - coins[j]] + 1 < min_num_coins[i]:
                    min_num_coins[i] = min_num_coins[i - coins[j]] + 1
    return min_num_coins[money]

money = 25
coins = [1,3,5,13,17]
print(dp_change(money, coins))