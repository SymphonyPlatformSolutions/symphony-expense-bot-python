import boto3
import base64
from .document import Document
import json

with open('./environment.json', 'r') as f:
    data = json.load(f)

client = boto3.client(
    'textract',
    aws_access_key_id=data['aws_access_key_id'],
    aws_secret_access_key=data['aws_secret_access_key'],
    region_name=data['region']
)
#aws comp
comprehend = boto3.client(
    'comprehend',
    aws_access_key_id=data['aws_access_key_id'],
    aws_secret_access_key=data['aws_secret_access_key'],
    region_name=data['region']
)
def parse_attachment(msg, bot_client):
    attachment_body = bot_client.get_message_client().get_msg_attachment(msg['stream']['streamId'], msg['messageId'], msg['attachments'][0]['id'])
    decoded = base64.b64decode(attachment_body)
    response = client.detect_document_text(Document={'Bytes': decoded})

    text = ""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            text = text + " " + item["Text"]

    entities = comprehend.detect_entities(LanguageCode="en", Text=text)
    print(entities)
    quantity = []
    for entity in entities["Entities"]:
        if entity.get("Type", "") == 'DATE':
            date = entity.get("Text")
        if entity.get("Type", "") == 'ORGANIZATION':
            description = entity.get("Text")
            org = entity.get("Text")
        if entity.get("Type", "") == 'QUANTITY':
            quantity.append(float(entity.get("Text").lstrip('$')))
    total = max(quantity)
    return [(org, date, total, description)]
