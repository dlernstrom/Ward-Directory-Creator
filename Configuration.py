#Configuration

import ConfigParser
import string

ConfigDefault = {
	"ward.wardName":			"Your Ward Name Here",
	"ward.isward":				"1",
	"ward.stakename":			"Your Stake Name Here",
	"quote.usequote":			"1",
	"quote.quotecontent":		"As children of the Lord\nwe should strive every day to rise to a higher level of personal rightousness in all of our actions.",
	"quote.quoteauthor":		"President James E. Faust",
	"block.displaySac":			"0",
	"block.sacstart":			"",#9:00 AM",
	"block.displayss":			"0",
	"block.ssstart":			"",#10:20 AM",
	"block.display_pr_rs":		"0",
	"block.pr_rs_start":		""#11:10 AM"
	}
"""Probably don't need
	"file.csvlocation":			"",
	"file.imagesdirectory":		"",
	"file.pdf_outdirectory":	"",
	"file.imagearchivedir":		"",
	"missing.missingname":		"",
	"missing.missingphone":		"",
	"missing.overridephone":	"0",
	"email.recipientcount":		"",
	"email.recipient1":			"",
	"bldg.addy1":				"",
	"bldg.addy2":				"",
	"bldg.phone":				"",
	"Leadership.BishName":		"",
	"Leadership.BishPhone":		"",
	"Leadership.BishOverPh":	"",
	"Leadership.BishDisp":		"",
	"Leadership.FirstName":		"",
	"Leadership.FirstPhone":	"",
	"Leadership.FirstOverPh":	"",
	"Leadership.FirstDisp":		"",
	"Leadership.SecondName":	"",
	"Leadership.SecondPhone":	"",
	"Leadership.SecondOverPh":	"",
	"Leadership.SecondDisp":	"",
	"Leadership.ClerkName":		"",
	"Leadership.ClerkPhone":	"",
	"Leadership.ClerkOverPh":	"",
	"Leadership.ClerkDisp":		"",
	"Leadership.FinName":		"",
	"Leadership.FinPhone":		"",
	"Leadership.FinOverPh":		"",
	"Leadership.FinDisp":		"",
	"Leadership.MemName":		"",
	"Leadership.MemPhone":		"",
	"Leadership.MemOverPh":		"",
	"Leadership.MemDisp":		"",
	"Leadership.EQName":		"",
	"Leadership.EQPhone":		"",
	"Leadership.EQOverPh":		"",
	"Leadership.EQDisp":		"",
	"Leadership.HPName":		"",
	"Leadership.HPPhone":		"",
	"Leadership.HPOverPh":		"",
	"Leadership.HPDisp":		"",
	"Leadership.RSName":		"",
	"Leadership.RSPhone":		"",
	"Leadership.RSOverPh":		"",
	"Leadership.RSDisp":		"",
	"Leadership.YMName":		"",
	"Leadership.YMPhone":		"",
	"Leadership.YMOverPh":		"",
	"Leadership.YMDisp":		"",
	"Leadership.YWName":		"",
	"Leadership.YWPhone":		"",
	"Leadership.YWOverPh":		"",
	"Leadership.YWDisp":		"",
	"Leadership.PrimaryName":	"",
	"Leadership.PrimaryPhone":	"",
	"Leadership.PrimaryOverPh":	"",
	"Leadership.PrimaryDisp":	"",
	"Leadership.WMLName":		"",
	"Leadership.WMLPhone":		"",
	"Leadership.WMLOverPh":		"",
	"Leadership.WMLDisp":		"",
	"Leadership.ActName":		"",
	"Leadership.ActPhone":		"",
	"Leadership.ActOverPh":		"",
	"Leadership.ActDisp":		"",
	"Leadership.NewsName":		"",
	"Leadership.NewsPhone":		"",
	"Leadership.NewsOverPh":	"",
	"Leadership.NewsDisp":		"",
	"Leadership.DirName":		"",
	"Leadership.DirPhone":		"",
	"Leadership.DirOverPh":		"",
	"Leadership.DirDisp":		""
	}
"""
class Configuration:
	def __init__(self, filename):
		self.filename = filename
		self.LoadConfigFile()

	def LoadConfigFile(self):
		"""
		returns a dictionary with key's of the form
		<section>.<option> and the values 
		"""
		cp = ConfigParser.ConfigParser()
		cp.read(self.filename)
		config = {}
		for sec in cp.sections():
			name = string.lower(sec)
			for opt in cp.options(sec):
				config[name + "." + string.lower(opt)] = string.strip(cp.get(sec, opt))
		self.CurrentConfig = config
		print "Config:", str(config)

	def SetValueByKey(self, key, value):
		section, option = key.split('.')
		self.SetValueByOption(string.lower(section), string.lower(option), value)

	def SetValueByOption(self, section, option, value):
		self.CurrentConfig[string.lower(section) + '.' + string.lower(option)] = value
		self.WriteConfigFile()

	def GetValueByKey(self, key):
		section, option = key.split('.')
		return self.GetValueByOption(section, option)

	def GetValueByOption(self, section, option):
		try:
			value = self.CurrentConfig[section + '.' + option]
		except KeyError:
			value = None
		return value

	def WriteConfigFile(self):
		"""
		given a dictionary with key's of the form 'section.option: value'
		write() generates a list of unique section names
		creates sections based that list
		use config.set to add entries to each section
		"""
		cp = ConfigParser.ConfigParser()
		sections = set([k.split('.')[0] for k in self.CurrentConfig.keys()])
		map(cp.add_section, sections)
		for k,v in self.CurrentConfig.items():
			s, o = k.split('.')
			cp.set(s, o, v)
		cp.write(open(self.filename, "w"))

if __name__=="__main__":
	ConfigHandle = Configuration("some.cfg")
	print "Result:", ConfigHandle.GetValueByKey('coolpeople.coolest')
	ConfigHandle.SetValueByKey('coolpeople.coolest', 'David L Ernstrom')
	#print ConfigHandle
	#ConfigHandle.write(Config)