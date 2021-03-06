import unittest

try:
    from unittest.mock import patch, Mock, MagicMock, mock_open
except ImportError:
    from mock import patch, Mock, MagicMock, mock_open


class MockerTestCase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        self.mock_open = mock_open
        self.Mock = Mock
        self.MagicMock = MagicMock

        super(MockerTestCase, self).__init__(*args, **kwargs)

    def patch(self, *args, **kwargs):
        patcher = patch(*args, **kwargs)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def patch_object(self, *args, **kwargs):
        patcher = patch.object(*args, **kwargs)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def patch_multiple(self, *args, **kwargs):
        patcher = patch.multiple(*args, **kwargs)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing

    def patch_dict(self, *args, **kwargs):
        patcher = patch.dict(*args, **kwargs)
        thing = patcher.start()
        self.addCleanup(patcher.stop)
        return thing


ENCRYPTED_DATA = """
-----BEGIN PGP MESSAGE-----

hQEMA1xKO0QntlBSAQgAnojr1QGGxd3ihH7ET0mlNkfpvb4tKLySNeKFoj+DqjI2
OxtJgD+adpalSAMQD5L57ttxPWSXzhXgnbCZslxFQWYz30j3BnaNe4cV4JMuL3qF
8/1E0xpZIBIza7I8Loo7IV7fVzKdv00T6gKImQQRgPVdTrLcmHk3xX8xEwTmdIdy
ZCjk3Hnn/i5AkXjIjxJ3NiGsAyAPZWtX91PRN2X4+GuIaN7sWMCGzzOY2roZxmNb
mMRpAb7NzxORORHbWXjH/0Y09DkaqNoZVBDN0fp2bYmFClU98ULW4NlyK6xcuTkp
2c5WMeX70maRzciXC81HnfASvFYPlgm0aquTi+/rstJSAaDQIXPCL5GQX4TQ9Vyy
ni3FsO40+4UBXUm03cLiy8wWTL2OIxs3QmVY2HsUGacypZf+r3NNwV3/4bR757qj
JmNIw2541RSIoUbitA8aw7el/w==
=VRFD
-----END PGP MESSAGE-----
"""


