# -*- coding: utf-8 -*-

# ****************************************************
# * class_iniconf.py
# *
# *    user configParser class
# *
# *  2019/06/28  T.Noguchi  create
# *
# *
# ****************************************************

import os
import sys
#sys.path.append('')

import configparser
import json

# -----------------------------------
# module variable
# -----------------------------------
# conf file
CONFIG_SETTINGS = {
    'authorize': [
        {'name': 'user_id',   'type': str,  'required': True},
        {'name': 'token',     'type': str,  'required': True},
    ],
    'object': [
        {'name': 'object',    'type': str,  'required': True},
    ],
    'resource': [
        {'name': 'url',       'type': str,  'required': True},
        {'name': 'query',     'type': str,  'required': False},
        {'name': 'action',    'type': str,  'required': False},
    ],
    'output': [
        {'name': 'ftype',     'type': str,  'required': True},
    ],
}

# character set
charset = 'UTF-8'

# -----------------------------------
# local function
# -----------------------------------

# -----------------------------------
# class
# -----------------------------------
class AttributeDict(object):

    def __init__(self, obj):
       self.obj = obj

    def __getstate__(self):
        return self.obj.items()

    def __setstate__(self):
        if not hasattr(self, 'obj'):
            self.obj = {}
        for key, val in items:
            self.obj[key] = val

    def __getattr__(self, name):
        if name in self.obj:
            return self.obj.get(name)
        else:
            return None

    def fields(self):
        return self.obj

    def keys(self):
        return self.obj.keys()


class Iniobj():

    def __init__(self, conf_file, conf_settings):
        self.conf_file = conf_file
        if conf_settings is None:
            self.conf_settings = CONFIG_SETTINGS
        else:
            self.conf_settings = conf_settings

        self.config = configparser.SafeConfigParser()
        self.obj = None

        if os.path.exists(self.conf_file):
            self.config.read(self.conf_file, encoding=charset)

    def get(self, sect, key):
        return self.config.get(sect, key)

    def set(self, sect, opt, value):
        if not self.config.has_section(sect):
            self.config.add_section(sect)

        self.config.set(sect, opt, value)

    def write(self):
        with open(self.conf_file, 'w') as f:
            self.config.write(f)

    # read and set config param
    def configParse() :

        ### File check
        if not os.path.exists(self.conf_file) :
            raise IOError(file_path)

        parser = configparser.ConfigParser()
        parser.read(self.conf_file)

        ### Convert to dictionary
        config = {}
        for sect in parser.sections() :
            config[sect] = {}
            for opt in parser.options(sect) :
                config[sect][opt] = parser.get(sect, opt)

        for sect in config.keys() :
            # multisector check
            if sect.startswith('resource') :
                sect_a = 'resource'
            else :
                sect_a = sect

            # check section
            if not sect_a in config_settings :
                raise KeyError(sect)

            for opt_attr in config_settings[sect_a] :
                # check need attributes
                if opt_attr['required'] and (not opt_attr['name'] in config[sect]) :

                    raise KeyError(opt_attr['name'])

                # exchange
                if config[sect][opt_attr['name']] == 'None' :
                    config[sect][opt_attr['name']] = None
                else :
                    config[sect][opt_attr['name']] = \
                        opt_attr['type'](config[sect][opt_attr['name']])

        self.obj = json.loads(json.dumps(config), object_hook=AttributeDict)

        return config, self.obj




