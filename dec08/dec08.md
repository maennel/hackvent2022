# [HV22.08] Santa's Virus

<table>
  <tr>
    <th>Categories</th>
    <td>Open-source intelligence</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>medium</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>yuva</td>
  </tr>
</table>

## Description
A user by the name of HACKventSanta may be spreading viruses. But Santa would never do that! The elves want you to find more information about this filthy impersonator.

![Evil santa](./37ff7417-5c2d-46bc-985c-715e6193d57a.jpg)

## Solution
This was a cat and mouse game through popular platforms, exploiting the open source information they provide.
Only with Twitter (if I'm not mistaken) one had to have a registered and logged in user.

The following steps were followed:
- Reverse image search and the picture's alternative name (`1668610707921`) lead to LinkedIn https://ch.linkedin.com/pub/dir/+/Hacker/ch-0-Schweiz (on an icognito browser).
- LinkedIn profile: https://ch.linkedin.com/in/hackventsanta
- Portfolio leads to: https://github.com/HackerSanta
- Has a release with the name "TAG": https://github.com/HackerSanta/FILES/releases/tag/HV22
- Has a file with the name `Undetected`.
- Running strings on this provides a string `ThisIsTheKeyToReceiveTheGiftFromSanta`.
- Uploading the file to Virustotal gives the info: "Almost there - Twitter-SwissSanta2022": https://www.virustotal.com/gui/file/4d0e17d872f1d5050ad71e0182073b55009c56e9177e6f84a039b25b402c0aef/details
- Twitter profile: https://twitter.com/SwissSanta2022
- 3 tweets with links:
  - https://tinyurl.com/4yekektd
  - https://qr1.be/H8YX
  - https://drive.google.com/file/d/11pKYrcwr7Hf1eSUq8twtN5aMK-oziPE4/view?usp=sharing
- The last Google Drive link is password protected. Use password `ThisIsTheKeyToReceiveTheGiftFromSanta`.
- Decode the Base64 string: https://gchq.github.io/CyberChef/#recipe=From_Base64('A-Za-z0-9%2B/%3D',true,false)&input=U0ZZeU1udElUMGhQSzFOQlRsUkJLMGRKVmtWVEswWk1RVWRUSzA1UFZDdFdTVkpWVTMwPQ
- Read the flag.

## Credits
Thanks to the FAIRTIQ security team for the entertaining solving session.

## Flag
```
HV22{HOHO+SANTA+GIVES+FLAGS+NOT+VIRUS}
```
