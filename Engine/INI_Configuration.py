# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os

from ConfigParser import ConfigParser, NoSectionError, \
    MissingSectionHeaderError


class Config(object):
    DEFAULT_INI_SECTION = 'wdc'
    def __init__(self, ini_defaults):
        super(Config, self).__setattr__('ini_defaults', ini_defaults)
        self.ensure_ini_path_exists()

    @property
    def config_dir(self):
        return os.path.join(os.environ['APPDATA'], self.DEFAULT_INI_SECTION)

    @property
    def ini_file_name(self):
        return os.path.join(self.config_dir, 'wdc.ini')

    def ensure_ini_path_exists(self):
        d = os.path.dirname(self.ini_file_name)
        if not os.path.exists(d):
            os.makedirs(d)

    def __getattr__(self, k):
        try:
            return self.get_config_val(k)
        except (AttributeError, KeyError, MissingSectionHeaderError):
            pass
        if k in self.ini_defaults:
            self.__setattr__(k, self.ini_defaults[k])
            return self.ini_defaults[k]
        raise AttributeError("Doesn't exist in other class nor INI")

    def __setattr__(self, k, v):
        if not k.lower() == k:
            raise Exception("Key must be lower case")
        config = self.get_config()
        config[k] = v
        self.set_config(config)

    def get_config(self):
        cp = ConfigParser()
        cp.read(self.ini_file_name)
        config = {}
        try:
            options = cp.options(self.DEFAULT_INI_SECTION)
        except NoSectionError:
            return config
        for opt in options:
            config_val = cp.get(self.DEFAULT_INI_SECTION, opt).strip()
            config[opt.lower()] = config_val
        return config

    def get_config_val(self, key):
        config = self.get_config()
        return config[key]

    def set_config(self, config):
        cp = ConfigParser()
        cp.add_section(self.DEFAULT_INI_SECTION)
        for k, v in config.items():
            cp.set(self.DEFAULT_INI_SECTION, k, v)
        with open(self.ini_file_name, "w") as f:
            cp.write(f)

    def get_config_string(self):
        msg = '<table border="1"><tr><th>Parameter</th><th>Value</th></tr>'
        config = self.get_config()
        keys = config.keys()
        keys.sort()
        for key in keys:
            msg += "<tr><td>%s</td><td>%s</td></tr>" % (key, config[key])
        msg += "</table>"
        return msg


class INIMixin(object):
    def __init__(self, *args, **kwargs):
        ini_defaults = {}
        if 'ini_defaults' in kwargs:
            ini_defaults = kwargs.pop('ini_defaults')
        super(INIMixin, self).__setattr__('ini', Config(ini_defaults))
        super(INIMixin, self).__init__(*args, **kwargs)

    @property
    def cache_dir(self):
        return self.ini.config_dir

    def __getattr__(self, k):
        if k in self.ini.ini_defaults:
            return self.ini.__getattr__(k)
        #return super(INIMixin, self).__getattr__(k)

    def __setattr__(self, k, v):
        if k in self.ini.ini_defaults:
            return self.ini.__setattr__(k, v)
        return super(INIMixin, self).__setattr__(k, v)
