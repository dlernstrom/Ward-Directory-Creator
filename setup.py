import time
import string

if __name__ == '__main__':
    versionFile = open('__version__.py', 'r+');
    versionFile.write('# Last Time The Person Hit Build:\n')
    versionFile.write('# ' + str(string.rjust(time.ctime(), 50)))
    versionFile.close()
