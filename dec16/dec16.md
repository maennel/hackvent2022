# [HV22.16] Needle in a qrstack

<table>
  <tr>
    <th>Categories</th>
    <td>Fun</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>hard</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>dr_nick</td>
  </tr>
</table>

## Description

Santa has lost his flag in a qrstack - it is really like finding a needle in a haystack.

Can you help him find it?

## Solution
In the [provided image (which is very large)](./haystack.png) a big QR code is composed by many (as in "a lot of") smaller QR codes at different scales.

To find the needle (the QR code containing the flag) in the haystack (the bunchof QR codes), I tried to disqalify wrong QR codes in an as lightweight way as possible.

To do so, I followed this algorithm:
1. Scan top left to top right for QR codes the size of one unit.
2. Test for whether the region at hand is a QR code. It is if it has a target (the recogniseable square on QR codes) in the top-left or bottom right corner.
3. If it is a QR code, compare it - unit by unit - to a wrong QR code and disqualify it, if equal. Later, I optimised this to only compare the sum of white pixels in the QR code.
4. If it is a QR code and does not match the wrong QR code, it is the QR code containing the flag. Stop the process at that point.
5. If it is not a QR code, it's either completely white (skip it in that case) or multiple QR codes at a deeper level. In the latter case, we would recurse and start from the beginning one level deeper.

See [my code(in python)](./solver.py) for the final solution. It runs through in about 40 seconds max.

The QR code containing the flag looks as follows (and I don't know where exactly it's located in the initial image ;) ):

![QR code containing the flag](./flag_scaled.png)

## Flag
```
HV22{1'm_y0ur_need13.}
```
