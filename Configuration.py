#Configuration

import ConfigParser
import string

class Configuration:
	def __init__(self, filename, defaults):
		self.filename = filename
		self.defaults = defaults
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
		if not len(config):
			config = self.defaults
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