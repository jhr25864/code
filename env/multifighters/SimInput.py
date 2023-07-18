import numpy as np
import math
from math import radians, tan


fighter_str = '.\MultiFighter.dll'
missile_str = '.\CBB_py.dll'
txt_log_switch = True
log_match = False


# 用于生成可供读取的经纬高文件
a = []
b = []
output_file = open('output.txt','w')

class FighterDataIn(object):
    def __init__(self):
        # 飞机控制模式选择（仅可在初始化时进行一次选择）
        self.control_mode = 3

        # 直接控制输入,依据操作模式代表不同含义
        # 控制模式0：[油门， 期望机体法向过载， 期望机体滚转速率， 无意义补充位]
        # 控制模式3：[油门， 纵向杆， 横向杆， 方向舵]
        self.control_input = [1, 1/9, 0, 0]

        # 航炮开火指令，1为发射，0为不发射
        self.fire = 0

        # 机载雷达锁定目标，机载雷达中，0为不锁定，敌机编号分别为1、2
        self.target_index = 0

        # 导弹开火指令，1为发射，0为不发射
        self.missile_fire = 0

        # 通信链路
        self.communication = [b'0x0', b'0x0', b'0x0', b'0x0', b'0x0']


def print_outdata(outdata):
    for i in range(len(outdata)):
        if i == 0:
            print('__________________________________________________________________________________'
                  '__________________________________________________________________________________')
        if i != 0:
            print('\n')

        print_selfdata(i, outdata[i])
        print_radardata(i, outdata[i])
        print_statedata(i, outdata[i])
        print_closedata(i, outdata[i])
        print_alertdata(i, outdata[i])


def print_selfdata(i, data):
        print('| 编号', i,
              '| 控制模式', data.selfdata.control_mode,
              '| 剩余血量', '%10.3f' % data.selfdata.left_bloods,
              '| 剩余导弹', data.selfdata.left_missile,
              '| 剩余子弹', '%10.3f' % data.selfdata.left_bloods, '|',

              '\n| 北速度', '%10.5f' % data.selfdata.NorthVelocity,
              '| 东速度', '%10.5f' % data.selfdata.EastVelocity,
              '| 地速度', '%10.0f' % data.selfdata.VerticalVelocity,
              '| 北加速度', '%10.5f' % data.selfdata.NorthAcceleration,
              '| 东加速度', '%10.5f' % data.selfdata.EastAcceleration,
              '| 地加速度', '%10.0f' % data.selfdata.VerticalAcceleration, '|',

              '\n| 俯仰角', '%10.5f' % data.selfdata.PitchAngle,
              '| 滚转角', '%10.5f' % data.selfdata.RollAngle,
              '| 偏航角', '%10.0f' % data.selfdata.YawAngle,
              '| 俯仰角速度', '%10.5f' % data.selfdata.PitchRate,
              '| 滚转角速度', '%10.5f' % data.selfdata.RollRate,
              '| 偏航角速度', '%10.0f' % data.selfdata.YawRate, '|',

              '\n| 攻角', '%10.5f' % data.selfdata.AttackAngle,
              '| 侧滑角', '%10.5f' % data.selfdata.SideslipAngle,
              '| 经度', '%10.5f' % data.selfdata.Longitude,
              '| 纬度', '%10.5f' % data.selfdata.Latitude,
              '| 高度', '%10.0f' % data.selfdata.Altitude, '|',

              '\n| 体轴法向过载', '%10.5f' % data.selfdata.NormalLoad,
              '| 体轴侧向过载', '%10.5f' % data.selfdata.LateralLoad,
              '| 体轴纵向过载', '%10.5f' % data.selfdata.LongitudeinalLoad,
              '| 体轴法向速度', '%10.5f' % data.selfdata.NormalVelocity,
              '| 体轴侧向速度', '%10.5f' % data.selfdata.LateralVelocity,
              '| 体轴纵向速度', '%10.0f' % data.selfdata.LongitudianlVelocity, '|',

              '\n| 真空速', '%10.5f' % data.selfdata.TrueAirSpeed,
              '| 指示空速', '%10.5f' % data.selfdata.IndicatedAirSpeed,
              '| 地速', '%10.5f' % data.selfdata.GroundSpeed,
              '| 剩余油量', '%10.5f' % data.selfdata.NumberofFuel,
              '| 推力', '%10.0f' % data.selfdata.Thrust,
              # 0：未发射；1：飞行中；2：命中；3：失效
              '| 导弹1状态', data.selfdata.Missile1State,
              '| 导弹2状态', data.selfdata.Missile2State, '|',
              )


