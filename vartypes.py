import struct

class MSBoolean:
	value = False
	position = 0
	
	def __init__(self, value, position):
		self.value = value
		self.position = position
		
	def __repr__(self):
		return "<boolean pos=" + str(self.position) + ", value=" + str(self.value) + ">"
		
	def update(self, dataArray, value):
		dataArray[self.position] = (0 if value == False else 1)
		self.value = value
		
class MSInteger32:
	value = 0
	position = 0
	
	def __init__(self, value, position):
		self.value = value
		self.position = position
		
	def __repr__(self):
		return "<integer32 pos=" + str(self.position) + ", value=" + str(self.value) + ">"
		
	def update(self, dataArray, value):
		v = struct.pack(">I", value)
		dataArray[self.position] = v[0]
		dataArray[self.position] = v[1]
		dataArray[self.position] = v[2]
		dataArray[self.position] = v[3]		
		self.value = value
