# 作者： Charles
# 公众号： Charles的皮卡丘
# 音乐下载器
# 目前支持的平台:
# 	网易云: wangyiyun.wangyiyun()
# 	QQ: qq.qq()
# 	酷狗: kugou.kugou()
# 	千千: qianqian.qianqian()
import os
import threading
from platforms import *
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk


# 下载器类
class Download_Thread(threading.Thread):
	def __init__(self, *args, **kwargs):
		super(Download_Thread, self).__init__(*args, **kwargs)
		self.__pause = threading.Event()
		self.__pause.clear()
		self.__running = threading.Event()
		self.__running.set()
		# 对应关系:
		# 	网易云音乐 -> '1'
		# 	QQ音乐 -> '2'
		# 	酷狗音乐 -> '3'
		# 	千千音乐 -> '4'
		self.engine = None
		self.songname = None
		self.num = 1
	def run(self):
		while self.__running.isSet():
			self.__pause.wait()
			if self.engine == '1':
				self.show_start_info()
				try:
					wangyiyun.wangyiyun().get(self.songname, num=self.num)
					self.show_end_info()
				except:
					title = '资源不存在'
					msg = '所要下载的资源不存在！'
					messagebox.showerror(title, msg)
			elif self.engine == '2':
				self.show_start_info()
				try:
					qq.qq().get(self.songname, num=self.num)
					self.show_end_info()
				except:
					title = '资源不存在'
					msg = '所要下载的资源不存在！'
					messagebox.showerror(title, msg)
			elif self.engine == '3':
				self.show_start_info()
				try:
					kugou.kugou().get(self.songname, num=self.num)
					self.show_end_info()
				except:
					title = '资源不存在'
					msg = '所要下载的资源不存在！'
					messagebox.showerror(title, msg)
			elif self.engine == '4':
				self.show_start_info()
				try:
					qianqian.qianqian().get(self.songname, num=self.num)
					self.show_end_info()
				except:
					title = '资源不存在'
					msg = '所要下载的资源不存在！'
					messagebox.showerror(title, msg)
			else:
				title = '解析失败'
				msg = '输入框参数解析失败！'
				messagebox.showerror(title, msg)
			self.pause()
	def pause(self):
		self.__pause.clear()
	def resume(self):
		self.__pause.set()
	def stop(self):
		self.__pause.clear()
		self.__running.clear()
	def show_start_info(self):
		title = '开始下载'
		msg = '搜索平台: {}\n已开始下载{}，请耐心等待。'.format(self.engine, self.songname)
		messagebox.showinfo(title, msg)
	def show_end_info(self, savepath='./results'):
		title = '下载成功'
		msg = '{}下载成功, 共{}歌曲被下载。'.format(self.songname, len(os.listdir(savepath)))
		messagebox.showinfo(title, msg)
t_download = Download_Thread()
t_download.start()


# 下载器
def downloader(options, op_engine_var, en_songname_var, en_num_var):
	try:
		engine = str(options.index(str(op_engine_var.get())) + 1)
		songname = str(en_songname_var.get())
		num = int(en_num_var.get())
	except:
		title = '输入错误'
		msg = '歌曲名或歌曲下载数量输入错误！'
		messagebox.showerror(title, msg)
		return None
	t_download.engine = engine
	t_download.songname = songname
	t_download.num = num
	t_download.resume()


# 关于作者
def ShowAuthor():
	title = '关于作者'
	msg = '作者: Charles\n公众号: Charles的皮卡丘\nGithub: https://github.com/CharlesPikachu/Music-Downloader'
	messagebox.showinfo(title, msg)


# 退出程序
def stopDemo():
	t_download.resume()
	t_download.stop()
	exit(-1)


# 主界面
def Demo(options):
	assert len(options) > 0
	# 初始化
	root = Tk()
	root.title('音乐下载器V1.0——公众号:Charles的皮卡丘')
	root.resizable(False, False)
	root.geometry('480x368+400+120')
	image_path = './bgimgs/bg1_demo.jpg'
	bgimg = Image.open(image_path)
	bgimg = ImageTk.PhotoImage(bgimg)
	lb_bgimg = Label(root, image=bgimg)
	lb_bgimg.grid()
	# Menu
	menubar = Menu(root)
	filemenu = Menu(menubar, tearoff=False)
	filemenu.add_command(label='退出', command=lambda: stopDemo(), font=('楷体', 10))
	menubar.add_cascade(label='文件', menu=filemenu)
	filemenu = Menu(menubar, tearoff=False)
	filemenu.add_command(label='关于作者', command=ShowAuthor, font=('楷体', 10))
	menubar.add_cascade(label='更多', menu=filemenu)
	root.config(menu=menubar)
	# Label+Entry组件
	# 	歌名
	lb_songname = Label(root, text='歌名:   ', font=('楷体', 10), bg='white')
	lb_songname.place(relx=0.1, rely=0.05, anchor=CENTER)
	en_songname_var = StringVar()
	en_songname = Entry(root, textvariable=en_songname_var, width=15, fg='gray', relief=GROOVE, bd=3)
	en_songname.insert(0, '尾戒')
	en_songname.place(relx=0.3, rely=0.05, anchor=CENTER)
	# 	下载数量
	lb_num = Label(root, text='下载数量:', font=('楷体', 10), bg='white')
	lb_num.place(relx=0.1, rely=0.15, anchor=CENTER)
	en_num_var = StringVar()
	en_num = Entry(root, textvariable=en_num_var, width=15, fg='gray', relief=GROOVE, bd=3)
	en_num.insert(0, '1')
	en_num.place(relx=0.3, rely=0.15, anchor=CENTER)
	# Label+OptionMenu组件
	lb_engine = Label(root, text='搜索引擎:', font=('楷体', 10), bg='white')
	lb_engine.place(relx=0.1, rely=0.25, anchor=CENTER)
	op_engine_var = StringVar()
	op_engine_var.set(options[0])
	op_engine = OptionMenu(root, op_engine_var, *options)
	op_engine.place(relx=0.3, rely=0.25, anchor=CENTER)
	# Button组件
	bt_download = Button(root, text='搜索并下载', bd=2, width=15, height=2, command=lambda: downloader(options, op_engine_var, en_songname_var, en_num_var), font=('楷体', 10))
	bt_download.place(relx=0.3, rely=0.40, anchor=CENTER)
	bt_download = Button(root, text='退出程序', bd=2, width=15, height=2, command=lambda: stopDemo(), font=('楷体', 10))
	bt_download.place(relx=0.3, rely=0.55, anchor=CENTER)
	root.mainloop()



if __name__ == '__main__':
	options = ["1.网易云音乐", "2.QQ音乐", "3.酷狗音乐", "4.千千音乐"]
	Demo(options)
