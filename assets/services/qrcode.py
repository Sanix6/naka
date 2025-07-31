import pyotp
import qrcode
import base64
from io import BytesIO

def generate_2fa_secret(user):
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=user.username, issuer_name="MyDRFApp")
    
    img = qrcode.make(uri)
    buf = BytesIO()
    img.save(buf, format='PNG')
    img_b64 = base64.b64encode(buf.getvalue()).decode()

    return secret, f"data:image/png;base64,{img_b64}"
