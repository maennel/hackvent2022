# [HV22.05] Missing gift

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

## Description
Like every year the elves were busy all year long making the best toys in Santas workshop. This year they tried some new fabrication technology. They had fun using their new machine, but it turns out that the last gift is missing.

Unfortunately, Alabaster who was in charge of making this gift is not around, because he had to go and fulfill his scout elf duty as an elf on the shelf.

But due to some very lucky circumstances the IT-guy elf was capturing the network traffic during this exact same time.

Goal:
Can you help Santa and the elves to fabricate this toy and find the secret message?

## Solution

Find the `gcode` file upload in the pcap file.

Visualise the `gcode` file in a service such as https://gcode.ws and read the flag.

## Notes
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


## Flag
```
HV22{this-is-a-w4ste-of-pl4stic}
```
