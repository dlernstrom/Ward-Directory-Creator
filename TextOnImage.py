from reportlab.platypus.flowables import ParagraphAndImage

class TextOnImage(ParagraphAndImage):
	'''combine a Paragraph ON an Image'''
	def wrap(self,availWidth,availHeight):
		wI, hI = self.I.wrap(availWidth,availHeight)
		self.wI = wI
		self.hI = hI
		# work out widths array for breaking
		####################################
		## I made the change so that the image width is the maximum width of the
		## flowable... the text needs to show up on the image
		self.width = self.wI
		P = self.P
		style = P.style
		xpad = self.xpad
		ypad = self.ypad
		leading = style.leading
		leftIndent = style.leftIndent
		later_widths = availWidth - leftIndent - style.rightIndent
		intermediate_widths = later_widths - xpad - wI
		first_line_width = intermediate_widths - style.firstLineIndent
		P.width = 0
		nIW = int((hI+ypad)/leading)
		P.blPara = P.breakLines([first_line_width] + nIW*[intermediate_widths]+[later_widths])
		if self._side=='left':
			self._offsets = [wI+xpad]*(1+nIW)+[0]
		P.height = len(P.blPara.lines)*leading
		self.height = max(hI,P.height)
		return (self.width, self.height)

	def draw(self):
		canv = self.canv
		if self._side=='left':
			self.I.drawOn(canv,0,self.height-self.hI)
			self.P._offsets = self._offsets
			try:
				self.P.drawOn(canv,0,0)
			finally:
				del self.P._offsets
		elif self._side == 'center':
			self.I.drawOn(canv, 0, 0)
			self.P.drawOn(canv, 0, self.ypad)
		else:#image on right
			self.I.drawOn(canv,self.width-self.wI-self.xpad,self.height-self.hI)
			self.P.drawOn(canv,0,0)