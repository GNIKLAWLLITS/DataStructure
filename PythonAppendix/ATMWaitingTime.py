# File name: ATMWaitingTime.py
# ----------------------------
# 需求分析：
# 假设银行有1台ATM机，共n位客户来银行操作ATM机器，求客户平均的排队等候时间。
#
# 逻辑梳理:
# ATM 机操作时间由客人选择的办理业务决定，符合随机分布。
# 客户流到达银行时间不定，符合随机分布。
# 累加每位客户排队等候的时间，再除以总客户数，即可得出客户的平均等候时间。
#
# 前提假设
# 实际应用中，ATM 机和客户流时间均为随机数，在本实例需做出一定条件限制以方便计算。
# ATM 机操作时间：1-5 分钟
# 下位客户到达时间：1-10 分钟
# 时间以整数为单位。
#
# 参考资料：https://blog.csdn.net/JannaSpeaking/article/details/83749585
#
# 问题：
# 对于ATM来说，这种做法保证了ATM的高使用率，提高了银行的效率
# 但是对于客户来说，增加了部分客户的等待时间。
# 在ATMWaitingTime2.py中尝试缩短客户等待时间

import random


class ATM:
    def __init__(self, maxtime=5):
        self.maxtime = maxtime

    # 返回每一次操作的时间
    def getServCompleteTime(self, start=0):
        return start + random.randint(1, self.maxtime)


class Customer:
    def __init__(self, num):
        self.count = num # 初始客户总数
        self.left = num  # 初始剩余客户数

    # 根据剩余客户情况，通知客户到银行，返回客户到银行所需要的时间，最大为10分钟
    def getNextArrvTime(self, start=0, arrvtime=10):
        if self.left != 0:
            self.left -= 1
            return start + random.randint(1, arrvtime)
        else:
            return 0

    # 检查剩余客户是否为0
    def isOver(self):
        return True if self.left == 0 else False


customer = Customer(5000)
atm = ATM()
# 等待列表，当客户到达银行后会被加入等待列表
waiting_list = list()
# 记录总的客户等待时间
waiting_time = 0
# 记录当前时间
cur_time = 0
# 将当前时间设为第一位客户到达时间
# 并将第一位客户添加到等待列表
cur_time += customer.getNextArrvTime()
waiting_list.append(cur_time)

# 当所有客户都已经来到银行，并且等待列表为空就退出循环
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

    # 如果当前还有剩余客户且等待列表中最后一位客户的到达时间早于ATM闲置时间，
    # 那么通知下一位客户来银行
    if not customer.isOver() and waiting_list[-1] < next_time:
        # 这里用的是最后一位客户的到达时间waiting_list[-1]而不是
        # 当前时间cur_time，其实很好理解，只有当最后一人已经达到，
        # 才能通知下一人
        next_arrv = customer.getNextArrvTime(waiting_list[-1])
        waiting_list.append(next_arrv)
        # 只要最新的客户到达时间仍早于ATM闲置时间，并且还有剩余客户
        # 就一直通知下一位客户来银行，这样可以防止ATM长时间处于闲置
        while next_arrv < next_time and not customer.isOver():
            next_arrv = customer.getNextArrvTime(next_arrv)
            waiting_list.append(next_arrv)

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

print(f'ATMWaitingTime >>> avg wating time={waiting_time / customer.count}')
print(f'ATMWaitingTime >>> total working time={cur_time}')