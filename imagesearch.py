import ctypes
import time
from win32api import GetSystemMetrics
from datetime import datetime


class ImgSearch(object):
	"""docstring for ImgSearch"""

	def __init__(self):
		super(ImgSearch, self).__init__()
		self.dllFunc = ctypes.windll.LoadLibrary('ImageSearchDLL.dll')
		self.dllFunc.ImageSearch.argtypes = (ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_char_p, ctypes.c_char_p,)
		self.dllFunc.ImageSearch.restype = ctypes.c_char_p
		self.default_width = GetSystemMetrics(0)
		self.default_height = GetSystemMetrics(1)
		self.resultPosition = 1
		self.tolerance = 0

	def ImageSearch(self, findImage, top=None, right=None, left=None, bottom=None, resultPosition=None, tolerance=None):
		if right == None:
			right = self.default_width
		if bottom == None:
			bottom = self.default_height
		if resultPosition == None:
			resultPosition = self.resultPosition
		if tolerance == None:
			tolerance = self.tolerance
		right, bottom = int(right), int(bottom)  # convert it if is decimal
		if isinstance(findImage, str):  # Just in case
			if tolerance > 0:
				findImage = "*{} {}".format(tolerance, findImage)
			res = self.dllFunc.ImageSearch(0, 0, right, bottom, findImage.encode(), findImage.encode())
		if res != b'0':
			_, x, y, w, h = [int(i) for i in res.decode().split('|')]
			if resultPosition:
				x, y = x + w / 2, y + h / 2  # center
			return x, y

	def ImageSearchs(self, findImage, top=None, right=None, left=None, bottom=None, resultPosition=None, tolerance=None):
		if isinstance(findImage, list):
			findImages = findImage
		else:
			findImages = [findImage]
		for findImage in findImages:
			res = self.ImageSearch(findImage, top, right, right, bottom, resultPosition, tolerance)
			if res:
				return res + (findImages.index(findImage),)  # append the index
			# print(res, findImage)

	def WaitForImageSearch(self, findImage, waitSecs, top=None, right=None, left=None, bottom=None, resultPosition=None, tolerance=None, wait_hide=False):
		startTime = datetime.now()
		while (datetime.now() - startTime).total_seconds() < waitSecs:
			res = self.ImageSearchs(findImage, top, right, left, bottom, resultPosition, tolerance)
			if wait_hide:
				if not res:
					return 1
			elif res:
				return res
			time.sleep(0.02)
