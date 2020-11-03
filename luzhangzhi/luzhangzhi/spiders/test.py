import xlsxwriter


# 创建一个工作簿并添加一张工作表，当然工作表是可以命名的
workbook = xlsxwriter.Workbook("D:\Learn\\test.xlsx")
worksheet = workbook.add_worksheet()

# 下面是我们要插入的数据
expenses = (
    ['Rent', 1000],
    ['Gas',   100],
    ['Food',  300],
    ['Gym',    50],
)

# 从第一个单元格开始，行和列的索引均为0
row = 0
col = 0

# 迭代数据并逐行写入
for temp in expenses:
    worksheet.write_row("A1", temp)
    row += 1

workbook.close()
