import tkinter as tk


def center_window(panel, width=300, height=200):
	# get screen width and height
	screen_width = panel.winfo_screenwidth()
	screen_height = panel.winfo_screenheight()

	# calculate position x and y coordinates
	x = (screen_width / 2) - (width / 2)
	y = (screen_height / 2) - (height / 2)
	panel.geometry('%dx%d+%d+%d' % (width, height, x, y))


root_panel = tk.Tk()
# root.geometry('960x500')
center_window(root_panel, 960, 500)
root_panel.resizable(False, False)  # 固定窗体
root_panel.title('我的第一个Python窗体')

    
def callback():
	print("~被调用了~")


# 创建一个顶级菜单
menubar = tk.Menu(root_panel)

# 创建一个下拉菜单“文件”，然后将它添加到顶级菜单中
filemenu = tk.Menu(menubar, tearoff=False)
filemenu.add_command(label="打开", command=callback)
filemenu.add_command(label="保存", command=callback)
filemenu.add_separator()
filemenu.add_command(label="退出", command=root_panel.quit)
menubar.add_cascade(label="文件", menu=filemenu)

# 创建另一个下拉菜单“编辑”，然后将它添加到顶级菜单中
editmenu = tk.Menu(menubar, tearoff=False)
editmenu.add_command(label="剪切", command=callback)
editmenu.add_command(label="拷贝", command=callback)
editmenu.add_command(label="粘贴", command=callback)
menubar.add_cascade(label="编辑", menu=editmenu)

# 显示菜单
# root_panel.config(menu=menubar)

root_panel['menu'] = menubar
root_panel.mainloop()

