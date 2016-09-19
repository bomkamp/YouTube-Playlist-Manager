from cx_Freeze import setup, Executable
import sys,os
# Dependencies are automatically detected, but it might need
# fine tuning.

path=os.getcwd()

#May need to update this manually to tcl/tk directory
os.environ['TCL_LIBRARY'] = r'C:\Program Files\Python35\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Program Files\Python35\tcl\tk8.6'

#May need fine tuning
files = []
files.append(path+r"\yt.ico")
files.append(path+r"\YouTube-96.png")

files.append(os.environ['TCL_LIBRARY']+r"\..\..\DLLs\tcl86t.dll")
files.append(os.environ['TK_LIBRARY']+r"\..\..\DLLs\tk86t.dll")

for file in os.listdir(path+r"\libav-x86_64-w64-mingw32-20160904\usr\bin"):
    files.append(os.path.join(path+r"\libav-x86_64-w64-mingw32-20160904\usr\bin",file))

buildOptions = {"includes":["tkinter.filedialog","youtube_dl"],
                    "packages":["tkinter.filedialog","youtube_dl"],
                    "optimize":"2",
                     "include_files":files,
                     }
base = 'Win32GUI' if sys.platform=='win32' else 'Console'

executables = [
    Executable('ypm_source.pyw', base=base, targetName = 'YouTubePlaylistManager.exe')
]

setup(name='YouTube Playlist Manager',
      version = '1.0',
      description = 'Downloads mp3 from Youtube video or mp3s from youtube playlist when provided a link. It will place them into a provided directory along with a long so if the program is run again it will only download new songs that it hasnt downloaded already.',
      options = dict(build_exe = buildOptions),
      executables = executables)
