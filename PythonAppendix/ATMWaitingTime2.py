# File name: ATMWaitingTime2.py
# -----------------------------
# 对于ATMWaitingTime.py的修改，尝试缩短客户的等待时间

import random
from ATMWaitingTime import ATM, Customer

customer = Customer(5000)
atm = ATM()
waiting_list = list()
waiting_time = 0
cur_time = 0
cur_time += customer.getNextArrvTime()
waiting_list.append(cur_time)

# 假设每一位客户对ATM的平均操作时间为1
avgServCompleteTime = 1


# 用来预估当前队伍中前n-1人对ATM操作的总时间
def getTotalServCompleteTime(waiting_list, avgServCompleteTime):
    return (len(waiting_list) - 1) * avgServCompleteTime


while len(waiting_list) != 0 or not customer.isOver():
    # 如果当前有客户正在银行排队，则让第一位排队客户去操作ATM
    if waiting_list[0] <= cur_time:
        next_time = atm.getServCompleteTime(cur_time)
        del waiting_list[0]
    # 如果没有客户在银行排队，那么每次向前1个单位时间
    else:
        next_time = cur_time + 1

    # 如果当前没有客户在银行排队但还有剩余客户，那么通知客户来银行
    if not customer.isOver() and len(waiting_list) == 0:
        next_arrv = customer.getNextArrvTime(cur_time)
        waiting_list.append(next_arrv)

    # 预估现在处于队伍中的前n-1人对ATM的操作时间
    totalServCompleteTime = getTotalServCompleteTime(waiting_list, avgServCompleteTime)

    # 当还有剩余客户并且
    # 队伍中最后一位客户的到达时间处在当前ATM使用时间加上队伍前n-2个人对ATM的使用时间
    # 和当前ATM使用时间加上队伍前n-1个人对ATM的使用时间之间才会通知下一位客户来银行
    # 这样做可以缩短客户的等待时间，但是会加长ATM的空闲时间
    if not customer.isOver() and\
         next_time + totalServCompleteTime - avgServCompleteTime <= waiting_list[-1]\
              < next_time + totalServCompleteTime:
        next_arrv = customer.getNextArrvTime(waiting_list[-1])
        waiting_list.append(next_arrv)
        totalServCompleteTime += avgServCompleteTime
        while next_time + totalServCompleteTime - avgServCompleteTime\
             <= next_arrv < next_time + totalServCompleteTime and not customer.isOver():
            next_arrv = customer.getNextArrvTime(next_arrv)
            waiting_list.append(next_arrv)
            totalServCompleteTime += avgServCompleteTime

    # 统计客户排队时间
    for i in waiting_list:
        if i <= cur_time:
            waiting_time += next_time - cur_time
        elif cur_time < i < next_time:
            waiting_time += next_time - i
        else:
            pass

    # 更新时间，准备下一轮循环
    cur_time = next_time

# 通过比较可以发现，第二种做法可以缩短客户等待时间，但会加长银行总的工作时间
print(f'ATMWaitingTime2 >>> avg wating time={waiting_time / customer.count}')
print(f'ATMWaitingTime2 >>> total working time={cur_time}')
