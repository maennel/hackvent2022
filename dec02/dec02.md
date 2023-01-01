# [HV22.02] Santa's song

<table>
  <tr>
    <th>Categories</th>
    <td>Fun</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>easy</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>kuyaya</td>
  </tr>
</table>

## Description
Santa has always wanted to compose a song for his elves to cherish their hard work. Additionally, he set up a vault with a secret access code only he knows!

The elves say that Santa has always liked to hide secret messages in his work and they think that the vaults combination number may be hidden in the magnum opus of his.

What are you waiting for? Go on, help the elves!

The provided pdf with [sheet music](./song.pdf).

### Hints
**Hint #1**: Keep in mind that you are given a web service, not a play button for a song.

**Hint #2**: As stated in the description, Santa's vault accepts a number, not text.

## Solution
The sheet music translates to the following musical notes:
```
 b a e  | f a c e d  | a | b a d | d e e d
```
Convert the resulting hex number to decimal:
```
ba ef ac ed ab ad de ed => 13470175147275968237
```

Enter the number (`13470175147275968237`) to the webservice and see flag.

## Flag
`HV22{13..s0me_numb3rs..37}`

## Resources
- [Sheet music](https://blog.sheetmusicplus.com/2015/12/30/learn-how-to-read-sheet-music-notes/)
- Calc
