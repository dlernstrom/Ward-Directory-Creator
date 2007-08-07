#RotatedTable

from reportlab.platypus import Table

class RotatedTable90(Table):
	def wrap(self, availWidth, availHeight):
		w, h = Table.wrap(self, availHeight = availWidth, availWidth = availHeight)
		#print "Wrap called"
		self.TableUsedw = w
		self.TableUsedh = h
		return h, w

	def draw(self):
		#print "Draw called"
		self.canv.translate(dx = self.TableUsedh, dy = 0)
		self.canv.rotate(90)
		Table.draw(self)

class RotatedTable270(Table):
	def wrap(self, availWidth, availHeight):
		w, h = Table.wrap(self, availHeight = availWidth, availWidth = availHeight)
		#print "Wrap called"
		self.TableUsedw = w
		self.TableUsedh = h
		return h, w

	def draw(self):
		#print "Draw called"
		self.canv.translate(dx = 0, dy = self.TableUsedw)
		self.canv.rotate(270)
		Table.draw(self)
