# [HV22.20] § 1337: Use Padding 📝

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

## Description
Santa has written an application to encrypt some secrets he wants to hide from the outside world. Only he and his elves, who have access too all the keys used, can decrypt the messages 🔐.

Santa's friends Alice and Bob have suggested that the application has a padding vulnerability❗, so Santa fixed it 🎅. This means it's not vulnerable anymore, right❗❓

Santa has also written a concept sheet of the encryption process: 

![Alice and Bob](./18ea12cd-8ac2-4106-a00b-a3075d90d2a8.png)

Source file of the service listening on the socket: [santa_aes_source.py](./santa_aes_source.py)

## Solution
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

# Similarly:
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
# Input:
⤀𐀀𐀀üüüüüüüüHV22{üaaaaaüüüüüüüüüü    # 32 characters
            HV22                     # The known secret (4 bytes)
                {                    # The character being brute-forced (1 byte)

⤀𐀀𐀀üü[ü]                            # Block 1: 16 bytes (in 5.5 characters)
      [ü]üüüüHV22{                   # Block 2: 16 bytes (in 9.5 characters)
                 üaaaaaüüüüüüüüüü    # Suffix: (32-4-1=) 27 bytes (in 16 characters)
                 üaaaaaüüüü[ü]       # Block 3: 16 bytes 
                           [ü]üüüüü  # Block 4: 11 bytes, leaving space for the 5 first chars of the secret.

# Encrypted output:
93bf5f8d6cbb8f6f058e60d927910bc9
0b747efd0a676df64ab65a27a2390bec  # Block 2 containing "[ü]üüüüHV22{"
e94f96d4bba3a7d2c764ecd37c8e560e
0b747efd0a676df64ab65a27a2390bec  # Block 4 is identical to block 2!
985f136077c09966e681a0e433b63b45
16e83610eb739f6c474497e599172497


# Conclusion:
The brute-forced character is "{", since the second and the 4th block are identical.
```

With this approach, I brute-forced character by character using a half-manual, half-programmed approach. See my [solver](./dec20-solver.py) for details.

## Links
- https://yidaotus.medium.com/breaking-ecb-by-prepending-your-own-message-b7b376d5efbb
- https://tripoloski1337.github.io/crypto/2020/07/12/attacking-aes-ecb.html
- https://www.utf8-chartable.de/unicode-utf8-table.pl

## Flag
```
HV22{len()!=len()}
```
