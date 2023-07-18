import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from demo_tcp_2_other_client import lat_lon_to_xz
from math import radians, tan




# 从txt文件读取数据
data = []

with open('output_meter.txt','r') as file:
    for line in file:
        line = line.strip()
        if line.startswith('[') and line.endswith(']'):
            line = line[1:-1]
            data.append(line.split(','))
data = np.array(data,dtype=float)
# 提取飞机种类、经度、纬度和高度数据
aircraft_types = data[:, 0].astype(int)
# longitude 经度
x_lo = data[:, 1]
# latutude 纬度
y_la = data[:, 2]
# x纬度，z经度
high = data[:,3]

# 获取飞机种类和颜色
unique_types = np.unique(aircraft_types)
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']  # 可自定义颜色

# 创建图形窗口
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')

# 绘制每个飞机的轨迹，使用不同颜色区分
for i, aircraft_type in enumerate(unique_types):
    mask = aircraft_types == aircraft_type
    ax.plot(x_lo[mask], y_la[mask],high[mask], color=colors[i % len(colors)], label='Aircraft Type {}'.format(aircraft_type))

# 设置坐标轴标签和标题
ax.set_xlabel('meter（Longitude）')
ax.set_ylabel('high')
ax.set_zlabel('meter（Latitude）')
ax.set_title('Aircraft Trajectories')

# 添加图例
ax.legend()

# 显示图形
plt.show()