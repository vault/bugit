
from django.core.exceptions import ValidationError
import base64

def validate_key_format(pubkey):
    prefix = pubkey.split(' ')[0]
    print prefix
    if prefix != 'ssh-rsa' and prefix != 'ssh-dss':
        raise ValidationError("Key does not begin with ssh-rsa or ssh-dss.")


def validate_key_decode(pubkey):
    data = pubkey.split(' ')[1]
    try:
        base64.b64decode(data)
    except TypeError:
        raise ValidationError("Key contains invalid data. Check that you copied it correctly.")

