# YouTube-Playlist-Manager
##AUTHOR: Greg Bomkamp
##DATE: 9/19/2016
###Build folder contains the most recent working version of the application. The application can be run by navigating through:
  build>YouTube Playlist Manager>YouTubePlaylistManager.exe
###Source folder contains: 
1. ypm_source: python application source code that is referenced by the build file.
2. ypm_build.py: cx_freeze build file needed to create the application bundle.
3. yt.ico & YouTube-96.png: both image files used in the application itself.
4. libav-x86-w64-mingw32-20160904: a working avprobe version used to create the mp3 files from the youtube mp4 files. The required files from /usr/bin/ are copied into the application build directory.

All of these are needed in order to create a working build of the applcation. There are many dependencies in order to build a version of this application including python v3.5+ and these modules: cx_freeze, youtube_dl, pillow. Cx_freeze is used to freeze the source code and package into the application. In order to do a fresh build, you will need to run 'python ypm_build.py'. This build file will reference the ypm_source.py file to create the build along will all other files in the source folder.
