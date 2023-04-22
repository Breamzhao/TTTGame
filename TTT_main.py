# This Project works good on Python 3.11.3. Make sure your Python version is beyond 3.0
import os
import random

""" 
操作简介：
-------------
| 1 | 2 | 3 |
-------------
| 4 | 5 | 6 |
-------------
| 7 | 8 | 9 |
-------------
你执X棋先手，输入对应的棋盘编号在即可在对应位置落子，落子的表现将会实时更新在棋盘上

"""



#清除屏幕信息，刷新棋盘
def UpdateTable():
    os.system('cls')
    print(f"-------------")
    print(f"| {TableState[0][0]} | {TableState[0][1]} | {TableState[0][2]} |")
    print(f"-------------")
    print(f"| {TableState[1][0]} | {TableState[1][1]} | {TableState[1][2]} |")
    print(f"-------------")
    print(f"| {TableState[2][0]} | {TableState[2][1]} | {TableState[2][2]} |")
    print(f"-------------")

#判定是否有人胜利，是返回对应棋子X或者O，否返回0
def isWin(Table):
    #横向3行判定
    for row in range(3):
        if Table[row][0] == Table[row][1] and Table[row][1] == Table[row][2] and Table[row][0] != ' ':
            if Table[row][0] == 'O':
                return 'O'
            else:
                return 'X'
    
    #纵向3行判定
    for col in range(3):
        if Table[0][col] == Table[1][col] and Table[1][col] == Table[2][col] and Table[0][col] != ' ':
            if Table[0][col] == 'O':
                return 'O'
            else:
                return 'X'

    #对角判定判定
    if (Table[0][0] == Table[1][1] and Table[1][1] == Table[2][2] and Table[0][0] != ' ') or (Table[0][2] == Table[1][1] and Table[1][1] == Table[2][0] and Table[0][2] != ' '):
        if Table[0][col] == 'O':
            return 'O'
        else:
            return 'X'
    
    #判定都没过就返回false
    return 0

#获取玩家输入，并转化为row和col
def getUserInput():
    position = ''
    while 1:
        position = input(f"Input your position: ")
        if position.isdigit():
            if int(position) <= 9 and int(position) > 0:
                break            
        print("Invalid Input! Please Input a integer from 1 to 9!")
    
    row = (int(position) - 1) // 3
    col = (int(position) - 1) % 3
    return [row, col]

#判定某个点是否可以放下棋子
def canPutOnChess(table, row, col):
    return table[row][col] == ' '

#在某个棋盘位置放下棋子
def putOnChess(table, row, col):
    Xcount = 0
    Ocount = 0
    NextisX = True
    for r in range(3):
        for c in range(3):
            if table[r][c] == 'X': Xcount += 1
            if table[r][c] == 'O': Ocount += 1
    
    NextisX = (Xcount == Ocount)
    
    if table[row][col] == ' ':
        if NextisX:
            table[row][col] = 'X'
        else:
            table[row][col] = 'O'
        return True
    return False

#判断棋盘是不是已经满了
def isTableFull(table):
    for row in range(3):
        for col in range(3):
            if table[row][col] == ' ':
                return False
    return True

# 获取当前棋盘的可走区域
def getAvaliablePosition(Table):
    AvailablePosition = []
    for r in range(3):
        for c in range(3):
            if Table[r][c] == ' ':
                AvailablePosition.append([r,c])
    return AvailablePosition

def countOXS(Table, p1, p2, p3):
    Ocount = 0
    Xcount = 0
    Scount = 0
    SPosition = []
    if Table[p1[0]][p1[1]] == 'O': Ocount += 1
    elif Table[p1[0]][p1[1]] == ' ': 
        Scount += 1
        SPosition = p1
    elif Table[p1[0]][p1[1]] == 'X': Xcount += 1

    if Table[p2[0]][p2[1]] == 'O': Ocount += 1
    elif Table[p2[0]][p2[1]] == ' ': 
        Scount += 1
        SPosition = p2
    elif Table[p2[0]][p2[1]] == 'X': Xcount += 1

    if Table[p3[0]][p3[1]] == 'O': Ocount += 1
    elif Table[p3[0]][p3[1]] == ' ': 
        Scount += 1
        SPosition = p3
    elif Table[p3[0]][p3[1]] == 'X': Xcount += 1

    return [Ocount, Xcount, Scount, SPosition]


