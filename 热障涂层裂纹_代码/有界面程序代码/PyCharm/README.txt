PyCharm中python程序生成可执行文件只需在PyCharm的Terminal终端中输入：pyinstaller -F -w xxx.py或pyinstaller -D xxx.py
-F：是所有库文件打包成一个可执行文件，windows下是exe，Linux下是对应的可执行文件；
-w：是禁止弹出黑色控制台窗口。
-F：生成一个文件夹，里面是多文件模式，启动快。
-D：仅仅生成一个文件，不暴露其他信息，启动较慢。（以-F和-D打包出的软件均在软件文件夹里，正如这所说-F多文件、启动快，-D一个文件、启动慢。）
-w：窗口模式打包，不显示控制台。
前提是已安装pyinstaller工具，安装此工具只需在PyCharm的Terminal终端中输入：pip install pyinstaller