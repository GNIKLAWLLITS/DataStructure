# 如何计算某一天是星期几？
# [参考：https://www.cnblogs.com/faterazer/p/11393521.html]
#
# 以2004年5月1日为例，已知该日为星期六
# 1. 首先，我们有一个最基本的思路，要想知道给定日期是星期几
#    就必须找到一个基准日期，从这个基准日期开始推算。(巧合的是，
#    根据反推，公元元年的前一年（公元0年）12月31日恰好是一
#    个星期日，所以我们可以将基准日期定为 0000/12/31)
#
# 2. 然后就算出给定日期和基准日期的天数差，这个天数差除以7
#    所得的余数是几就是星期几。而这个天数差由两部分构成，
#    给定日期到基准日期之间所有的完整年的全部天数和最后的
#    非完整年的全部天数。
#
# 3. 需要注意闰年，规定公历年份是4的倍数的，且不是100的倍数，
#    为普通闰年（例如：2004）。公历年份是整百数的，必须是
#    400的倍数才是世纪闰年（例如：2000）。每当遇到一个闰年，
#    我们就给当年的总天数加1。


# 公式为：W= (Y-1)*365 + [(Y-1)/4] - [(Y-1)/100] + [(Y-1)/400] + D
def dayOfWeek1(day, month, year):
    W = ((year-1) * 365\
        + (year-1) // 4 - (year-1) // 100 + (year-1) // 400\
        + (31+29+31+30+1))
    return (W%7 - 1)


# 4. 但是我们注意到在dayOfWeek1中，求出来的W很大,
#    主要是因为第一项(Y-1)*365很大，使用起来也不方便。
#    因为最终要得到W除以7的余数，所以我们可以考虑先来
#    化简一下(Y-1)*365，只要找到一个和(Y-1)*365模7
#    同余的数就可以
#    因为(Y-1)*365 = 52*7*(Y-1) + (Y-1)
#    所以(Y-1)*365可以替换为(Y-1)
#
# 5. 除此之外，D的具体数值也很难求，在第一个函数中我们手动
#    算出了D的大小，现在我们想要使用一个公式来自动求出D。
#
#    首先我们可以列出月份和天数之间的对应关系：
#       月份: 1   2      3   4   5   6   7   8   9   10  11  12
#       天数: 31  28/29  31  30  31  30  31  31  30  31  30  31
#    因为所有的天数都大于28，将所有天数都减去28也不会影响结果
#        月       份: 1   2      3   4   5   6   7   8   9   10  11  12
#        天       数: 3   0/1    3   2   3   2   3   3   2   3   2   3
#        平年累计天数: 3    3     6   8   11  13  16  19  21  24  26  29
#        闰年累计天数: 3    4     7   9   12  14  17  20  22  25  27  30
#    通过观察发现除去1，2月，从3-7，从8-12的天数都满足3-2-3-2-3
#    这一规律，且每5个月增加13天。所以我们可以使用f(x) = (13//5)*x
#    来模拟。最终求得D的表达式：
#        | d                                  (m=1)
#    D = | 31 + d                             (m=2)
#        | 13*(m+1)//5 - 7 + (m-1)*28 + d + i (m>=3)
#    (m-1)*28是我们之前减去的天数；如果是润年，i=1，否则i=0
#
# 6. 这个时候我们可以发现，如果按照之前的规律，12月之后的一个月的天数
#    也应该是3，而1月正好是3。所以我们可以将1，2月视作前一年的13，14
#    月。这样不但延续了日期变换的规律，而且将2月份移到了每一年的末尾，
#    省去了我们判断平闰年的麻烦。D就变成了：
#        | d                               (m=1)
#    D = | 31 + d                          (m=2)
#        | 13*(m+1)//5 - 7 + (m-1)*28 + d  (14>=m>=3)
#
# 7. 当我们将每一年的1，2月看做前一年的13，14月时，判断闰年的函数也
#    需要改变一下。
#    比如说之前0000.12.31-0002.5.1可以表示为：
#               |---------------|---------|
#              0000.12.31   0001.12.31   0002.5.1
#    这一时间段总共跨越了2年（0001年一整年和0002年的一部分）
#    现在变成了：
#                  0000.14.29     0001.14.28
#               |-----|---------|----|----|
#               |               |         |
#            0000.12.31     0001.12.31   0002.5.1
#    这一时间段现在跨越了3年（0000年的一部分，0001年的一整年和0002年的一部分）
#    因此计算闰年的部分需要改为 [(Y)/4] - [(Y)/100] + [(Y)/400]


# 新的公式为：W = (Y-1) + [(Y)/4] - [(Y)/100] + [(Y)/400] + 13*(m+1)//5 - 7 + d
# 这个公式也是我们最常用的时间转换公式
def dayOfWeek2(day, month, year):
    if month < 3:
        month = month + 12
        year -= 1

    W = (year-1)\
        + (year//4) - (year//100) + (year//400)\
        + 13*(month+1)//5 - 7\
        + day

    return (W%7 - 1)


# 上述公式还不是最简练的形式，我们还可以继续对年份进行化简
# TODO


def test(day, month, year):
    dayOfWeekName = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
    week = dayOfWeek1(day, month, year)
    week = dayOfWeek2(day, month, year)
    print(dayOfWeekName[week])


if __name__ == '__main__':
    test(1, 5, 2004)