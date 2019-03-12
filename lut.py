class LUT():
	def __init__(self):
		pass

	def I(self):
		lut = [i for i in range(0, 256)]
		return lut

	# cdf [0, 255] -> [0, 255]
	# cdf'[0, 255] -> [0, 255]
	def inv(self, cdf):
		lut = [0 for i in range(0, 256)]
		for i in range(0, 256):
			for j in range(255, -1, -1):
				if (cdf[j] < i):
					lut[i]= j
					break
		return lut

	# cdf_1 * cdf_2
	def mul(self, cdf_1, cdf_2):
		lut = [cdf_2[x] for x in cdf_1]
		return lut

	# cdf * c
	def mul_i(self, cdf, c):
		lut = [int(x * c) for x in cdf]
		return lut

	# pdf [0, 255] -> [0, 1]
	# cdf [0, 255] -> [0, 1]
	def hm(self, cdf_1, cdf_2):
		return self.mul(self.mul_i(cdf_1, 255), self.inv(self.mul_i(cdf_2, 255)))

	def hm3(self, cdf_1, cdf_2):
		return (self.hm(cdf_1[0], cdf_2[0]), self.hm(cdf_1[1], cdf_2[1]), self.hm(cdf_1[2], cdf_2[2]))
