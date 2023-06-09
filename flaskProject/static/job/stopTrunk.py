import win32api as api
import win32console as con
import os
import sys

# 向某个进程发送crtl+c指令
def send_ctrl_c(pid):
    con.FreeConsole()
    if con.AttachConsole(int(pid)) == None:
        api.SetConsoleCtrlHandler(None, 1)
        api.GenerateConsoleCtrlEvent(con.CTRL_C_EVENT, 0)
        api.Sleep(2000)
        con.FreeConsole()
        api.SetConsoleCtrlHandler(None, 0)

# 通过host+port获取进程pid
def get_pid_by_port(port):
    res = os.popen(f'netstat -ano |findstr "{port}"').readlines()
    for i in res:
        if i.split()[-2] == 'LISTENING':
            print(i)
            return i.split()[-1]

port = sys.argv[1]

send_ctrl_c(get_pid_by_port(port))