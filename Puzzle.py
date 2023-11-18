import os
from PIL import Image 
import tkinter as tk
import tkinter.messagebox as msg
import numpy as np
import win32ui

class Square:
    def __init__(self,orderID):
        self.orderID=orderID
    def draw(self,canvas,board_pos):
        img=Pics[self.orderID]
        canvas.create_image(board_pos,image=img)

def SplitImage():
    dlg = win32ui.CreateFileDialog(1) # 1表示打开文件对话框
    dlg.SetOFNInitialDir('D:') # 设置打开文件对话框中的初始显示目录
    dlg.DoModal()
    src=dlg.GetPathName()
    if src !='':
        img=Image.open(src)
        w,h=img.size

        rownum=int(input('请输入切割行数:'))
        colnum=int(input('请输入切割列数:'))

        rowheight=h//rownum
        colwidth=w//colnum

        num=0
        if rowheight and colwidth:
            for i in range(rownum):
                for j in range(colnum):
                    p_path=os.path.dirname(src)+"/"+os.path.splitext(os.path.basename(src))[0]
                    if not os.path.exists(p_path):
                        os.makedirs(p_path)
                    box=(j*colwidth,i*rowheight,(j+1)*colwidth,(i+1)*rowheight)
                    img.crop(box).save(p_path+"/"+str(num)+".png")
                    num+=1
            return p_path,colwidth,rowheight,colnum,rownum
            print('处理已完成！')
        else:
            print('行列切割参数不合理！')
    else:
        return '','','','',''

#加载图片
def load_pics():
    Pics=[]
    order=[i for i in range(len(os.listdir(path)))]
    os.chdir(path)
    for i in order:
        Pics.append(tk.PhotoImage(file=str(i)+'.png'))
    return Pics

#生成正确顺序的列表
def board_mk():
    small=[]
    big=[]
    count=0
    for i in range(ROW):
        for j in range(COL):
            small.append(count)
            count+=1
        big.append(small)
        small=[]
    return big

def init_board():
    #打乱图像块
    L=list(range(ROW*COL))
    np.random.shuffle(L)
    #print(L)
    for i in range(ROW):
        for j in range(COL):
            idx=i*ROW+j
            orderID=L[idx]
            board[i][j]=Square(orderID)
            
def drawBoard(canvas):
    
    #绘制黑框
    canvas.create_polygon((0,0,WIDTH,0,WIDTH,HEIGHT,0,HEIGHT),width=1,outline='Black')
    #绘制所有图像块
    for i in range(ROW):
        for j in range(COL):
            board[i][j].draw(canvas,(colwidth*(j+0.5),rowheight*(i+0.5)))
            
def switch(pos):
    global steps
    global note
    global r1
    global c1
    global current_square
    
    #将单机位置换算成拼图板上的棋盘坐标
    r=int(pos.y//rowheight)
    c=int(pos.x//colwidth)
    if r < ROW and c < COL:
        if note == 0:
            current_square=board[r][c]
            labelval("已选择一块拼图，单击下一个拼图可与之交换位置。")
            r1=r
            c1=c
            note+=1
        elif note == 1:
            board[r1][c1]=board[r][c]
            board[r][c]=current_square
            drawBoard(cv)
            labelval("拼图位置已交换")
            note=0
            steps+=1
            lab2.config(text='步数：'+str(steps))
            
            #每交换一次拼图都会进行一次输赢判断
            if win():
                msg.showinfo(title="恭喜!",message="你成功了！")
        
def labelval(vText):
    lab1.config(text=vText)
    
def win():
    for i in range(ROW):
        for j in range(COL):
            if board[i][j].orderID != i*ROW+j:
                return False
    return True

def eBtnClose():
    root.destroy()
    
def replay():
    print("重新开始")
    global steps
    steps=0
    b1.config(text='重新开始游戏')
    lab1.config(text='选择一个拼图')
    lab2.config(text='步数：'+str(steps))
    init_board()
    cv.delete('all') #清除画布上所有内容
    drawBoard(cv)
    
if __name__=='main':
    #设置窗口
    root=tk.Tk()
    root.title("拼图游戏")

    path,colwidth,rowheight,COL,ROW=SplitImage()

    steps=0
    note=0
    r1=None
    c1=None
    current_square=None

    WIDTH=colwidth*COL
    HEIGHT=rowheight*ROW

    board=board_mk()
    Pics=load_pics()

    cv=tk.Canvas(root,bg='green',width=WIDTH,height=HEIGHT)
    cv.bind('<Button-1>',switch)
    cv.pack()
    b1=tk.Button(root,text='单击以开始游戏',command=replay,width=20)
    b1.pack()
    lab1=tk.Label(root,text='选择一个拼图',width=60)
    lab1.pack()
    lab2=tk.Label(root,text='步数：'+str(steps),fg='red',width=20)
    lab2.pack()
    b2=tk.Button(root,text='结束游戏',command=eBtnClose,width=20)
    b2.pack()

    replay()
    root.mainloop()