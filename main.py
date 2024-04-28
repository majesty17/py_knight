# -*- conding: utf-8 -*-
import os
from PIL import Image

abc = "0abcdefgh12345678"


def nextStep(now):
    """根据当前位置返回下一跳位置"""
    ret = []
    pos_x = abc.find(now[0])
    pos_y = abc.find(now[1]) - 8

    if pos_x not in range(1, 9) or pos_y not in range(1, 9):
        print(f"the pos <{now}> not valid!")
        return []

    if pos_x + 2 in range(1, 9) and pos_y + 1 in range(1, 9):
        ret.append(abc[pos_x + 2] + str(pos_y + 1))
    if pos_x + 2 in range(1, 9) and pos_y - 1 in range(1, 9):
        ret.append(abc[pos_x + 2] + str(pos_y - 1))
    if pos_x - 2 in range(1, 9) and pos_y + 1 in range(1, 9):
        ret.append(abc[pos_x - 2] + str(pos_y + 1))
    if pos_x - 2 in range(1, 9) and pos_y - 1 in range(1, 9):
        ret.append(abc[pos_x - 2] + str(pos_y - 1))

    if pos_x + 1 in range(1, 9) and pos_y + 2 in range(1, 9):
        ret.append(abc[pos_x + 1] + str(pos_y + 2))
    if pos_x + 1 in range(1, 9) and pos_y - 2 in range(1, 9):
        ret.append(abc[pos_x + 1] + str(pos_y - 2))
    if pos_x - 1 in range(1, 9) and pos_y + 2 in range(1, 9):
        ret.append(abc[pos_x - 1] + str(pos_y + 2))
    if pos_x - 1 in range(1, 9) and pos_y - 2 in range(1, 9):
        ret.append(abc[pos_x - 1] + str(pos_y - 2))
    # print(f"find next stop of {now} is {ret}")
    return ret


def runGame(game):
    """计算"""
    # 情况1，发现一个解：
    if len(game["pos"]) == 0:
        print("solved: path is " + game["path"])

        return

    # 情况2，找到下一跳的8种位置
    now = game["now"]
    for i in nextStep(now):
        # print(i)
        if i not in game["pos"]:  # 如果下一个可跳的点不在pos里，继续
            continue
        else:  # 如果在的话，递归进去
            new_game = {}
            new_game["now"] = i
            new_game["path"] = game["path"] + ',' + i
            new_game["pos"] = game["pos"].replace(i, "")
            runGame(new_game)


def readGame():
    """从屏幕读取游戏"""
    print("屏幕截取中...请稍候!")
    os.system("adb shell screencap -p /sdcard/a.png")
    os.system("adb pull /sdcard/a.png .")
    print("截图完毕！")
    img = Image.open('a.png')
    box = (0, 861, 1080, 1941)
    new_img = img.crop(box)
    new_img = new_img.convert("RGB")

    print(new_img.mode)
    pos = ""
    for i in range(8):
        for j in range(8):
            a = new_img.getpixel((j * 135 + 67, i * 135 + 67))  # j是横向的,左到右；i纵向的，上到下
            # print(a)
            if a in [(255, 255, 255), (113, 134, 184)]:  # 这两种颜色是背景，说明没有旗子
                print("[ ]", end='')
            else:
                pos = pos + abc[j + 1] + str(8 - i)
                print("[x]", end='')
        print("")
    new_img.save("2.png")
    print(pos)

    img.close()

    now = "a7"
    runGame({
        "now": now,
        "pos": pos,
        "path": now
    })


if __name__ == '__main__':
    game = {
        "now": "e4",  # 马当前的位置
        "pos": "c5",  # 棋盘上仍存在的位置，为空说明结束
        "path": "e4"  # 已经走过的位置，包括当前位置
    }
    readGame()
    # runGame(game)
    # print(nextStep('a8'))
