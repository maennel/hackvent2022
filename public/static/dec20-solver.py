#!/usr/bin/enc python
# -*- coding: utf-8 -*-
import socket
import sys
from string import ascii_lowercase, ascii_uppercase, ascii_letters, digits, punctuation

host = '402c82fd-8d8b-4c1b-a2a7-ee3e834c6aec.rdocker.vuln.land'
port = 1337

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except socket.error:
    print('Failed to create socket')
    sys.exit()

print('# Getting remote IP address')
try:
    remote_ip = socket.gethostbyname( host )
except socket.gaierror:
    print('Hostname could not be resolved. Exiting')
    sys.exit()

# Connect to remote server
print('# Connecting to server, ' + host + ' (' + remote_ip + ')')
s.connect((remote_ip , port))

print(s.recv(2048))


for c in ascii_letters + digits +punctuation:
    m = f"⤀𐀀𐀀üüüüüüüüHV22{{{c}üaaaaaüüüüüüüüüü\n" # l
    m = f"𐀀𐀀𐀀⤀üüüüüHV22{{l{c}⤀aaaaaaaaüüüüüüü\n" # e
    m = f"⤀𐀀𐀀⤀üüüüüHV22{{le{c}⤀aaaaaaaüüüüüüü\n" # n
    m = f"⤀𐀀⤀⤀üüüüüHV22{{len{c}⤀aaaaaaüüüüüüü\n" # (
    m = f"⤀⤀⤀⤀üüüüüHV22{{len({c}⤀aaaaaüüüüüüü\n" # )
    m = f"⤀⤀⤀üüüüüüHV22{{len(){c}⤀aaaaüüüüüüü\n" # !
    m = f"⤀⤀üüüüüüüHV22{{len()!{c}⤀aaaüüüüüüü\n" # =
    m = f"⤀üüüüüüüüHV22{{len()!={c}⤀aaüüüüüüü\n"  # l
    m = f"⤀aüüüüüüüHV22{{len()!=l{c}⤀aüüüüüüü\n"  # e
    m = f"üaüüüüüüüHV22{{len()!=le{c}⤀üüüüüüü\n"  # n
    m = f"aaüüüüüüüHV22{{len()!=len{c}⤀⤀üüüüü\n"  # (
    m = f"aaaüüüüüüHV22{{len()!=len({c}⤀⤀⤀üüü\n"  # )
    m = f"aaaaüüüüüHV22{{len()!=len(){c}⤀⤀⤀⤀ü\n"  # }

    print(m)
    s.sendall(m.encode())
    out = s.recv(2048)
    print(out)
    data = out[0:16*2*6]
    guess = data[16*2:2*16*2]
    flag = data[3*16*2:4*16*2]
    print(c)
    print(f"{flag} == {guess}")
    if guess == flag:

        print()
        print(f"Match: {c} ({flag})")
        break
    s.sendall(b'y\n')
    s.recv(2048)

