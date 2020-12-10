#!/usr/bin/env python
# -*- coding:UTF-8 -*-

'''
Conway's Game of Life
Jimmy Ho
MIT License
'''

'''
RULES OF CONWAY'S GAME OF LIFE
The universe of the Game of Life is a two-dimensional orthogonal grid of square cells, each of which is in one of
two possible states, live or dead, (or populated and unpopulated, respectively). Every cell interacts with its eight neighbours,
which are the cells that are horizontally, vertically, or diagonally adjacent. At each step in time, the following transitions
occur:
1. Any live cell with fewer than two live neighbours dies, as if by underpopulation.
2. Any live cell with two or three live neighbours lives on to the next generation.
3. Any live cell with more than three live neighbours dies, as if by overpopulation.
4. Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
The initial pattern constitutes the seed of the system. The first generation is created by applying the above rules
simultaneously to every cell in the seed; births and deaths occur simultaneously, and the discrete moment at which this
happens is sometimes called a tick. Each generation is a pure function of the preceding one. The rules continue to be applied
repeatedly to create further generations.

康威生命游戏规则
康威生命游戏设计在一个二维细胞矩阵内，每个细胞具有两个状态：存活或死亡。每个细胞都与其周围的8个细胞有一定关系。
每一回合都将满足以下规则：
1. 任何活细胞周围存在少于2个活细胞，则该细胞死亡。
2. 任何活细胞周围存在2~3个活细胞，则该细胞存活。
3. 任何活细胞周围存在多于3个活细胞，则该细胞死亡。
4. 任何死细胞周围存在3个活细胞，则该细胞存活。
初始的状态根据系统随机的种子构造。第一代通过以上规则从原始状态生成，且存活和死亡同时发生。生成一次称为一个tick。
每一代都从前一代生成，且规则一直适用。
'''

import os
import time


# 生成随机矩阵
def initMatrix(length, width):
    from random import randint
    # 避免shallow copy 的方法
    matrix = [[randint(0, 1) for i in range(length)] for i in range(width)]
    return matrix


# 周围存活细胞个数
def scanMatrix(matrix):
    length = len(matrix[0])
    width = len(matrix)
    result = initMatrix(length, width)
    for i in range(width):
        for j in range(length):
            sp = 0
            if (i in range(2, width-1)) and (j in range(2, length-1)):  # 中间区域 8次判断
                if matrix[i-2][j-2] == 1:
                    sp += 1
                if matrix[i-2][j-1] == 1:
                    sp += 1
                if matrix[i-2][j] == 1:
                    sp += 1
                if matrix[i-1][j-2] == 1:
                    sp += 1
                if matrix[i-1][j] == 1:
                    sp += 1
                if matrix[i][j-2] == 1:
                    sp += 1
                if matrix[i][j-1] == 1:
                    sp += 1
                if matrix[i][j] == 1:
                    sp += 1
                result[i-1][j-1] = sp
            elif i == 1 and j == 1:  # 左上角 3次判断
                if matrix[i][j-1] == 1:
                    sp += 1
                if matrix[i-1][j] == 1:
                    sp += 1
                if matrix[i][j] == 1:
                    sp += 1
                result[i-1][j-1] = sp
            elif i == width and j == 1:  # 左下角 3次判断
                if matrix[i-1][j] == 1:
                    sp += 1
                if matrix[i-2][j-1] == 1:
                    sp += 1
                if matrix[i-2][j] == 1:
                    sp += 1
                result[i-1][j-1] = sp
            elif i == 1 and j == length:  # 右上角 3次判断
                if matrix[i-1][j-2] == 1:
                    sp += 1
                if matrix[i-2][j-2] == 1:
                    sp += 1
                if matrix[i-2][j-1] == 1:
                    sp += 1
                result[i-1][j-1] = sp
            elif i == width and j == length:  # 右下角 3次判断
                if matrix[i-2][j-2] == 1:
                    sp += 1
                if matrix[i-1][j-2] == 1:
                    sp += 1
                if matrix[i-2][j-1] == 1:
                    sp += 1
                result[i-1][j-1] = sp
            elif i == 1 and (j in range(2, length-1)):  # 上边界 5次判断
                if matrix[i-1][j-2] == 1:
                    sp += 1
                if matrix[i-1][j] == 1:
                    sp += 1
                if matrix[i][j-2] == 1:
                    sp += 1
                if matrix[i][j-1] == 1:
                    sp += 1
                if matrix[i][j] == 1:
                    sp += 1
                result[i-1][j-1] = sp
            elif i == width and (j in range(2, length-1)):  # 下边界 5次判断
                if matrix[i-2][j-2] == 1:
                    sp += 1
                if matrix[i-2][j-1] == 1:
                    sp += 1
                if matrix[i-2][j] == 1:
                    sp += 1
                if matrix[i-1][j-2] == 1:
                    sp += 1
                if matrix[i-1][j] == 1:
                    sp += 1
                result[i-1][j-1] = sp
            elif (i in range(2, width-1)) and j == 1:  # 左边界 5次判断
                if matrix[i-2][j-1] == 1:
                    sp += 1
                if matrix[i][j-1] == 1:
                    sp += 1
                if matrix[i-2][j] == 1:
                    sp += 1
                if matrix[i-1][j] == 1:
                    sp += 1
                if matrix[i][j] == 1:
                    sp += 1
                result[i-1][j-1] = sp
            elif (i in range(2, width-1)) and j == length:  # 右边界 5次判断
                if matrix[i-2][j-2] == 1:
                    sp += 1
                if matrix[i-1][j-2] == 1:
                    sp += 1
                if matrix[i][j-2] == 1:
                    sp += 1
                if matrix[i-2][j-1] == 1:
                    sp += 1
                if matrix[i][j-1] == 1:
                    sp += 1
                result[i-1][j-1] = sp
    return result


# tick迭代
def updateMatrix(matrix, result):
    length = len(matrix[0])
    width = len(matrix)
    matrixNext = initMatrix(length, width)
    for i in range(width):
        for j in range(length):
            if result[i-1][j-1] == 3:
                matrixNext[i-1][j-1] = 1
            elif matrix[i-1][j-1] == 1 and result[i-1][j-1] == 2:
                matrixNext[i-1][j-1] = 1
            else:
                matrixNext[i-1][j-1] = 0
    return matrixNext


# Terminal矩阵可视化
def visualizeMatrix(matrix):
    visualunit_survive = '❤'
    visualunit_dead = '☠'
    length = len(matrix[0])
    width = len(matrix)
    visual = ''
    for i in range(width):
        for j in range(length):
            if matrix[i-1][j-1] == 1:
                visual += visualunit_survive+' '
            elif matrix[i-1][j-1] == 0:
                visual += visualunit_dead+' '
        visual += '\n'
    return visual


# START TEST
a = initMatrix(40, 30)  # 矩阵大小40*30
v_a = visualizeMatrix(a)
print('原始图形：')
print(v_a)
os.system('pause')
for i in range(100):  # 迭代100次
    os.system('cls')
    b = scanMatrix(a)
    a = updateMatrix(a, b)
    v_a = visualizeMatrix(a)
    print('迭代图形：')
    print(v_a)
    time.sleep(0.03)  # 迭代间隔0.03s
exit(0)
