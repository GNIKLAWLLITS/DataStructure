'''
Python数据结构：Date_ADT

Implements a proleptic Gregorian calendar date as a Julian day number.
Interfaces: 
+ Date(year, month, day): 创建一个 Date 实例并初始化成公历中的一天。西元前 1 年及之前的日期中的年部分用负数表示。
+ year(): 返回该公历日期的年。
+ month(): 返回该公历日期的月。
+ day(): 返回该公历日期的日。
+ monthName(): 返回该公历日期的月份名。
+ dayOfWeek(): 返回星期数，值为 [1-7]，0 表示星期一，6 表示星期日。
+ numDays(otherDate): 返回这两个日期间所差距的天数，是一个正整数。
+ isLeapYear(): 布尔值，检测该日期是否在一个闰年中。
+ advanceBy(days): 如果参数是正数，则返回的日期将增加这么多天，如果负数则减少，有必要的话，该日期将近似到西元前 4714 年的 12 月 24 日。
+ comparable(otherDate): 实现逻辑运算，如 &lt;, &lt;=, &gt;, &gt;=, ==, !==。
+ toString(): 返回 `yyyy-mm-dd` 形式的字符串表示。

公历中的一天和Julian day的转化公式：
T = (M - 14) / 12
jday = D - 32075 + (1461 * (Y + 4800 + T) / 4) +
                    (367 * (M - 2 - T * 12) / 12) -
                    (3 * ((Y + 4900 + T) / 100) / 4)
'''


class Date:
    def __init__(self, day, month, year):
        self._julianDay = 0
        assert self._isValidGregorian(day, month, year), 'Invalid Gregorian date'
        # Calaculate the correct Julian day
        # 换算成Julian Day主要是为了方便进行日期比较
        t = 0
        if month < 3:
            t = -1
        self._julianDay = day - 32075 + (1461 * (year+4800+t) // 4)\
                                      + (367 * (month -2 -t * 12) // 12)\
                                      - (3 * ((year + 4900 + t) // 100) // 4)

    def _isValidGregorian(self, day, month, year):

        # 需要考虑以下几点  1. 月份只能从1-12
        #                2. 天数只能从1-31
        #                3. 大小月
        #                4. 闰年的二月

        if month < 1 or month > 12:
            return False

        if day <= 0:
            return False

        months_31_days = [1, 3, 5, 7, 8, 10, 12]
        months_30_days = [4, 6, 9, 11]

        if month in months_31_days:   # 大月
            if day > 31:
                return False
        elif month in months_30_days: # 小月
            if day > 30:
                return False
        else:                         # 二月
            if self._leapYear(year):
                if day > 29:
                    return False
            else:
                if day > 28:
                    return False

        return True

    def _toGregorian(self):
        A = self._julianDay + 68569
        B = 4 * A // 146097
        A = A - (146097*B + 3) // 4
        year = 4000 * (A+1) // 1461001
        A = A - (1461*year//4) + 31
        month = 80 * A // 2447
        day = A - (2447*month//80)
        A = month // 11
        month = month + 2 - (12*A)
        year = 100 * (B-49) + year + A

        return (day, month, year)

    # Return the Gergorian year, month and day
    def year(self):
        return self._toGregorian()[2] # return Y from (Y, M, D)

    def month(self):
        return self._toGregorian()[1] # return M from (Y, M, D)

    def day(self):
        return self._toGregorian()[0] # return D from (Y, M, D)

    # Return the Gergotian month name
    def monthName(self):
        months = [
            "Jan",
            "Feb",
            "Mar",
            "Apr",
            "May",
            "Jun",
            "Jul",
            "Aug",
            "Sept",
            "Oct",
            "Nov",
            "Dec",
        ]
        return months[self.month() - 1]

    # Returns day of the week as an int between 0 (Mon) and 6 (Sun).
    def dayOfWeek(self):
        day, month, year = self._toGregorian()
        if month < 3:
            month = month + 12
            year -= 1

        W = (year-1)\
            + (year//4) - (year//100) + (year//400)\
            + 13*(month+1)//5 - 7\
            + day

        return (W%7 - 1)

    def dayOfWeekNmae(self):
        dayOfWeekNmae = ['Mon', 'Tue', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
        w = self.dayOfWeek()
        return dayOfWeekNmae[w]

    # Return number of days between two dates
    def numDays(self, otherDate):
        if self._julianDay > otherDate._julianDay:
            return self._julianDay - otherDate._julianDay
        else:
            return otherDate._julianDay - self._julianDay

    # Return if a year is a leap year
    def _leapYear(self, year):

        # 普通闰年：公历年份是4的倍数的，且不是100的倍数，为普通闰年（例如：2004）
        # 世纪闰年：公历年份是整百数的，必须是400的倍数才是世纪闰年（例如：2000）

        if year % 400 == 0 or (year % 4 == 0 and year % 100 != 0):
            return True
        return False

    def isLeapYear(self):
        return self._leapYear(self.year())

    # Return the advanced date
    def advanceBy(self, days):
        self._julianDay += days
        if self._julianDay < 0:
            self._julianDay = 0

    # Logically compare two dates
    def __eq__(self, otherDate):
        return self._julianDay == otherDate._julianDay

    def __lt__(self, otherDate):
        return self._julianDay < otherDate._julianDay

    def __le__(self, otherDate):
        return self._julianDay <= otherDate._julianDay

    # Return the date as a string in Gregorian format.
    def __str__(self):
        day, month, year = self._toGregorian()
        return "%04d-%02d-%02d" % (year, month, day)

    def __repr__(self):
        return str(self)


def test():
    date = Date(30, 4, 2020)
    print(f'Date: {date.__str__()}')
    print('The month is ' + date.monthName())
    print(f'{date.__str__()} is {date.dayOfWeekNmae()}')
    oldDate = Date(2, 1, 1)
    print(f'From {oldDate.__str__()} to now, {date.numDays(oldDate)} days have passed')
    if date.isLeapYear():
        print(f'{date.year()} is a leap year')
    else:
        print(f'{date.year()} is not a leap year')
    date.advanceBy(10)
    print(f'10 days later is {date.__str__()}, {date.dayOfWeekNmae()}')
    newDate = Date(29, 4, 2020)
    if date.__le__(newDate):
        print(f'{date.__str__()} <= {newDate.__str__()} ')
    else:
        print(f'{date.__str__()} > {newDate.__str__()} ')


if __name__ == '__main__':
    test()
