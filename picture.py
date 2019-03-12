from PIL import Image
from PIL import ImageTk
from lut import LUT
import numpy as np
import matplotlib.pyplot as plt

def luminance(pixel):
	#return (pixel[0] + pixel[1] + pixel[2]) // 3
	return int(pixel[0] * 0.299 + pixel[1] * 0.587 + pixel[2] * 0.114)

class Picture:
	def __init__(self, path = "", resize = False):
		if (path == ""):
			print("Path is required to load image.")
			# throw
			exit(0)

		self.img = Image.open(path)
		if (resize):
			size = self.img.size
			self.img = self.img.resize((size[0] * 300 // size[1], 300))

		self.tkimg = ImageTk.PhotoImage(self.img)
		self.data = [x for x in self.img.getdata()]

		self.lumi = 0
		self.cont = 1

		self.calc_rgb_cdf()
		self.calc_lum_cdf()

	def get_img(self):
		return self.img

	def get_tkimg(self):
		return self.tkimg

	# pdf [0, 255] -> [0, 1]
	# cdf [0, 255] -> [0, 1]
	def calc_lum_cdf(self):
		self.pdf_l = [0 for i in range(0, 256)]
		self.cdf_l = [0 for i in range(0, 256)]

		for x in self.data:
			self.pdf_l[luminance(x)] += 1 / len(self.data)

		self.cdf_l[0] = self.pdf_l[0]
		for i in range(1, 256):
			self.cdf_l[i] = self.cdf_l[i - 1] + self.pdf_l[i]

	def calc_rgb_cdf(self):
		self.pdf_r = [0 for i in range(0, 256)]
		self.pdf_g = [0 for i in range(0, 256)]
		self.pdf_b = [0 for i in range(0, 256)]

		self.cdf_r = [0 for i in range(0, 256)]
		self.cdf_g = [0 for i in range(0, 256)]
		self.cdf_b = [0 for i in range(0, 256)]
		for x in self.data:
			self.pdf_r[x[0]] += 1 / len(self.data)
			self.pdf_g[x[1]] += 1 / len(self.data)
			self.pdf_b[x[2]] += 1 / len(self.data)

		self.cdf_r[0] = self.pdf_r[0]
		self.cdf_g[0] = self.pdf_g[0]
		self.cdf_b[0] = self.pdf_b[0]
		for i in range(1, 256):
			self.cdf_r[i] = self.cdf_r[i - 1] + self.pdf_r[i]
			self.cdf_g[i] = self.cdf_g[i - 1] + self.pdf_g[i]
			self.cdf_b[i] = self.cdf_b[i - 1] + self.pdf_b[i]

	def get_rgb_cdf(self):
		return (self.cdf_r, self.cdf_g, self.cdf_b)

	def get_lum_cdf(self):
		return self.cdf_l



	def lumi_cont(self, pixel):
		return (max(min(int(pixel[0] * self.cont + self.lumi) , 256), 0),
				max(min(int(pixel[1] * self.cont + self.lumi) , 256), 0),
				max(min(int(pixel[2] * self.cont + self.lumi) , 256), 0),
				pixel[3])

	def update(self):
		tmp = [self.lumi_cont(pixel) for pixel in self.data]
		self.img.putdata(tmp)
		self.tkimg = ImageTk.PhotoImage(self.img)

	def change_lumi(self, lumi):
		self.lumi = int(lumi)
		self.update()

	def change_cont(self, cont):
		self.cont = float(cont)
		self.update()


	def match_lumi(self, target):
		lut = LUT().hm(self.get_lum_cdf(), target.get_lum_cdf())
		self.convert_lum(lut)

	def match_rgb(self, target):
		cdf_1 = self.get_rgb_cdf()
		cdf_2 = target.get_rgb_cdf()
		lut0 = LUT().hm(cdf_1[0], cdf_2[0])
		lut1 = LUT().hm(cdf_1[1], cdf_2[1])
		lut2 = LUT().hm(cdf_1[2], cdf_2[2])
		self.convert_rgb(lut0, lut1, lut2)

	def match_GB2R(self):
		cdf = self.get_rgb_cdf()
		#lut0 = LUT().I()
		#lut1 = LUT().hm(cdf[1], cdf[0])
		#lut2 = LUT().hm(cdf[2], cdf[0])
		lut0 = LUT().I()
		lut1 = LUT().I()
		lut2 = LUT().I()
		self.convert_rgb(lut0, lut1, lut2)

	def match_RB2G(self):
		cdf = self.get_rgb_cdf()
		lut0 = LUT().hm(cdf[0], cdf[1])
		lut1 = LUT().I()
		lut2 = LUT().hm(cdf[2], cdf[1])
		self.convert_rgb(lut0, lut1, lut2)

	def match_RG2B(self):
		cdf = self.get_rgb_cdf()
		lut0 = LUT().hm(cdf[0], cdf[2])
		lut1 = LUT().hm(cdf[1], cdf[2])
		lut2 = LUT().I()
		self.convert_rgb(lut0, lut1, lut2)

	def show(self):
		self.img.show()

	def save(self, path):
		self.img.save(path)


	def convert_lum_pixel(self, pixel, lut):
		return (lut[pixel[0]], lut[pixel[1]], lut[pixel[2]])
		source = luminance(pixel)
		target = lut[luminance(pixel)]
		if (source == 0):
			return (target, target, target)
		dlt = target / source
		return (int(pixel[0] * dlt), int(pixel[1] * dlt), int(pixel[2] * dlt))

	def convert_original(self):
		self.img.putdata(self.data)
		self.tkimg = ImageTk.PhotoImage(self.img)

	def convert_rgb(self, lut_r, lut_g, lut_b):
		tmp = [(lut_r[pixel[0]], lut_g[pixel[1]], lut_b[pixel[2]]) for pixel in self.data]
		self.img.putdata(tmp)
		self.tkimg = ImageTk.PhotoImage(self.img)

	def convert_lum(self, lut):
		tmp = [self.convert_lum_pixel(pixel, lut) for pixel in self.data]
		#tmp = [self.convert_lum_pixel(pixel, lut) for pixel in self.data]
		self.img.putdata(tmp)
		self.tkimg = ImageTk.PhotoImage(self.img)
