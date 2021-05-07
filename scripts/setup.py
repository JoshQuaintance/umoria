from os import chdir, system
import os
import ctypes
from time import sleep
from shutil import move
import subprocess


def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0

    return is_admin


def setup():
    if (not isAdmin()):
        print('Script not running as admin ...')
        print('Please run this script with admin access...')
        input('Press [Enter] to exit ...')
        return

    print('')
    print('Installing Chocolatey')
    print('')

    system(
        "start \"CHOCO INSTALL\" /wait powershell.exe -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command \"[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString(\'https://chocolatey.org/install.ps1\'))\" && SET \"PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\""
    )

    sleep(1)
    status, result = subprocess.getstatusoutput("refreshenv")

    if (status == 1):
        print('There is an issue with refreshenv.')
        print('I cannot control this.')
        print('The only thing you can do is run the script again')
        input('Press [Enter] to exit ...')
        exit()

    system('refreshenv')

    print('Chocolatey installed ...')
    print()

    system("choco feature enable -n allowGlobalConfirmation")

    print('Installing mingw (gcc and g++ compilers)')
    print()
    system("start \"Install MINGW\" /wait choco install mingw")

    sleep(1)
    system('refreshenv')
    print('MingW installed ...')

    print()
    print('Installing CMake')
    system("start \"Install CMake\" /wait choco install cmake --installargs 'ADD_CMAKE_TO_PATH=System'")

    sleep(1)
    system('refreshenv')
    print("Cmake Installed")

    print()
    print('Installing git ...')

    system("start \"Install git\" /wait choco install git")
    print('Git installed')

    print('Checking if git command works yet or not ...')
    sleep(1)

    status, result = subprocess.getstatusoutput("git --version")

    if status == 1:
        print('It seems like the git command isn\'t working yet.')
        print('I give up already and just not fix this error')
        print('What you can do is just literally run this script again')
        input('Press [Enter] to exit ...')
        exit()

    print('Cloning modified umoria source code ...')
    system("start /wait git clone https://github.com/JoshuaPelealu/umoria")

    print('Setup done')

    chdir('./umoria')

    system("powershell.exe -NoP -NonI -Command \"Expand-Archive '.\\PDCurses-3.8.zip' '.\\unzipped'")
    move('./unzipped/PDCurses-3.8', './PDCurses-3.8')

    chdir('./scripts')

    system('explorer .')

    print('Running first time compile.')

    system('start compile.exe')

    system('start README.md')

    print('PLEASE READ THE README.TXT THAT IS ALREADY OPEN FIRST.')
    input('Press [Enter] to continue ...')

    chdir('../')
    system('start umoria.sln')

    input('Press [Enter] to exit ...')


if __name__ == "__main__":
    setup()
