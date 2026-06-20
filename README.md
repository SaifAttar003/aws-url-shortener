# AWS Serverless URL Shortener

A fully serverless URL shortener built on AWS — similar to bit.ly. Submit a long URL and get a short URL back. Visiting the short URL automatically redirects to the original.

---

## 🏗️ Architecture

```
User
  ↓
API Gateway
  ├── POST /shorten → Lambda → DynamoDB (store URL)
  └── GET /{shortCode} → Lambda → DynamoDB (lookup) → Redirect
```

---

## 🛠️ AWS Services Used

| Service | Purpose |
|---|---|
| AWS Lambda | Core logic — generate short codes, store and retrieve URLs |
| Amazon API Gateway | Expose REST API endpoints (POST and GET) |
| Amazon DynamoDB | NoSQL database to store short code → long URL mappings |
| AWS IAM | Lambda execution role with DynamoDB permissions |
| Amazon CloudWatch | Automatic Lambda execution logging |

---

## 📸 Project Screenshots

### API Gateway Resources
![API Gateway](screenshots/api-gateway-resources.png)

### Successful URL Shortening
![API Response](screenshots/api-response.png)

### DynamoDB Storing URL Mapping
![DynamoDB Items](screenshots/dynamodb-items.png)

### Lambda Function
![Lambda Function](screenshots/lambda-function.png)

### Redirect Working in Browser
![Redirect Working](screenshots/redirect-working.png)

---

## ⚙️ How It Works

**Shorten a URL (POST /shorten):**
1. User sends a POST request with a long URL
2. Lambda generates a random 6-character short code
3. Short code and long URL stored in DynamoDB
4. Returns short URL to user

**Visit a short URL (GET /{shortCode}):**
1. User visits the short URL in browser
2. API Gateway triggers Lambda with the short code
3. Lambda looks up the short code in DynamoDB
4. Returns HTTP 301 redirect to the original long URL

---

## 🚀 API Endpoints

**Base URL:**
```
https://krvmz9ynhk.execute-api.us-east-1.amazonaws.com/prod
```

**POST /shorten — Create short URL**
```bash
curl -X POST https://krvmz9ynhk.execute-api.us-east-1.amazonaws.com/prod/shorten \
  -H "Content-Type: application/json" \
  -d '{"long_url": "https://www.google.com"}'
```

Response:
```json
{
  "short_code": "tbhNAx",
  "short_url": "https://krvmz9ynhk.execute-api.us-east-1.amazonaws.com/prod/tbhNAx"
}
```

**GET /{shortCode} — Redirect to original URL**
```
https://krvmz9ynhk.execute-api.us-east-1.amazonaws.com/prod/tbhNAx
→ Redirects to https://www.google.com
```

---

## 🗄️ DynamoDB Schema

| Attribute | Type | Description |
|---|---|---|
| short_code | String (PK) | Unique 6-character code |
| long_url | String | Original long URL |

---

## 💡 Key Concepts Demonstrated

**Serverless Architecture**
No servers to manage — Lambda runs only when a request comes in. Pay only for actual usage.

**REST API Design**
POST for creating resources, GET for retrieving — proper HTTP method usage.

**NoSQL Database**
DynamoDB key-value store — perfect for fast URL lookups by short code.

**HTTP Redirects**
301 permanent redirect — browser automatically follows to original URL.

**IAM Least Privilege**
Lambda only has DynamoDB permissions it needs — nothing more.

---

## 📚 What I Learned

- Building serverless APIs with Lambda and API Gateway
- Lambda proxy integration for passing HTTP context
- DynamoDB put_item and get_item operations
- HTTP redirect responses (301) from Lambda
- Connecting API Gateway resources to Lambda functions
- Debugging Lambda using CloudWatch logs

---

## 👤 Author

**Saif Attar**
- LinkedIn: [linkedin.com/in/saif-attar-b15775346](https://linkedin.com/in/saif-attar-b15775346)
- GitHub: [github.com/SaifAttar003](https://github.com/SaifAttar003)
