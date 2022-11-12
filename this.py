import tkinter as tk
import time
import threading
 
songs = ['爱情买卖', '朋友', '回家过年', '好日子']
movies = ['阿凡达', '猩球崛起']
 
 
def music(songs):
    global text  # 故意的，注意与movie的区别
    for s in songs:
        text.insert(tk.END, "听歌曲：%s \t-- %s\n" % (s, time.ctime()))
        time.sleep(1)
 
 
def movie(movies, text):
    for m in movies:
        text.insert(tk.END, "看电影：%s \t-- %s\n" % (m, time.ctime()))
        time.sleep(2)
 
 
root = tk.Tk()
 
text = tk.Text(root)
text.pack()
 
tk.Button(root, text='音乐', command=music(songs)).pack()
tk.Button(root, text='电影', command=movie(movies, text)).pack()
 
root.mainloop()