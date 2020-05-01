# Python数据结构：数组和列表

import array  # Python提供较原始的array类

# array的创建
int_arr = array.array('i', [1, 2, 3])
str_arr = array.array('u', 'hello')

# 所有的类型创建码
print(array.typecodes)

# array的方法和list基本相同，例如append，pop，insert，remove， index等
# 但array还有一些特殊的功能。

arr = array.array('i', [1, 2, 3])

# Method: tolist()
# Usage: array.tolist()
# ---------------------
# 根据array的元素返回一个列表

lis = arr.tolist()

# Method: fromlist()
# Usage: array.fromlist()
# -----------------------
# 在array末尾附加列表中的元素
arr0 = array.array('i')
arr0.fromlist(lis)

# Method: tobytes()
# Usage: array.tobytes()
# ----------------------
# 将array转化为一个字节对象

print(arr)
arr_byte = arr.tobytes()
print(f'arr_byte={arr_byte}')
print(f'Type of arr_byte={type(arr_byte)}')

# Method: frombytes()
# Usage: array.frombytes(b)
# -------------------------
# 将字节对象还原成array
# 在array末尾附加转换后的字节对象

arr1 = array.array('i')
arr1.frombytes(arr_byte)
print(f'arr1={arr1}')

# Method: tofile()
# Usage: array.tofile(f)
# ----------------------
# 将所有的元素作为bytes写入f

with open('arr.bin', 'wb') as f: # 以二进制的方式打开文本
    arr.tofile(f)

# Method: fromfile()
# Usage: array.fromfile(f, n)
# ---------------------------
# 读取文件f中的前n个元素到array中
# n超过界限就会报错：
# EOFError: read() didn't return enough bytes

arr2 = array.array('i')
with open('arr.bin', 'rb') as f:
    arr2.fromfile(f, 3)
print(arr2)