def print_radardata(i, data):
    print('\n| radar_data',
          '| 友机高低角', '%10.5f' % data.radardata.friend_EleAngle,
          '| 友机方位角', '%10.5f' % data.radardata.friend_AziAngle,
          '| 友机距离', '%10.5f' % data.radardata.friend_Distance,
          '| 北东地速度', '%10.5f' % data.radardata.friend_NorthVelocity,
          '| 北东地速度', '%10.5f' % data.radardata.friend_EastVelocity,
          '| 北东地速度', '%10.5f' % data.radardata.friend_VerticalVelocity, '|',

          '\n| 敌机1编号',  data.radardata.target1_Index,
          '| 敌机1高低角', '%10.5f' % data.radardata.target1_EleAngle,
          '| 敌机1方位角', '%10.5f' % data.radardata.target1_AziAngle,
          '| 敌机1距离', '%10.5f' % data.radardata.target1_Distance,
          '| 北东地速度', '%10.5f' % data.radardata.target1_NorthVelocity,
          '| 北东地速度', '%10.5f' % data.radardata.target1_EastVelocity,
          '| 北东地速度', '%10.5f' % data.radardata.target1_VerticalVelocity, '|',

          '\n| 敌机2编号',  data.radardata.target2_Index,
          '| 敌机2高低角', '%10.5f' % data.radardata.target2_EleAngle,
          '| 敌机2方位角', '%10.5f' % data.radardata.target2_AziAngle,
          '| 敌机2距离', '%10.5f' % data.radardata.target2_Distance,
          '| 北东地速度', '%10.5f' % data.radardata.target2_NorthVelocity,
          '| 北东地速度', '%10.5f' % data.radardata.target2_EastVelocity,
          '| 北东地速度', '%10.5f' % data.radardata.target2_VerticalVelocity, '|',
          )


def print_statedata(i, data):
    print('\n| state_data',
          '| 友机经度', '%10.5f' % data.statedata.friend_Longitude,
          '| 友机纬度', '%10.5f' % data.statedata.friend_Latitude,
          '| 友机高度', '%10.5f' % data.statedata.friend_Altitude,
          '| 友机存活', data.statedata.friend_Survive,

          '\n| 敌机1编号',  data.statedata.target1_Index,
          '| 敌机1经纬高', '%10.5f' % data.statedata.target1_Longitude,
          '| 敌机1经纬高', '%10.5f' % data.statedata.target1_Latitude,
          '| 敌机1经纬高', '%10.5f' % data.statedata.target1_Altitude,
          '| 敌机1存活', data.statedata.target1_Survive,

          '\n| 敌机2编号',  data.statedata.target2_Index,
          '| 敌机2经纬高', '%10.5f' % data.statedata.target2_Longitude,
          '| 敌机2经纬高', '%10.5f' % data.statedata.target2_Latitude,
          '| 敌机2经纬高', '%10.5f' % data.statedata.target2_Altitude,
          '| 敌机2存活', data.statedata.target2_Survive,'|'
          )


def print_closedata(i, data):
    print('\n| close_data',
          '| 友机高低角', '%10.5f' % data.closedata.friend_EleAngle,
          '| 友机方位角', '%10.5f' % data.closedata.friend_AziAngle,
          '| 友机距离', '%10.5f' % data.closedata.friend_Distance,

          '\n| 敌机1编号', data.closedata.target1_Index,
          '| 敌机1高低角', '%10.5f' % data.closedata.target1_EleAngle,
          '| 敌机1方位角', '%10.5f' % data.closedata.target1_AziAngle,
          '| 敌机1距离', '%10.5f' % data.closedata.target1_Distance,

          '\n| 敌机2编号', data.closedata.target2_Index,
          '| 敌机2高低角', '%10.5f' % data.closedata.target2_EleAngle,
          '| 敌机2方位角', '%10.5f' % data.closedata.target2_AziAngle,
          '| 敌机2距离', '%10.5f' % data.closedata.target2_Distance, '|',
          )


def print_alertdata(i, data):
    print('\n| alert_data',
          '| 飞机告警数量',data.alertdata.emergency_num,
          '| 飞机告警方位角',  data.alertdata.emergency_EleAngle,
          '| 飞机告警方位角',data.alertdata.emergency_AziAngle,

          '\n| 导弹告警数量', data.alertdata.emergency_missile_num,
          '| 导弹告警方位角',data.alertdata.emergency_missile_EleAngle,
          '| 导弹告警方位角',data.alertdata.emergency_missile_AziAngle,
          )

# 姜宏睿后续添加，主要用于生成matlab仿真可视化文件。
#主要逻辑为：首先将仿真生成的所有数据保存在output.txt中，然后利用display.py依据此数据画出四个无人机的简单轨迹
#用于快速复盘仿真
def print_outdata2(outdata):

    for i in range(len(outdata)):
        if i == 0:
            print('__________________________________________________________________________________'
                  '__________________________________________________________________________________')
        if i != 0:
            print('\n')

        print_positiondata(i, outdata[i])
        # print(a)
        # print(b)
        # print(len(b))
        # output_file.write("Data:\n")
        data_str = str(a)
        if data_str is not None:
            output_file.write(data_str)
            output_file.write("\n")
        a.clear()

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



#直接输出的就是经纬高转换后的坐标
def print_positiondata(i,data):


    #飞机编号
    a.append(i)
    #计算经度所对应的坐标
    x_lat,y_lon = lat_lon_to_xz(data.selfdata.Latitude,data.selfdata.Longitude)


    a.append(y_lon)
    a.append(x_lat)
    a.append(data.selfdata.Altitude)
    # b.append(a)

    # print(i,
    #       data.selfdata.Longitude,
    #       data.selfdata.Latitude,
    #       data.selfdata.Altitude)