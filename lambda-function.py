import json
import boto3
import string
import random

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('url-shortener')

def generate_short_code():
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=6))

def lambda_handler(event, context):
    print("Event:", json.dumps(event))

    http_method = event.get('httpMethod') or event.get('requestContext', {}).get('http', {}).get('method', '')
    path = event.get('path', '')

    # POST /shorten — create short URL
    if http_method == 'POST' and 'shorten' in path:
        try:
            body = json.loads(event.get('body', '{}'))
        except:
            body = {}

            long_url = body.get('long_url')

            if not long_url:
                return {
            'statusCode': 400,
            'body': json.dumps({'error': 'long_url is required'})
        }

        short_code = generate_short_code()

        table.put_item(Item={
            'short_code': short_code,
            'long_url': long_url
        })

        return {
            'statusCode': 200,
            'body': json.dumps({
                'short_code': short_code,
                'short_url': f"https://krvmz9ynhk.execute-api.us-east-1.amazonaws.com/prod/{short_code}"
            })
        }

        # GET /{shortCode} — redirect to long URL
    elif http_method == 'GET':
        short_code = event.get('pathParameters', {}).get('shortCode')

        if not short_code:
                    return {
                'statusCode': 400,
                'body': json.dumps({'error': 'shortCode is required'})
            }

        response = table.get_item(Key={'short_code': short_code})
        item = response.get('Item')

        if not item:
                return {
            'statusCode': 404,
            'body': json.dumps({'error': 'URL not found'})
        }

        return {
            'statusCode': 301,
            'headers': {'Location': item['long_url']},
            'body': ''
        }

        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'Invalid request', 'method': http_method, 'path': path})
        }