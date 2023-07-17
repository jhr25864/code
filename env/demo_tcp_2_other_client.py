from multifighters.simulation_env import CombatEnv
from multifighters.SimInput import FighterDataIn, print_outdata
# ========================
import socket
from threading import Thread
import threading
import time
import random
from math import radians, tan
# ========================

######################## tcp通信 by ybw ########################
server_addr = ('127.0.0.1', 9999)
tcp_cli_socket = socket.socket()
name = 'EnvDemo'


def msg_recv():
    """
    接收数据
    """
    while True:
        data = tcp_cli_socket.recv(1024)
        if data.decode("utf-8") == "exit":
            print('小飞机不玩了，一不小心退出了群聊！')
            tcp_cli_socket.close()
            break
        print(data.decode("utf-8"))


def msg_send(message):
    """
    发送数据
    """
    data_info = message
    if data_info == "exit":
        tcp_cli_socket.send(data_info.encode("utf-8"))
    else:
        tcp_cli_socket.send((data_info + ' -ta').encode("utf-8"))


def generate(message):
    msg_send(message)


def lat_lon_to_xz(latitude, longitude):
    # 地球半径，单位为千米
    EARTH_RADIUS = 6371.0

    # 将经纬度转换为弧度
    lat_rad = radians(latitude)
    lon_rad = radians(longitude)

    # 计算墨卡托投影的平面坐标
    x = EARTH_RADIUS * lon_rad
    z = EARTH_RADIUS * tan(lat_rad)

    return x, z
def start():
    """
    连接服务器
    """
    try:
        tcp_cli_socket.connect(server_addr)
    except Exception as e:
        print("小飞机还没找到组织，请重试！")
        tcp_cli_socket.close()
        print(e)
        return

    while True:
        tcp_cli_socket.send((name + ' -n').encode('utf-8'))
        data = tcp_cli_socket.recv(128).decode('utf-8')
        print(data)
        if data == "OK":
            print("小飞机加入了群聊！")
            break
        else:
            print(data)

    t = Thread(target=msg_recv)
    t.start()
    # t1 = Thread(target=msg_send)
    # t1.start()

def battle():
    # 初始化设定
    env = CombatEnv()
    datain = [FighterDataIn() for m in range(4)]
    ######################## 飞机设定控制模式为0或3 ###########################
    for i in range(4):
        datain[i].control_mode = 3

    # 完成初始化
    env.initial(datain)

    # 开始多轮仿真
    for i_episode in range(111):
        # 重置仿真
        outdata = env.reset()

        for t in range(12000):
            # 编辑输入控制数据
            #######################################################################
            # 直接控制模式的动作输入
            for i in range(4):
                if i == 0:
                    # 蓝0
                    datain[i].control_input = [1, 1 / 8, 0, 0]
                    datain[i].target_index = 0
                    datain[i].missile_fire = 1
                    datain[i].fire = 1
                    datain[i].communication = [b'0x0', b'0x0', b'0x0', b'0x0', b'0x0']
                if i == 1:
                    # 蓝1
                    datain[i].control_input = [1, 1 / 9, 0, 0]
                    datain[i].target_index = 1
                    datain[i].missile_fire = 1
                    datain[i].fire = 1
                    datain[i].communication = [b'0x1', b'0x1', b'0x1', b'0x1', b'0x1']
                if i == 2:
                    # 红2
                    datain[i].control_input = [1, 1 / 8, 0, 0]
                    datain[i].target_index = 0
                    datain[i].missile_fire = 1
                    datain[i].fire = 1
                if i == 3:
                    # 红3
                    datain[i].control_input = [1, 1 / 9, 0, 0]
                    datain[i].target_index = 2
                    datain[i].missile_fire = 1
                    datain[i].fire = 1
            ########################################################################

            # 回合更新
            outdata, terminal, blue_time_count, red_time_count = env.update(datain)

            # 打印数据
            # print('\n仿真步长', t)
            # print_outdata(outdata)
            ######################## tcp通信 by ybw ########################
            www = ''
            for i in range(4):
                x, z = lat_lon_to_xz(outdata[i].selfdata.Latitude, outdata[i].selfdata.Longitude)
                y = outdata[i].selfdata.Altitude
                pitch = outdata[i].selfdata.PitchAngle  # '\n| 俯仰角', '%10.5f' % data.selfdata.PitchAngle,
                roll = outdata[i].selfdata.RollAngle  # '| 滚转角', '%10.5f' % data.selfdata.RollAngle,
                yaw = outdata[i].selfdata.YawAngle  # '| 偏航角', '%10.0f' % data.selfdata.YawAngle,
                www = www + str(x) + ',' + str(y) + ',' + str(z) + ',' + str(pitch) + ',' + str(roll) + ',' + str(
                    yaw) + ';'
            msg_send(www)
            ######################## tcp通信 by ybw ########################
            # 仿真结束
            if terminal >= 0:
                print("Episode: \t{} ,episode len is: \t{}".format(i_episode, t))
                print(terminal, blue_time_count, red_time_count)
                break
###############################################################
if __name__ == '__main__':
    start()
    t1 = Thread(target=battle)
    t1.start()
