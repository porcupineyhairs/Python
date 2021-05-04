import hmac
import hashlib
import base64

timestamp = '1577262236757'
app_secret = 'JC4qK824MRqB9OhbLAA2OjwKJk_v3srOal0jGByVWNgl71AKKBUo7aBu6i0AoYGt'
app_secret_enc = app_secret.encode('utf-8')
string_to_sign = '{}\n{}'.format(timestamp, app_secret)
string_to_sign_enc = string_to_sign.encode('utf-8')
hmac_code = hmac.new(app_secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
sign = base64.b64encode(hmac_code).decode('utf-8')
print(sign)
