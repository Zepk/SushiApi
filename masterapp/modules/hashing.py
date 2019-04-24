import hashlib
import hmac
import base64

# Recibe el mensaje y clave, y retorna el hash para usar a modo de autenficiacion
def security_hash(message, key):
    key_b = str.encode(key)
    message_b = str.encode(message)

    digester = hmac.new(key_b, message_b, hashlib.sha1)
    signature1 = digester.digest()

    signature2 = base64.encodestring(signature1)
    signature2 = signature2.rstrip()

    return signature2.decode('UTF-8')
