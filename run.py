# @Author: DivineEnder
# @Date:   2018-03-10 08:27:59
# @Email:  danuta@u.rochester.edu
# @Last modified by:   DivineEnder
# @Last modified time: 2018-03-11 00:14:46

from Utils import settings
settings.init()
import sys

from importlib import import_module

def main():
	script = sys.argv[1:2][0].replace("/", ".").replace("\\", ".")
	mod = import_module(script)
	mod.main()

if __name__ == "__main__":
	main()
