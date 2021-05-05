from os import chdir, system
import os
import ctypes
from time import sleep
from shutil import move


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
        "@\"%SystemRoot%\\System32\\WindowsPowerShell\\v1.0\\powershell.exe\" -NoProfile -InputFormat None -ExecutionPolicy Bypass -Command \"[System.Net.ServicePointManager]::SecurityProtocol = 3072; iex ((New-Object System.Net.WebClient).DownloadString(\'https://chocolatey.org/install.ps1\'))\" && SET \"PATH=%PATH%;%ALLUSERSPROFILE%\chocolatey\""
    )

    print('Chocolatey installed ...')
    print()

    system("choco feature enable -n allowGlobalConfirmation")

    print('Installing mingw (gcc and g++ compilers)')
    print()
    system("choco install mingw")

    print('MingW installed ...')

    print()
    print('Installing CMake')
    system("choco install cmake --installargs 'ADD_CMAKE_TO_PATH=System'")

    print("Cmake Installed")

    print()
    print('Installing git ...')

    system("choco install git")
    print('Git installed')

    system("refreshenv")

    print('Cloning modified umoria source code ...')
    system("git clone https://github.com/JoshuaPelealu/umoria")

    print('Setup done')

    chdir('./umoria')

    system("powershell.exe -NoP -NonI -Command \"Expand-Archive '.\\PDCurses-3.8.zip' '.\\unzipped'")
    move('./unzipped/PDCurses-3.8', './PDCurses-3.8')

    chdir('./scripts')

    system('explorer .')

    system('start README.txt')

    print('Running first time compile.')

    system('start compile.exe')

    print('PLEASE READ THE README.TXT THAT IS ALREADY OPEN FIRST.')
    input('Press [Enter] to continue ...')

    chdir('../')
    system('start "umoria.sln"')

    input('Press [Enter] to exit ...')


if __name__ == "__main__":

    setup()
