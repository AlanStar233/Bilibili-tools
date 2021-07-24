# import User_Info as bliuinfo
import tkinter
import tkinter as tk

window = tkinter.Tk()
window.title('哔哩哔哩用户信息查询')
window.geometry('600x400')

tm = tk.Label(window, text='text here', bg='green', font=('Arial', 12), width=15)
tm.pack()

window.mainloop()
