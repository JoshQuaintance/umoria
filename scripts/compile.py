from os import chdir, environ, system, path
import subprocess
import sys
from shutil import move


def check():
    print('Checking if everything is setup yet ...')
    status, result = subprocess.getstatusoutput("choco -v")

    if (status == 1):
        print('Chocolatey is not installed yet ...')
        print('Please run the \'setup.exe\' first')
        input('Press [Enter] to exit ...')
        exit()

    status, result = subprocess.getstatusoutput("gcc -v")

    if (status == 1):
        print('gcc is not installed yet ...')
        print('Please run the \'setup.exe\' first')
        input('Press [Enter] to exit ...')
        exit()

    status, result = subprocess.getstatusoutput("g++ -v")

    if (status == 1):
        print('g++ is not installed yet ...')
        print('Please run the \'setup.exe\' first')
        input('Press [Enter] to exit ...')
        exit()

    status, result = subprocess.getstatusoutput("g++ -v")

    if (status == 1):
        print('cmake is not installed yet ...')
        print('Please run the \'setup.exe\' first')
        input('Press [Enter] to exit ...')
        exit()

    print('Check done ...')
    return


def get_paths():
    curses_lib = None
    curses_lib_include = None

    print('Getting curses library path ...')

    if path.exists('../PDCurses-3.8/wincon/pdcurses.lib'):
        curses_lib = path.abspath('../PDCurses-3.8/wincon/pdcurses.lib').encode('unicode_escape')
        curses_lib_include = path.abspath('../PdCurses-3.8').encode('unicode_escape')
    else:
        print("Cannot find PDCurses file ...")
        print('There was something wrong when cloning the git repository')
        print('Well, I don\'t know what you did, but if I\'m in your class')
        print('Ask for my help ... bc I\'m way too lazy to document this')

    return curses_lib.decode(), curses_lib_include.decode()


def move_necessary_files():
    chdir('./umoria/')

    if (not path.exists('./Debug/data')):
        move('./data/', './Debug/')

    if (not path.exists('./Debug/AUTHORS')):
        move('./AUTHORS', './Debug/AUTHORS')

    if (not path.exists('./Debug/LICENSE')):
        move('./LICENSE', './Debug/LICENSE')

    if (not path.exists('./Debug/scores.dat')):
        move('./scores.dat', './Debug/scores.dat')

    chdir('../scripts')

    return


def compile():

    check()

    print('Setting system variables ...')
    print()

    curses_lib, curses_lib_include = get_paths()

    # environ['CURSES_LIBRARY'] = "H:\\umoria\\PDCurses-3.8\\wincon\\pdcurses.lib"
    # environ['CURSES_INCLUDE_PATH'] = "H:\\umoria\\PDCurses-3.8"

    environ['CURSES_LIBRARY'] = curses_lib
    environ['CURSES_INCLUDE_PATH'] = curses_lib_include

    print('Building Compile Makefile')
    print()

    chdir('../')

    status, result = subprocess.getstatusoutput(
        "cmake -DCURSES_LIBRARY=\"%CURSES_LIBRARY%\" -DCURSES_INCLUDE_PATH=\"%CURSES_INCLUDE_PATH%\" -G \"Visual Studio 16 2019\" -A Win32 .")

    if(status == 1):
        print('Makefile compilation failed')

    print()
    print('Makefile built ...')
    print('Compiling code ...')

    status, result = subprocess.getstatusoutput("cmake --build .")

    if (status == 0):
        print('Compile complete')

    elif(status == 1):
        print('Compile failed: ')
        print(result)

    move_necessary_files()

    fin = open('root_dir', 'w')

    print(path.abspath('../'))

    fin.write(path.abspath('../'))

    fin.close()

    return


if __name__ == '__main__':
    compile()
