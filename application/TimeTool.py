import urllib2
import time

Websites = [['http://directory.ernstrom.net/date.php', ''],
			['', '']]

def TimeTool():
	for Site in Websites:
		req = urllib2.Request(Websites[0][0])
		fd = urllib2.urlopen(req)
		page = ''
		while 1:
			data = fd.read(1024)
			if not len(data):
				break
			page += data
			#print page
		if len(page):
			fd.close()
			if Websites[0][1] == '':
				return page
			else:
				CommandString = 'return ' + Websites[0][1] + '(page)'
				#print CommandString
				exec(CommandString)

if __name__ == '__main__':
	print TimeTool()