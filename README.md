# symphony-expense-bot-python
Demo expense report bot showcases how to use Symphony Elements and Amazon Textract


Watch the demo video below:

https://drive.google.com/file/d/1MvCYIAWjkwk5-0TbBIm6K4KCQPownU-V/view?usp=sharing

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
resources/environment.json

* Configure Bot UserID, MongoDB Credentials, and AWS IAM User Info:

```
{
  "bot_id" : "BOT ID",
  "db" : "DB NAME",
  "host": "MONGODB URI",
  "region": "us-east-1",
  "aws_access_key_id": "YOUR AWS ACCESS KEY ID",
  "aws_secret_access_key": "YOUR AWS SECRET ACCESS KEY"
}
```

# Testing

* In order to test locally, follow configuration instructions above and clone repo
* Install dependencies locally:

```
$ python3 -m venv env
$ source env/bin/activate
$ pip install -r requirements.txt

```
Navigate to expenseBot/python and run:

```
$ python3 main_rsa.py
```

# MongoDB

Connect to MongoDB via pymongo or mongoengine:

* https://docs.mongodb.com/ecosystem/drivers/pymongo/

# AWS Textract

* Create AWS IAM User Account to access AWS Features
* Leverage AWS Textract using boto3 python SDK: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/textract.html
* Check out the developers guide for using AWS Textract: https://docs.aws.amazon.com/textract/latest/dg/getting-started.html

python/processors/img_processor.py 

```
def parse_attachment(msg, bot_client):
    attachment_body = bot_client.get_message_client().get_msg_attachment(msg['stream']['streamId'], msg['messageId'],       msg['attachments'][0]['id'])
    decoded = base64.b64decode(attachment_body)
    response = client.detect_document_text(Document={'Bytes': decoded})

    text = ""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            text = text + " " + item["Text"]

    entities = comprehend.detect_entities(LanguageCode="en", Text=text)
    print(entities)
    quantity = []
    try:
        for entity in entities["Entities"]:
            if entity.get("Type", "") == 'DATE':
                date = entity.get("Text")
            if entity.get("Type", "") == 'ORGANIZATION':
                description = entity.get("Text")
                org = entity.get("Text")
            if entity.get("Type", "") == 'QUANTITY':
                quantity.append(float(entity.get("Text").lstrip('$')))
        total = max(quantity)
    except ValueError:
        bot_client.get_message_client().send_msg(msg['stream']['streamId'], MessageFormatter().format_message('Invalid price format, try again'))
    return [(org, date, total, description)]
```

# Disclaimer 

* This project was created to demonstrate how to use elements and a simple AWS Textract integration
* Note that not all receipts can be read/extracted successfuly using AWS Textract
* See the below sample receipt as one that works with the text extraction logic in python/processors/img_processor.py

![Receipt](resources/receipt.png)

