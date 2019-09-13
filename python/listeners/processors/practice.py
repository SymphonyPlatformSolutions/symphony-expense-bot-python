import boto3
client = boto3.client('textract')

response = client.analyze_document(
    Document={
        'Bytes': image,
    },
    FeatureTypes=[
        'FORMS'
    ]
)


with open(file_name, 'rb') as file:
        img_test = file.read()
        bytes_test = bytearray(img_test)
        print('Image loaded', file_name)

    # process using image bytes
    client = boto3.client('textract')
    response = client.analyze_document(Document={'Bytes': bytes_test}, FeatureTypes=['FORMS'])
