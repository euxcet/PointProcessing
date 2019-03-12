from picture import Picture
from lut import LUT
import tkinter as tk

class UI:
	def __init__(self):
		self.root = tk.Tk()
		self.pic = []
		self.image = []

	def hm_original(self):
		self.pic[-1].convert_original()
		self.image[-1].configure(image = self.pic[-1].get_tkimg())

	def hm_lum(self):
		lut = LUT().hm(self.pic[0].get_lum_cdf(), self.pic[1].get_lum_cdf())
		self.pic[2].convert_lum(lut)
		self.image[2].configure(image = self.pic[2].get_tkimg())

	def hm_rgb(self):
		lut = LUT().hm3(self.pic[0].get_rgb_cdf(), self.pic[1].get_rgb_cdf())
		self.pic[2].convert_rgb(lut[0], lut[1], lut[2])
		self.image[2].configure(image = self.pic[2].get_tkimg())

	def hm_GB2R(self):
		cdf = self.pic[0].get_rgb_cdf()
		lut0 = LUT().I()
		lut1 = LUT().hm(cdf[1], cdf[0])
		lut2 = LUT().hm(cdf[2], cdf[0])
		self.pic[1].convert_rgb(lut0, lut1, lut2)
		self.image[1].configure(image = self.pic[1].get_tkimg())

	def hm_RB2G(self):
		cdf = self.pic[0].get_rgb_cdf()
		lut0 = LUT().hm(cdf[0], cdf[1])
		lut1 = LUT().I()
		lut2 = LUT().hm(cdf[2], cdf[1])
		self.pic[1].convert_rgb(lut0, lut1, lut2)
		self.image[1].configure(image = self.pic[1].get_tkimg())

	def hm_RG2B(self):
		cdf = self.pic[0].get_rgb_cdf()
		lut0 = LUT().hm(cdf[0], cdf[2])
		lut1 = LUT().hm(cdf[1], cdf[2])
		lut2 = LUT().I()
		self.pic[1].convert_rgb(lut0, lut1, lut2)
		self.image[1].configure(image = self.pic[1].get_tkimg())

	def change_lumi(self, lumi):
		self.pic[0].change_lumi(lumi)
		self.image[0].configure(image = self.pic[0].get_tkimg())

	def change_cont(self, cont):
		self.pic[0].change_cont(cont)
		self.image[0].configure(image = self.pic[0].get_tkimg())

	def create_lumi_scale(self):
		scale = tk.Scale(self.root,
			label = 'Luminance',
			from_ = -100,
			to = 100,
			orient = tk.HORIZONTAL,
			length = 200,
			command = self.change_lumi)

		scale.grid(row = 1)

	def create_cont_scale(self):
		scale = tk.Scale(self.root,
			label = 'Contrast',
			from_ = 0,
			to = 4,
			resolution = 0.05,
			orient = tk.HORIZONTAL,
			length = 200,
			command = self.change_cont)

		scale.grid(row = 2)
		scale.set(1)

	def create_hm_buttons(self, row = 0, col = 0):
		frame = tk.Frame(self.root)
		frame.grid(row = row, column = col)
		tk.Button(frame, text = "Original", width = 10, height= 5, command = self.hm_original).pack()
		tk.Button(frame, text = "By Lum", width = 10, height= 5, command = self.hm_lum).pack()
		tk.Button(frame, text = "By RGB", width = 10, height = 5, command = self.hm_rgb).pack()

	def create_hm_single_buttons(self, row = 0, col = 0):
		frame = tk.Frame(self.root)
		frame.grid(row = row, column = col)
		tk.Button(frame, text = "Original", width = 10, height= 5, command = self.hm_original).pack()
		tk.Button(frame, text = "G & B -> R", width = 10, height= 5, command = self.hm_GB2R).pack()
		tk.Button(frame, text = "R & B -> G", width = 10, height= 5, command = self.hm_RB2G).pack()
		tk.Button(frame, text = "R & G -> B", width = 10, height = 5, command = self.hm_RG2B).pack()

	def load_img(self, image_path, label = '', row = 0, col = 0):
		if (label != ''):
			tk.Label(self.root, text = label).grid(row = row - 1, column = col)
		self.pic.append(Picture(image_path, True))
		self.image.append(tk.Label(self.root, image = self.pic[-1].get_tkimg()))
		self.image[-1].grid(row = row, column = col)

	def start(self):
		self.root.mainloop()
