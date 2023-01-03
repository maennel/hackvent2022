# [HV22.22] Santa's UNO flag decrypt0r

<table>
  <tr>
    <th>Categories</th>
    <td>Reverse engineering</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>leet</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>explo1t</td>
  </tr>
</table>

## Description
The elves made Santa a fancy present for this Christmas season. He received a fancy new Arduino where his elves encoded a little secret for him. However, Santa is super stressed out at the moment, as the children's presents have to be sent out soon. Hence, he forgot the login, the elves told him earlier. Can you help Santa recover the login and retrieve the secret the elves sent him?

## Solution
An [Arduino AVR8 binary](./unoflagdecryptor.elf) is provided.

I opened the binary in Ghidra and reversed the main function.

It read in some password and XORed the password against some hardcoded data in the binary (under the `flags` label).

To get the password, the following validation procedure was derived from the disassembled and sometimes decompiled code (although the decompilation was only useful to see the high lines of the control flow):

```
X = W           # Read one character on the input
X = X + 0x250   # Add 0x250 to X % 0xd
Xlo = *X        # Read data at address X + 0x250 into X
Xhi = 0
X = X + 0x133 + 0x25 = X + 0x158 
Wlo = *X        # Read data at address X + 0x158 into Wlo
```


Memory at `0x250 + (X % 0xd)` as read in:
```
05 5c 03 07 0d 00 3c c8 2b 14 43 31 a5
05 5c 03 07 0d 00 3c c8 2b 14 43 31 a5
05 5c 03 07 0d 00 3c
```
If we add `0x158` to these values, we end up with the following hex values:
```
15d 1b4 15b 15f 165 158 194 220 183 16c 19b 189 1fd
15d 1b4 15b 15f 165 158 194 220 183 16c 19b 189 1fd
15d 1b4 15b 15f 165 158 194
```
If we look up the values at these addresses, we get:
```
f3 b6 28 48 06 41 fc 0e 02 08 10 f5 6a
f3 b6 28 48 06 41 fc 0e 02 08 10 f5 6a 
f3 b6 28 48 06 41 fc
```

Finally, the input password was XORed with the data from the computation above, which had to result in the following sequence of bytes:
```
80 d7 46 3c 67 7b 95 51 6e 67 66 90 35 9b d7 5a 2c 65 71 98 6b 66 57 73 87 59 97 cc 09 69 27 7b d5
```

Taking [the XOR of these two values](https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto')XOR(%7B'option':'Hex','string':'80%20d7%2046%203c%2067%207b%2095%2051%206e%2067%2066%2090%2035%209b%20d7%205a%202c%2065%2071%2098%206b%2066%2057%2073%2087%2059%2097%20cc%2009%2069%2027%207b%20d5'%7D,'Standard',false)&input=ZjMgYjYgMjggNDggMDYgNDEgZmMgMGUgMDIgMDggMTAgZjUgNmEgZjMgYjYgMjggNDggMDYgNDEgZmMgMGUgMDIgMDggMTAgZjUgNmEgZjMgYjYgMjggNDggMDYgNDEgZmM) gives us the expected password:
```
santa:i_love_hardc0ded_cr3dz!!!:)
```

Finally, we XOR this with the data at `flags`:
```
3b 37 5c 46 1a 54 58 3c 5f 30 04 56 29 5b 13 47 55 0d 06 3b 50 0f 6e 0f 1e 49 3b 0f 7e 46 11 0d 54
```

...which returns the flag.

See [how it's done in CyberChef](https://gchq.github.io/CyberChef/#recipe=From_Hex('Auto'/disabled)XOR(%7B'option':'Hex','string':'3b%2037%205c%2046%201a%2054%2058%203c%205f%2030%2004%2056%2029%205b%2013%2047%2055%200d%2006%203b%2050%200f%206e%200f%201e%2049%203b%200f%207e%2046%2011%200d%2054'%7D,'Standard',false)&input=c2FudGE6aV9sb3ZlX2hhcmRjMGRlZF9jcjNkeiEhITop).


## Flag
```
HV22{n1c3_r3v3r51n6_5k1llz_u_g07}
```
