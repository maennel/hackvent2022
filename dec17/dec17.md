# [HV22.17] Santa's Sleigh

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

## Description
As everyone seems to modernize, Santa has bought a new E-Sleigh. Unfortunately, its speed is limited. Without the sleight's full capabilities, Santa can't manage to visit all kids... so he asked Rudolf to hack the sleigh for him.

I wonder if it worked.

Unfortunately, Rudolph is already on holiday. He seems to be in a strop because no one needs him to pull the sledge now. We only got this raw data file he sent us.

### Hints
- Rodolph is heavy on duty during his holiday trip, but he managed to send und at least a photo of his first step.

[![Hint 1](./3f256b4c-ea03-4239-957c-b730ae0994f4_scaled.jpg)](./3f256b4c-ea03-4239-957c-b730ae0994f4.jpg)

- Rudolf finally wants some peace and quiet on vacation. But send us one last message together with a picture: "I thought they speak 8 or 7 N1"


## Solution
Initial reaction: 🤷

The second hint pointed towards a software called [PulseView](https://sigrok.org/wiki/PulseView).

With this software I was able to open the [provided file](./SantasSleigh.raw).

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

## Links
- https://www.creationfactory.co/2021/12/reverse-engineering-laotie-ti30-scooter.html
- https://github.com/teixeluis/escooter-lcd-esc-decode
- Sigrok PulseView: https://sigrok.org/wiki/Downloads

## Flag
```
HV22{H4ck1ng_S4nta's_3-Sleigh}
```
