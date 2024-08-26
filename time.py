import csv
from datetime import datetime

# 定义CSV文件路径和输出文件路径
file_path = r'C:\Users\裕龙\Desktop\汽车销售数据.csv'
output_file_path = r'C:\Users\裕龙\Desktop\output.txt'

# 观测窗口结束期
current_date = datetime.now()

# 定义将天数转换为X年X天的函数
def days_to_years_days(days):
    years = days // 365
    remaining_days = days % 365
    return f"{years}年{remaining_days}天"

# 处理数据并写入结果到文件
try:
    with open(file_path, mode='r') as file, \
         open(output_file_path, mode='w', encoding='utf-8') as output_file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                # 将“上牌时间”转换为datetime对象
                registration_date_str = row['上牌时间'] + '-01'
                registration_date = datetime.strptime(registration_date_str, '%Y年%m月-%d')
            except KeyError:
                print(f"列名错误: 找不到'上牌时间'列")
                continue
            except ValueError:
                print(f"日期格式错误: 无法解析日期'{registration_date_str}'")
                continue

            # 过滤2020年下半年的数据
            if datetime(2020, 7, 1) <= registration_date <= datetime(2020, 12, 31):
                # 计算上牌时间到当前时间的天数间隔
                days_interval = (current_date - registration_date).days
                # 转换天数为年和天的格式
                interval_str = days_to_years_days(days_interval)
                # 写入结果到文件
                output_file.write(f"汽车名称: {row['名称']}, 上牌时间: {row['上牌时间']}, 时间间隔: {interval_str}\n")
except Exception as e:
    print(f"发生错误: {e}")