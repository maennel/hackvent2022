# [HV22.25] Santa's Prophesy

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

## Description
Based on an old fairytale from Kobeliaky, Santa can provide more than presents. He can show you the future!

## Solution
The following steps were executed to get the flag:
1. Navigate to page.
2. Extract data from jpeg image.
3. Find `/upload` page using `dirbuster` or `ffuf`.
4. Create a pytorch machine learing model in [solver.py](./solver.py)
5. Upload model and see flag.

```
HOHO, the model is showing fantastic results. You can have the cookie you deserve: HV22{AA21B6AB-4520-4AD2-8016-4A9F2C371E6E}
```

## Flag
```
HV22{AA21B6AB-4520-4AD2-8016-4A9F2C371E6E}
```
