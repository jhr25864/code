from multifighters.simulation_env import CombatEnv
from multifighters.SimInput import FighterDataIn, print_outdata


if __name__ == '__main__':
    # 初始化设定
    env = CombatEnv()
    datain = [FighterDataIn() for m in range(4)]
    ######################## 飞机设定控制模式为0或3 ###########################
    for i in range(4):
        datain[i].control_mode = 3

    # 完成初始化
    env.initial(datain)

    # 开始多轮仿真
    for i_episode in range(1):
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
            print('\n仿真步长', t)
            print_outdata(outdata)

            # 仿真结束
            if terminal >= 0:
                print("Episode: \t{} ,episode len is: \t{}".format(i_episode, t))
                print(terminal, blue_time_count, red_time_count)
                break

