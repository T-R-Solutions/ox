import os,sys
assert sys.argv[1]=='bus-child'
fd=int(sys.argv[2]);os.dup2(fd,3);os.set_inheritable(3,True)
os.environ.update(LISTEN_FDS='1',LISTEN_PID=str(os.getpid()))
os.execv('/usr/bin/dbus-broker-launch',['dbus-broker-launch','--scope','user'])
