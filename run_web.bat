@echo off

REM ����Python��������·��
set PYTHON=python

REM ִ��ѵ������
start "Flask App" %PYTHON% app.py

REM �ȴ�����������
timeout /t 1

REM �Զ���Ĭ�����������FlaskӦ��
start http://127.0.0.1:5000

pause