from binascii import unhexlify, hexlify
from unittest import TestCase
from hashlib import sha256

import secp256k1
from bitcoin.ecc import PrivateKey, PublicKey
from bitcoin.helper import hash160
from bitcoin.script import p2wpkh_script

A = 0
B = 7
P = 2**256 - 2**32 - 977
N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141

class SECPTest(TestCase):

    def test_identity(self):
        ''' 1 * G '''
        answer = b'0479be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8'
        one = 1
        bone = one.to_bytes(32, 'big')
        g = secp256k1.ec_pubkey_create(bone)
        der = secp256k1.ec_pubkey_serialize(g, secp256k1.EC_UNCOMPRESSED)
        g_hex = hexlify(der)
        self.assertEqual(answer, g_hex)

class PrivateKeyTest(TestCase):

    def test_sign(self):
        # Test vectors produced from Justin's shitty "bedrock" library
        secret = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00d'
        msg = b'hello'
        der_sig = b'0E\x02!\x00\x96u"\x8c\xc6\xd4\xadG\x12=-\xe4HDe\xb1T\xd1\x17\xab\x02{\x01\xc5++yCMf\xdd\xd5\x02 Yg\x81(\x9akQ\xcb\x1fj\xd8H\x89\x91\x92\x8d\x87f\xa5\xc9\xe0\xc5h_b\x9ddb\x88i\x94\x14'
        sig_r = b'\xd5\xddfMCy++\xc5\x01{\x02\xab\x17\xd1T\xb1eDH\xe4-=\x12G\xad\xd4\xc6\x8c"u\x96'
        sig_s = b'\x14\x94i\x88bd\x9db_h\xc5\xe0\xc9\xa5f\x87\x8d\x92\x91\x89H\xd8j\x1f\xcbQk\x9a(\x81gY'

        private_key = PrivateKey(secret)
        msg_hash = sha256(msg).digest()
        sig = private_key.sign(msg_hash)
        self.assertEqual(sig.r, sig_r)
        self.assertEqual(sig.s, sig_s)

    def test_derive_pubkey(self):
        secret = b'\x01' * 32
        sec = b'\x03\x1b\x84\xc5V{\x12d@\x99]>\xd5\xaa\xba\x05e\xd7\x1e\x184`H\x19\xff\x9c\x17\xf5\xe9\xd5\xdd\x07\x8f'

        private_key = PrivateKey(secret)
        public_key = private_key.public_key()
        self.assertEqual(public_key.sec, sec)

class PublicKeyTest(TestCase):

    def test_constructor(self):
        valid_sec = b'\x04\x1b\x84\xc5V{\x12d@\x99]>\xd5\xaa\xba\x05e\xd7\x1e\x184`H\x19\xff\x9c\x17\xf5\xe9\xd5\xdd\x07\x8fp\xbe\xaf\x8fX\x8bT\x15\x07\xfe\xd6\xa6B\xc5\xabB\xdf\xdf\x81 \xa7\xf69\xdeQ"\xd4zi\xa8\xe8\xd1'
        invalid_sec = b'\x04\x1b\x84\xc5V{\x12d@\x99]>\xd5\xaa\xba\x05e\xd7\x1e\x184`H\x19\xff\x9c\x17\xf5\xe9\xd5\xdd\x07\x8fp\xbe\xaf\x8fX\x8bT\x15\x07\xfe\xd6\xa6B\xc5\xabB\xdf\xdf\x81 \xa7\xf69\xdeQ"\xd4zi\xa8\xe8\xd2'

        # Valid SEC shouldn't raise
        PublicKey(valid_sec)

        # Invalid SEC should raise
        with self.assertRaises(ValueError):
            PublicKey(invalid_sec)

    def test_parse(self):
        pass

    def test_serialize(self):
        pass

    def test_address(self):
        answer = 'tb1qp3hulh6ksuhhryyk6w6uvmns6l42qxymxw53t5'
        sec_pubkey = unhexlify('021ade60158012dd6f89059ee76826a96c011a6ee680df2d4566e5f226f5a3db71')
        script_pubkey = b'00140c6fcfdf56872f719096d3b5c66e70d7eaa0189b'

        script = p2wpkh_script(PublicKey(sec_pubkey))
        address = script.p2wpkh_address(testnet=True)

        self.assertEqual(answer, address)