KEYS = """
-----BEGIN PGP PUBLIC KEY BLOCK-----

mQINBFau5egBEAC9bRyIgfg/Yml+2lfvvG04AQ1EDaicgXMwAnAH9RX284hoAohx
c+dIusmAISlxXlxGSnyyYX26g8SoJUgvYxNrgleMZu8WkZ+MLFIA/1ryiEtMzK6/
n8HqE/vYYJAuAtxcfxrWlfWS+U+/p0T3xt5KCQ8oel5ziVryQrzqw2Oatcu6t+4B
pPp2WFG22lL/efCCpLlypOEimws1FEF665/hHzIpiWh7tJyDTE6CT4V8GX0XVWr3
9LwctN3bk3egD5acuRjawaouvFmIxJCJyd0cEFVIFTWVzkJB0oO/MRjBdbTW72Hc
ZT0d7WusnJaF9AhcWOujCZmYr8X+q/R8xEX8p36+FVboPERZ5F8v2O9FbK5sR75s
6wEnRKqm8pvvVwJHue9Y/TVUYrj+KQfEXOOIY+CaUN4Kz8foBAxxM/7m5SH03lPB
/jlhVt6go6Sohe294W9wtZ4KnWfy3foLAieplRkdeQIDLkwMb9Ok/bAO3AA137QR
uYcCY0dnPV1sEWABRa3UjjwIk9f+C4ydBPNRTw8bxhgGd682HiMbBdNaVx38Twv1
Z9cG9xI3lOINIMXPfFH8SROfBTf/XQNv9uWVIT0excTnQDKJy7LPCrJIA67mjaxZ
xKHiOUJj0MfzWYcxOy1cp0bFD8/TjeU+yuU7ChqpHnylSQZfCswDar99iwARAQAB
tDNQYXNzcGllIChBdXRvLWdlbmVyYXRlZCBieSBQYXNzcGllKSA8cGFzc3BpZUBs
b2NhbD6JAjkEEwEIACMFAlau5egCGy8HCwkIBwMCAQYVCAIJCgsEFgIDAQIeAQIX
gAAKCRD9+xEZC5ktDhD/EACf/cjsHt2c1BSCeGU1MWmTIcyzpyBhsgL70mshVNtl
Q24oy3+6yIN04KIwKTPLezHFAvZf3gHZy6O5nd6oaR5alWgCkfMIFWaaq9iCfn0I
dS6y82yUG6atGyT+Y1sZYCRHFTxjTmK9q48wxvDWm5IfYRglYvvwF+5Uma2fCZxz
NutwOjI1Nu2LpLHp9i+7MnMfMHt+rWg5/J+ECNr5Qg/yC3VP083kXHZbJzOz5B30
rByDjADEy36xY9VA3HTX5xhAilKLkOzyvjx8WoqQgvL4aR8MJNoJiKlwNCylsX8V
B3vu/f6w8fyJTQgmrUMF6QYZRvY15Key/1KJzEwv+W/e2mTTcLpTsQcUkQ2wRVlB
LWWJZvqYJfaCNHHuw2ps5S8nU7+6GrrmCUYa7Wkew37WM78D/B5MC20wfITuR7f5
lNd7RWAeZ4+ib39bySqjLmv9c3jPpGKWfXo50ClyixPvnKD3MWjxLYUiZrirsCaj
IxpbuVUvcntQzSlsOsJ7LWTz4XUGk9GZQ3I3/KG2M/E3LED1MZ3ykoIy0kpAyUeh
ebvSMsm2VBVli2rpFtZJ0j3+iP23Y0FeoTA1NQtHTskU3GuJ+NJCV9tpxLrHj8BH
BcbQjmMrXBvv/LgpzzYdq0NLR9yUNnfoIYbL1bbPX3H4crUFa/Ifz/7qVEyjVc/P
FbkBDQRWruXoAQgAv1Kp2FfPID6pYH+3c0vPzuc00XFaj2FkE1g8xIXpT4kRssHs
QeHznc7gZFi16fFUDwQfhNUuP9DlCMEre/Mw1T3BxlwjKRSvMFWpoXQBRwnpkH2K
Ar6LadJqO9gXtpXxhAF3TvD3+wZe2nMchQcFRLVytKjTGvh60ijWg9aQHG/MIBy8
tO5r+dsqCD6qGqfHOcR9ZoMOMbSwB7cGscQRI8y0o5CFLwvNyQ/2X5dXy6udqe6c
DUBakXzjpQqXgsXbK0QeCOHg/hHOtO6NgvSwYMffbGprX+AyW66AjvSb/EQMByyY
wpmpPT0xR9prYR1//kwAiZLwNUu8VXcfIc7LTwARAQABiQM+BBgBCAAJBQJWruXo
AhsuASkJEP37ERkLmS0OwF0gBBkBCAAGBQJWruXoAAoJEHvIIEoJS/PUhcYIAInL
/Z9vd7Lsb+o2ZPgrURynFaamMMEk3fFePdGTzHGF6XHfgi37irSVY6zfMlyI9ass
AUhpcDjv+Y3dRar7BEMf69wCUOcG/E72jKFZTYNCOVz5D7ZtFCm5IesRozIyXObO
UUOreMOdW9WurSBcxehCA/pSzy12ikwL4cJJ03GvRhutC2JnBsbcAIdrXjAAQjNE
1rCArCEK46eLi2Mp5oSch8uqPFoOxHO/TTmdQwdGQAIXxwkmi+WxKbGxSQF61HcS
lHortckq2mGCabDSajWwk9++6q/EuKtip3w+gXURfRxJjD/NNxBtQ47LbA82OKk/
Tirs3ZrP1pOuee3CG6dflg//QLo3E61pMwjFc9uBmTM9NokOiYdvj7beX9yMumgK
fJS7SFb+MTeAoTnJvifHrQI1vEY5B75EY7fkvlUJM2usXMxe16avJJTDL/HcqX4D
40/mJLCM3haKErORRJ3VX0mwo4/m77DrbrOTqKT055GAxUBaZ7d/2szStmeXuoLR
tdRXDNDtT1FS0H9Xl360bToFJJ3LS5kj1udLlotkfCKrulYlgawoN9FFij6QixDR
afRPR6d4AgAKTbqYWon76KouSPTtfRR55xlnTOpFLOjwQ1+ueg0JJiYmmvkG4NFs
bmFzKwQUO1B1bbi3c5RQ6Q9XuNJmagbKOrSdeox6cTS2RoIAN07YPjRdiHG2XhZs
E/qB3J3uUb4hcRin9bmstHBOesYc8w9tnhqLyDCtInARrbZUy3b8uigR5Y6P7uaY
oDWYlQYP9qBkfPC3Z+U41NhnTyVWX0ZU9OCtg4Lb8Jr6Mp/rz6KqSnQFLP8RLxuH
zaVdR+ifxgTCS8JTacWcr44Y4vFpMOSXWaWZ2Ri/GOJ+Wy2/H6ncfAnLPH8FDHJF
l0TEbbTPqYoNqLWavWTX/BMNeDfVzU/qB6hl0epJ6a4ukHIdlRVl+Si0gpJC8R+S
XLmP9lW6CbPxaxakiBAYktZlEQ8RhqTDPFgJ1D0o4Xi3+HuMayHMHk+IzmlhZU2+
3YM=
=AYMH
-----END PGP PUBLIC KEY BLOCK-----
-----BEGIN PGP PRIVATE KEY BLOCK-----

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
Tb7dgw==
=v8Tb
-----END PGP PRIVATE KEY BLOCK-----
"""


def create_keys(passphrase, path, key_length=4096):
    if path:
        with open(path, 'w') as keysfile:
            keysfile.write(KEYS)
    else:
        return KEYS
