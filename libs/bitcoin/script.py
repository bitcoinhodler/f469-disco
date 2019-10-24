from bitcoin.helper import encode_bech32_checksum, hash160

def p2wpkh_script(pubkey):
    '''Takes a pubkey and returns the p2wpkh ScriptPubKey'''
    h160 = hash160(pubkey.sec)
    return Script(b'\x00\x14' + h160)

class Script:

    def __init__(self, raw):
        self.raw = raw

    def p2wpkh_address(self, testnet=False):
        # FIXME: more flexibly handle network prefixes
        if self.raw[:2] != b'\x00\x14' or len(self.raw) != 22:
            raise ValueError("Not P2WPKH pubkey")

        return encode_bech32_checksum(self.raw, testnet)
