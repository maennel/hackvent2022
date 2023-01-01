# [HV22.03] gh0st

<table>
  <tr>
    <th>Categories</th>
    <td>Fun, Crypto</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>easy</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>0xdf</td>
  </tr>
</table>

## Description

The elves found this Python script that Rudolph wrote for Santa, but it's behaving very strangely. It shouldn't even run at all, and yet it does! It's like there's some kind of ghost in the script! Can you figure out what's going on and recover the flag?

## Solution
Null bytes and python are not a good match.

Modify the source file as follows to print out the flag.
```diff
--- gh0st.py    2022-12-29 18:19:06.838727817 +0100
+++ gh0st_mod.py        2022-12-29 18:36:37.261604169 +0100
@@ -44,8 +44,10 @@
 flag = list(map(ord, sys.argv[1]))
 correct = [17, 55, 18, 92, 91, 10, 38, 8, 76, 127, 17, 12, 17, 2, 20, 49, 3, 4, 16, 8, 3, 58, 67, 60, 10, 66, 31, 95, 1, 93]
 
-for i,c in enumerate(flag):
-    flag[i] ^= ord(song[i*10 % len(song)])
+for i,c in enumerate(correct):
+    correct[i] ^= ord(song[i*10 % len(song)])
+
+print("".join([chr(c) for c in correct]))
 
 if all([c == f for c,f in zip(correct, flag)]):
     print('''Congrats!''')
```

## Flag
```
HV22{nUll_bytes_st0mp_cPy7h0n}
```
