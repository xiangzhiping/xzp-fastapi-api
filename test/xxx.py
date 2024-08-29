x = "images/<ZQz6i6H8RU94u7BAHpRmWt>-屏幕截图 2023-06-30 174607.png"

# 查找最后一个 '.' 的位置
last_dot_index = x.rfind('.')
print("Last dot index:", last_dot_index)

# 如果找到了 '.', 则截取从 '.' 开始到最后的子串
if last_dot_index != -1:
    extension = x[last_dot_index:]
    print("Extension:", extension)
else:
    print("No '.' found in the string.")
