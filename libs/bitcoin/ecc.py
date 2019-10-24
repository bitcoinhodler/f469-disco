import secp256k1

class PrivateKey:

    def __init__(self, secret):
        # check valid bytes
        self.secret = secret

    def __add__(self, other):
        raise NotImplementedError()

    def __sub__(self, other):
        raise NotImplementedError()

    def __mul__(self, other):
        raise NotImplementedError()

    def __repr__(self):
        return '<PrivateKey ...>'

    def sign(self, msg_hash):
        rs_bytes = secp256k1.ecdsa_sign(msg_hash, self.secret)
        return Signature(rs_bytes)

    def public_key(self):
        raw = secp256k1.ec_pubkey_create(self.secret)
        sec = secp256k1.ec_pubkey_serialize(raw, secp256k1.EC_COMPRESSED)
        return PublicKey(sec)

class PublicKey:

    def __init__(self, sec):
        # Check it's a valid pubkey
        secp256k1.ec_pubkey_parse(sec)
        self.sec = sec

    def __eq__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __ne__(self, other):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __truediv__(self, other):
        pass

    def x(self):
        pass

    def y(self):
        pass

    @classmethod
    def parse(self):
        pass

    def serialize(self):
        '''SEC serialization'''
        pass

class Signature:

    def __init__(self, r_and_s):
        assert len(r_and_s) == 64, 'bad signature'
        self.r = r_and_s[:32]
        self.s = r_and_s[32:]

    @classmethod
    def parse(self):
        pass

    def serialize(self):
        '''DER serialization'''
        # remove all null bytes at the beginning
        rbin = self.r.lstrip(b'\x00')
        # if rbin has a high bit, add a \x00
        if rbin[0] & 0x80:
            rbin = b'\x00' + rbin
        result = bytes([2, len(rbin)]) + rbin

        # remove all null bytes at the beginning
        sbin = self.s.lstrip(b'\x00')
        # if sbin has a high bit, add a \x00
        if sbin[0] & 0x80:
            sbin = b'\x00' + sbin
        result += bytes([2, len(sbin)]) + sbin

        return bytes([0x30, len(result)]) + result

