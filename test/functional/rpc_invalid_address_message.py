#!/usr/bin/env python3
# Copyright (c) 2020-present The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test error messages for 'getaddressinfo' and 'validateaddress' RPC commands."""

from test_framework.test_framework import BitcoinTestFramework

from test_framework.util import (
    assert_equal,
    assert_raises_rpc_error,
)

BECH32_VALID = 'rsmt1qtmp74ayg7p24uslctssvjm06q5phz4yr7z4gsm'
BECH32_VALID_UNKNOWN_WITNESS = 'rsmt1p424qk6hwn9'
BECH32_VALID_CAPITALS = 'RSMT1QPLMTZKC2XHARPPZDLNPAQL78RSHJ68U3FASHA5'
BECH32_VALID_MULTISIG = 'rsmt1qdg3myrgvzw7ml9q0ejxhlkyxm7vl9r56yzkfgvzclrf4hkpx9yfq4vtgyx'

BECH32_INVALID_BECH32 = 'rsmt1p0xlxvlhemja6c4dqv22uapctqupfhlxm9h8z3k2e72q4k9hcz7vq0krr2w'
BECH32_INVALID_BECH32M = 'rsmt1qw508d6qejxtdg4y5r3zarvary0c5xw7kf2krp6'
BECH32_INVALID_VERSION = 'rsmt130xlxvlhemja6c4dqv22uapctqupfhlxm9h8z3k2e72q4k9hcz7vqx7fd6q'
BECH32_INVALID_SIZE = 'rsmt1s0xlxvlhemja6c4dqv22uapctqupfhlxm9h8z3k2e72q4k9hcz7v8n0nx0muaewav25vl2afl'
BECH32_INVALID_V0_SIZE = 'rsmt1qw508d6qejxtdg4y5r3zarvary0c5xw7kqql9lxjl'
BECH32_INVALID_PREFIX = 'smt1pw508d6qejxtdg4y5r3zarvary0c5xw7kw508d6qejxtdg4y5r3zarvary0c5xw7kvv9vkc'
BECH32_TOO_LONG = 'rsmt1q049edschfnwystcqnsvyfpj23mpsg3jcedq9xv049edschfnwystcqnsvyfpj23mpsg3jcedq9xv049edschfnwystcqnsvy96d0s0'
BECH32_ONE_ERROR = 'rsmt1q049edschfnwystcqnsvyfpj23mpsg3jcpnd99m'
BECH32_ONE_ERROR_CAPITALS = 'RSMT1QPLMTZKC2XHARPPZDLNPAQL78RSHJ68U3JASHA5'
BECH32_TWO_ERRORS = 'rsmt1qax9suht3qv95sw33xavx8crpxduefdrs5kakut' # should be rsmt1qax9suht3qv95sw33wavx8crpxduefdrs5kaku3
BECH32_NO_SEPARATOR = 'rsmtq049ldschfnwystcqnsvyfpj23mpsg3jcedq9xv'
BECH32_INVALID_CHAR = 'rsmt1q04oldschfnwystcqnsvyfpj23mpsg3jcpnd99m'
BECH32_MULTISIG_TWO_ERRORS = 'rsmt1qdg3myrgvzw7ml8q0ejxhlkyxn7vl9r56yzkfgvzclrf4hkpx9yfq4vtgyx'
BECH32_WRONG_VERSION = 'rsmt1ptmp74ayg7p24uslctssvjm06q5phz4yr7z4gsm'

BASE58_VALID = 'TDGrtbYRVP3Qaki2CRpEY57VrN4CFAFFc8'
BASE58_INVALID_PREFIX = 'STnZQMnb6Sa5qsuvwgx1xVQCuPH9dnjTuE'
BASE58_INVALID_CHECKSUM = 'TDGrtbYRVP3Qaki2CRpEY57VrN4CFAFFc9'
BASE58_INVALID_LENGTH = '2VKf7XKMrp4bVNVmuRbyCewkP8FhGLP2E54LHDPakr9Sq5mtU2'

INVALID_ADDRESS = 'asfah14i8fajz0123f'
INVALID_ADDRESS_2 = '1q049ldschfnwystcqnsvyfpj23mpsg3jcedq9xv'

