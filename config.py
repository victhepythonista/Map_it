import os
from configparser import ConfigParser


CONFIG_FILE = './data/settings/settings.config'

def check_folder(path):
    if os.path.isdir(path):
        return True
    else:
        try:
            os.mkdir(path)
            return True
        except:
            print('could not create path ',path)
            return False
def check_file(  path):
    if os.path.isfile(path) :
        return True
    else:
        try:
            with open(path, 'w') as stg:
                stg.close()
                return True
        except:
            return False
def check_section(conf,section):
    try:
        conf[section]
        return True
    except:
        conf.add_section(section)
        return True
def check_variable_in_section(conf, section,variable,default_data  =''):
    try:
        conf[section][variable]
        return True
    except:
        conf[section][variable] = default_data
        return True
def save_configuration(conf):
    check_file(CONFIG_FILE)
    with open(CONFIG_FILE, 'w') as f:
        conf.write(f)
def make_parser():
    conf = ConfigParser()
    conf.read(CONFIG_FILE)
    return conf


class Config:
    @staticmethod
    def read(  section, var ,data_if_none ='' ):
        conf = make_parser()
        check_section(conf,section)
        check_variable_in_section(conf,section,var,default_data = data_if_none)
        data = conf[section][var ]
        save_configuration(conf)
        return data
    @staticmethod
    def write(  section, var, data):
        conf = make_parser()
        check_section(conf,section)
        conf[section][var] = data
        save_configuration(conf)

#Config.write('MAPEDITOR','AUTO_RECT', 'True')
#bool = Config.read('MAPEDITOR','AUTO_RECT')
