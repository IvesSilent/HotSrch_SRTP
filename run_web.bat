@echo off

REM 设置Python环境变量路径
set PYTHON=python

REM 执行训练命令
start "Flask App" %PYTHON% app.py

REM 等待服务器启动
timeout /t 1

REM 自动打开默认浏览器访问Flask应用
start http://127.0.0.1:5000

pause