import tkinter as tk
from PIL import Image
from PIL import ImageTk

class Picture:
	def __init__(self, path = ""):
		self.img = None
		self.tkimg = None
		if (path != ""):
			self.img = Image.open("logo.png")
			self.img = self.img.resize((300,300))
			self.tkimg = ImageTk.PhotoImage(self.img)
			self.imglist = [x for x in self.img.getdata()]

		self.luma = 0
		self.cont = 1

	def get_img(self):
		return self.img

	def get_tkimg(self):
		return self.tkimg

	def luma_cont(self, pixel):
		return (max(min(int(pixel[0] * self.cont + self.luma) , 255), 0),
				max(min(int(pixel[1] * self.cont + self.luma) , 255), 0),
				max(min(int(pixel[2] * self.cont + self.luma) , 255), 0),
				pixel[3])

	def update(self):
		tmp = [self.luma_cont(pixel) for pixel in self.imglist]
		self.img.putdata(tmp)
		self.tkimg = ImageTk.PhotoImage(self.img)

	def change_luma(self, luma):
		self.luma = int(luma)
		self.update()

	def change_cont(self, cont):
		self.cont = float(cont)
		self.update()





def change_cont(cont):
	print(cont)

class UI:
	def __init__(self):
		self.root = tk.Tk()


	def change_luma(self, luma):
		self.pic.change_luma(luma)
		self.label.configure(image = self.pic.get_tkimg())

	def change_cont(self, cont):
		self.pic.change_cont(cont)
		self.label.configure(image = self.pic.get_tkimg())

	def create_luma_scale(self):
		scale = tk.Scale(self.root,
			label = 'Luma',
			from_ = -100,
			to = 100,
			orient = tk.HORIZONTAL,
			length = 200,
			command = self.change_luma)

		scale.pack()


	def create_cont_scale(self):
		scale = tk.Scale(self.root,
			label = 'Contrast',
			from_ = 0,
			to = 4,
			resolution = 0.05,
			orient = tk.HORIZONTAL,
			length = 200,
			command = self.change_cont)

		scale.set(1)
		scale.pack()


	def load_img(self):
		self.pic = Picture("logo.png")
		self.label = tk.Label(self.root, image = self.pic.get_tkimg())
		self.label.pack()

	def start(self):
		self.root.mainloop()

def main():
	ui = UI()
	ui.load_img()
	ui.create_luma_scale()
	ui.create_cont_scale()

	ui.start()

if __name__ == "__main__":
	main()