class InvalidAddressErrorMessageTest(BitcoinTestFramework):
    def set_test_params(self):
        self.setup_clean_chain = True
        self.num_nodes = 1
        self.uses_wallet = None

    def check_valid(self, addr):
        info = self.nodes[0].validateaddress(addr)
        assert info['isvalid']
        assert 'error' not in info
        assert 'error_locations' not in info

    def check_invalid(self, addr, error_str, error_locations=None):
        res = self.nodes[0].validateaddress(addr)
        assert not res['isvalid']
        assert_equal(res['error'], error_str)
        if error_locations:
            assert_equal(res['error_locations'], error_locations)
        else:
            assert_equal(res['error_locations'], [])

    def test_validateaddress(self):
        # Invalid Bech32
        self.check_invalid(BECH32_INVALID_SIZE, "Invalid Bech32 address program size (41 bytes)")
        self.check_invalid(BECH32_INVALID_PREFIX, 'Invalid or unsupported Segwit (Bech32) or Base58 encoding.')
        self.check_invalid(BECH32_INVALID_BECH32, 'Version 1+ witness address must use Bech32m checksum')
        self.check_invalid(BECH32_INVALID_BECH32M, 'Version 0 witness address must use Bech32 checksum')
        self.check_invalid(BECH32_INVALID_VERSION, 'Invalid Bech32 address witness version')
        self.check_invalid(BECH32_INVALID_V0_SIZE, "Invalid Bech32 v0 address program size (21 bytes), per BIP141")
        self.check_invalid(BECH32_TOO_LONG, 'Bech32 string too long', list(range(90, 108)))
        self.check_invalid(BECH32_ONE_ERROR, 'Invalid Bech32 checksum', [9])
        self.check_invalid(BECH32_TWO_ERRORS, 'Invalid Bech32 checksum', [22, 43])
        self.check_invalid(BECH32_ONE_ERROR_CAPITALS, 'Invalid Bech32 checksum', [38])
        self.check_invalid(BECH32_NO_SEPARATOR, 'Missing separator')
        self.check_invalid(BECH32_INVALID_CHAR, 'Invalid Base 32 character', [8])
        self.check_invalid(BECH32_MULTISIG_TWO_ERRORS, 'Invalid Bech32 checksum', [19, 30])
        self.check_invalid(BECH32_WRONG_VERSION, 'Invalid Bech32 checksum', [5])

        # Valid Bech32
        self.check_valid(BECH32_VALID)
        self.check_valid(BECH32_VALID_UNKNOWN_WITNESS)
        self.check_valid(BECH32_VALID_CAPITALS)
        self.check_valid(BECH32_VALID_MULTISIG)

        # Invalid Base58
        self.check_invalid(BASE58_INVALID_PREFIX, 'Invalid or unsupported Base58-encoded address.')
        self.check_invalid(BASE58_INVALID_CHECKSUM, 'Invalid checksum or length of Base58 address (P2PKH or P2SH)')
        self.check_invalid(BASE58_INVALID_LENGTH, 'Invalid checksum or length of Base58 address (P2PKH or P2SH)')

        # Valid Base58
        self.check_valid(BASE58_VALID)

        # Invalid address format
        self.check_invalid(INVALID_ADDRESS, 'Invalid or unsupported Segwit (Bech32) or Base58 encoding.')
        self.check_invalid(INVALID_ADDRESS_2, 'Invalid or unsupported Segwit (Bech32) or Base58 encoding.')

        node = self.nodes[0]


        if not self.options.usecli:
            # Missing arg returns the help text
            assert_raises_rpc_error(-1, "Return information about the given bitcoin address.", node.validateaddress)
            # Explicit None is not allowed for required parameters
            assert_raises_rpc_error(-3, "JSON value of type null is not of expected type string", node.validateaddress, None)

    def test_getaddressinfo(self):
        node = self.nodes[0]

        assert_raises_rpc_error(-5, "Invalid Bech32 address program size (41 bytes)", node.getaddressinfo, BECH32_INVALID_SIZE)
        assert_raises_rpc_error(-5, "Invalid or unsupported Segwit (Bech32) or Base58 encoding.", node.getaddressinfo, BECH32_INVALID_PREFIX)
        assert_raises_rpc_error(-5, "Invalid or unsupported Base58-encoded address.", node.getaddressinfo, BASE58_INVALID_PREFIX)
        assert_raises_rpc_error(-5, "Invalid or unsupported Segwit (Bech32) or Base58 encoding.", node.getaddressinfo, INVALID_ADDRESS)
        assert "isscript" not in node.getaddressinfo(BECH32_VALID_UNKNOWN_WITNESS)

    def run_test(self):
        self.test_validateaddress()

        if self.is_wallet_compiled():
            self.init_wallet(node=0)
            self.test_getaddressinfo()


if __name__ == '__main__':
    InvalidAddressErrorMessageTest(__file__).main()
