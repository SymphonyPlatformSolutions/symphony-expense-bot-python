# symphony-expense-bot-python
Demo expense report bot showcases how to use Symphony Elements and Amazon Textract


Watch the demo video below:

[![Watch the video](resources/demo.png)](https://drive.google.com/file/d/1MvCYIAWjkwk5-0TbBIm6K4KCQPownU-V/view?usp=sharing)


# Configuration

## Populate Configuration Files

resources/config.json

* Set your SessionAuth URL, KeyAuth URL, Pod URL, and Agent URL respectively:

```
{
    "sessionAuthHost": "develop2.symphony.com",
    "sessionAuthPort": 443,
    "keyAuthHost": "develop2.symphony.com",
    "keyAuthPort": 443,
    "podHost": "develop2.symphony.com",
    "podPort": 443,
    "agentHost": "develop2.symphony.com",
    "agentPort": 443,
    ...
    
}
```
* Set Authentication Method and point configuration file to RSA Private Key or Certificate:

```
{
  ...
  "authType": "rsa",
  "botPrivateKeyPath": "./rsa/",
  "botPrivateKeyName": "rsa-private-karlPythonDemo.pem",
  ...
}
```

* Configure bot username and email address corresponding to the bots service account in the dedicated Pod
* Set optional truststore path

```
{
  ...
  "botUsername": "karlPythonDemo",
  "botEmailAddress": "karlPythonDemo@demo.com",
  "truststorePath": ""
}
```
