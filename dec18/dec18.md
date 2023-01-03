# [HV22.18] Santa's Nice List

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

## Description

Santa stored this years "Nice List" in an encrypted zip archive. His mind occupied with christmas madness made him forget the password. Luckily one of the elves wrote down the SHA-1 hash of the password Santa used.

```
xxxxxx69792b677e3e4c7a6d78545c205c4e5e26
```

Can you help Santa access the list and make those kids happy?

## Solution

Start investigating the [provided zip file](./nice-list.zip), which seems to be encrypted.

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

## Links
- https://hashcat.net/forum/thread-7794.html
- https://www.bleepingcomputer.com/news/security/an-encrypted-zip-file-can-have-two-correct-passwords-heres-why/
- https://hashcat.net/wiki/doku.php?id=hashcat

## Flag
```
HV22{HAVING_FUN_WITH_CHOSEN_PREFIX_PBKDF2_HMAC_COLLISIONS_nzvwuj}
```
