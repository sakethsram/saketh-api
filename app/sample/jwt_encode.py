import jwt
import datetime
import time

def jwt_generate_token(payload, key, algo):
    token = jwt.encode(payload, key, algorithm=algo)

    print(token)

    return token

def jwt_decode_token(token, secret_key, algo):
    decoded_payload = None
    try:
        # Decode the token
        decoded_payload = jwt.decode(token, secret_key, algorithms=algo)

        print(decoded_payload)
    except jwt.ExpiredSignatureError:
        print('Token has expired')
    except jwt.InvalidTokenError:
        print('Invalid token')
        
    return decoded_payload

# Define your secret key
secret_key = 'abcd!234'
algoritham = 'HS256'

payload = {
    'username': "bhagavansprasad@gmail.com",
    'client': 'johndoe',
    'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=10)  # Token expires in 1 hour
}
    
def main():
    print(f"payload :{payload}")
    token = jwt_generate_token(payload, secret_key, algoritham)
    print(f"token :{token}")

    for i in range(1, 12):
        decoded_value = jwt_decode_token(token, secret_key, [algoritham])
        print(f"decoded value :{decoded_value}")
        print(f"{i}. Sleeping...")
        time.sleep(1)
        print()

if __name__ == "__main__":
    main()