
from django.core.exceptions import ValidationError

def validate_key(pubkey):
    prefix = pubkey.strip()[0:7]
    print prefix
    if prefix != 'ssh-rsa' and prefix != 'ssh-dss':
        raise ValidationError("Key does not begin with ssh-rsa or ssh-dss.")