# AI策略算法
def calcAIInput(Table):
    AP = getAvaliablePosition(Table)
    
    #先判断有没有自己二连即将获胜的点，有就直接赢
    for elem in AP:
        rowres = countOXS(Table, [0,elem[1]], [1,elem[1]], [2, elem[1]])
        if rowres[0] == 2 and rowres[2] == 1: return rowres[3]

        colres = countOXS(Table, [elem[0], 0], [elem[0], 1], [elem[0], 2])
        if colres[0] == 2 and colres[2] == 1: return colres[3]

        if (elem[0] + elem[1]) % 2 == 0:
            diagonal1res = countOXS(Table, [0, 0], [1, 1], [2, 2])
            diagonal2res = countOXS(Table, [0, 2], [1, 1], [2, 0])
            if diagonal1res[0] == 2 and diagonal1res[2] == 1: return diagonal1res[3]
            if diagonal2res[0] == 2 and diagonal2res[2] == 1: return diagonal2res[3]

    #再判断有没有对手二连即将获胜的点，有就堵死
    for elem in AP:
        rowres = countOXS(Table, [0,elem[1]], [1,elem[1]], [2, elem[1]])
        if rowres[1] == 2 and rowres[2] == 1: return rowres[3]

        colres = countOXS(Table, [elem[0], 0], [elem[0], 1], [elem[0], 2])
        if colres[1] == 2 and colres[2] == 1: return colres[3]

        if (elem[0] + elem[1]) % 2 == 0:
            diagonal1res = countOXS(Table, [0, 0], [1, 1], [2, 2])
            diagonal2res = countOXS(Table, [0, 2], [1, 1], [2, 0])
            if diagonal1res[1] == 2 and diagonal1res[2] == 1: return diagonal1res[3]
            if diagonal2res[1] == 2 and diagonal2res[2] == 1: return diagonal2res[3]
    
    #如果不符合条件，优先走中心和角上（即Row + Col为偶数的点），然后走边上
    bHasCornerChoice = False
    for elem in AP:
        if (elem[0] + elem[1]) % 2 == 0 : 
            bHasCornerChoice = True
            break
    if bHasCornerChoice == True:
        #调试发现循环会跳过[1,0]这个元素，感觉是Remove和for的逻辑有点冲突，不太好查，所以直接做两遍筛选
        for elem in AP:
            if(elem[0] + elem[1]) % 2 == 1:
                AP.remove(elem)
        for elem in AP:
            if(elem[0] + elem[1]) % 2 == 1:
                AP.remove(elem)

    Position = random.choice(AP)
    return Position



"""下面是流程代码"""


#先初始化棋盘状态并刷新棋盘表现
TableState = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
UpdateTable()

#无人获胜棋盘也没满时，根据玩家输入放棋子
while not isTableFull(TableState) and isWin(TableState) == 0:
    UserInput = getUserInput()
    isSuccess = putOnChess(TableState, UserInput[0], UserInput[1])

    UpdateTable()

    if not isSuccess:
        print(f'Invalid Choice! Position not Empty!')    
    
    #AI下棋逻辑
    else: 
        if isWin(TableState) == 0 and not isTableFull(TableState):
            AIInput = calcAIInput(TableState)
            putOnChess(TableState, AIInput[0], AIInput[1])
            UpdateTable()
    


#有人获胜或者棋盘满了，跳出循环，打印结果并结束程序
UpdateTable()
if isWin(TableState) == 0:
    if isTableFull(TableState):
        print('Draw!')
elif isWin(TableState) == 'X':
    print('X win!')
elif isWin(TableState) == 'O':
    print('O win!')