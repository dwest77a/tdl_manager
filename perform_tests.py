## Python test setup script

import os

os.system('cp -r tests/test*.py .')
os.system('pytest test*.py')

os.system('rm -r test*.py')