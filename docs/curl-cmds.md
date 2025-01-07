### Authentication
#### Authentication Req-Reply
```sh
curl -X 'POST' \
'http://localhost:8000/login' \
-H 'accept: application/json' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-d 'username=bhagavansprasad%40gmail.com&password=bjnjnuh'
```
#### Response body
```json
{
"access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJiaGFnYXZhbnNwcmFzYWRAZ21haWwuY29tIiwicm9sZXMiOlsiRklOT1BTIl0sImV4cCI6MTczNjE1Njg4OH0.BNz3ncOceypJLRr8PwTmREorebZjYAKyQQQATujaZhY",
"token_type": "bearer",
"roles": "FINOPS",
"client_id": 1,
"user_full_name": "bhagavan prasad"
}
```

### List users
```sh
curl -X GET "http://127.0.0.1:8000/users" -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYmhhZ2F2YW5zcHJhc2FkQGdtYWlsLmNvbSIsInJvbGVzIjpbIkZJTk9QUyJdLCJjbGllbnRfaWQiOjEsImV4cCI6MTczNjI1MzMzM30.M6MNR3O6iIQElTGNqNpuXsG00iyGo3znySg-7lTH7b0"
```
    Response headers
    content-length: 283 
    content-type: application/json 
    date: Mon,06 Jan 2025 04:48:08 GMT 
    server: uvicorn 

### client onboarding
```sh
curl -X 'POST' \
  'http://localhost:8000/client_onboarding' \
  -H 'Authorization: Bearer xxxxxx....EMgPO0BNG7aYMOHG8' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "b2b_distributors": [
    {
      "disty_id": 1
    },
    {
      "disty_id": 3
    },
    {
      "disty_id": 4
    }
  ],
  "accounting_tool_details": {
    "invoice_inputs": "PO",
    "invoice_number_auto": 1,
    "accounting_tool_name": "PeppyBooks",
    "accounting_tool_url": "https://peppybooks.evenflow.com",
    "accounting_tool_userid": "evenflowadmin",
    "accounting_tool_pwd": "jnjnuhuh1234"
  }
}'

```