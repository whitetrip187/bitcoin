#!/usr/bin/env python3
# Copyright (c) 2019-present The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.
"""Test basic signet functionality"""

from decimal import Decimal

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import assert_equal

SIGNET_DEFAULT_CHALLENGE = '5121039f9bb77d6060c9142655557c5c3396757007bf43772df4f91406d2a921a9c7a921037edd3e277bb236cb1f6108a6f0fe427a0482ed944473bd25f522fa55af6aced852ae'

# Blocks 1-10 of the default Summitcoin signet, mined with contrib/signet/miner (generate
# --set-block-time 1792800000+600*height --nbits 1e0377ae) and signed with the test-only keys in
# test/functional/data/signet_default_challenge_test_keys.txt.
signet_blocks = [
    '0000002069ceecd2ac9a8de78b3f09d84cf884705b0167af651f0b2a135c204d6a01000073b804af6a7407d0abd558742806e71b0af237efca4102edf6f1471bb0bb188458f7db6aae77031eec67100001020000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025100feffffff0200f2052a01000000160014279318e9055a62f8d0481fc9b1006e5aade52f840000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa24900473044022026c1a778dcdd1de4739c64563c46f69da66292e563ee2388e601dc62f0803dd4022076970064ac448eed147f2459005f3a7627d5557c2260c315c1a3ba0a0649af8801000120000000000000000000000000000000000000000000000000000000000000000000000000',
    '00000020df56080787455bee235475d799de8b7c4e381abdec36b40b3da716deff000000399c42d7eee688e1dc48350d33045912ef143caa56cab633a327435343916a5fb0f9db6aae77031ed9214d0001020000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025200feffffff0200f2052a01000000160014a8983f79c7773a00665bdf5f202aa5661bd931c40000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa24900473044022049ce3ddd4ad8a7e754919b7770a4b957d160309e8986a8838bbb69dd83e2948e0220430be2799146aaa81675f2031cd83c2b5059f1362e1b28d65d320cdbd5dae8f701000120000000000000000000000000000000000000000000000000000000000000000001000000',
    '00000020d23b5524d0319ff880f357b4c4eecb85b45500a0ec94f80c6df73524270200008036fbdcd43959817b3ed2add3bbb272f8633a1baa42231e51cad2d07c2da89f08fcdb6aae77031e3f1f150001020000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025300feffffff0200f2052a010000001600148d029e7023cd0e7bef49e1096a613bf8ea64b7690000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa249004730440220332cbcd1995009b865ad069c806c09a8ab6ec829ea7da2a9807de0a2bbabb391022022e8f4d64d423ecad0e436d9e8ea21f9c5589ee831164df4b9d8e80dca8b3f2401000120000000000000000000000000000000000000000000000000000000000000000002000000',
    '00000020dc09b9710e33c16a2a8e0f2290b1fd9f6832563d612b8b9eacd4e9b3bc00000098d91b1e579d2542362613f7be88f6f598c05f221292deabc3ccb1921f4b9cd360fedb6aae77031e0888080001020000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025400feffffff0200f2052a010000001600145afadf4c2443b30d7b54ec3bfda95494fc0c02910000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa249004730440220433e43f34b53a8999a2ce5957603be88f57f5e5abf1ad6458f3b14cd1ce1842d022030ad6dbe4b87fb388809452c8ecbc5368d841d9d3a712479d4afc3ee11b541ad01000120000000000000000000000000000000000000000000000000000000000000000003000000',
    '00000020ef372f5ea7099b4eb873e05830b6ab339ebaa6739e87569bb4be91055b010000c79c010973b070d66c30d54307df01b5a1e543629f425941a1f90ba5e29d6f24b800dc6aae77031eabf00e0001020000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025500feffffff0200f2052a0100000016001433e6e3485b9feee86ca228e26ab9f902c4eb15ff0000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa2490047304402204e5022cebb854a4a0f4976b25383c50e863c2d0040c00e447681e5de92c3618b022046493ad0c231ee38a12a86e3ba836c89e57bbfcacada13f23a468a42b29c30c001000120000000000000000000000000000000000000000000000000000000000000000004000000',
    '000000209631b352513f8462c8ec9eb8c7740a88062777046102e4b519f645860b03000059485a8cbc59fbe6d9037ca934c3bfe3bae370be968cfcbb476734e74aa170091003dc6aae77031e5203760001020000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025600feffffff0200f2052a010000001600149adc5450a9ca54705cd19953bbfc5eeec66a9dc30000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa2490047304402202608d574e9d66fab81bf8b908d5a405add42e1cc2a339349fd4197125673656202204d093f2c697fb0410237b8f095e39c1015491191cf7a326082eb7e664235584a01000120000000000000000000000000000000000000000000000000000000000000000005000000',
    '00000020bc86d1d4f2600da47eacdd2ebcf68bcfc0b643e57e246c51a3d6792929030000def4f8f20178d2cc439b30ee6271ba659d236876baad0ccce2141ca41582469b6805dc6aae77031e49df120001020000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025700feffffff0200f2052a01000000160014cdc333f19e73df194234f40964db53892ac1e1da0000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa2490047304402202fb0af21bae6098ddf0661f5cc6938b696f21c477841ba1ef2a1d9e8af50959c02205129445c3dd4e35ae031350b7de8116c5a4ec7e8a91f2629d001b50c74f5803501000120000000000000000000000000000000000000000000000000000000000000000006000000',
    '00000020880eea3aa68793e47f832842fc0c7929245c049dc484a0f747f5e21fa2020000d8694ba82ca9b399dca67a44ce19cf2b388cff70afeb1a2a467d6be998dc1e97c007dc6aae77031e3e7e190001020000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025800feffffff0200f2052a01000000160014c3e98402b7a2d3213dd63e1032fc6558ff668ae40000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa2490047304402200d2c4c8469438d483e6a5789a9acbe7919d4acac26061cf228017fded53ad38502207a6a5ee6668108fc938c5d6b4805a5648bf68e367b7a49768cf3ec448298335401000120000000000000000000000000000000000000000000000000000000000000000007000000',
    '00000020f4c5a14056f14f2d58fcaf4422367ef375112e68a18721fad5894fb8b7020000213fbbb99cda7900bd30032dcb02209583b84c699e5a6ae018f94350ce66482b180adc6aae77031ea044120001020000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025900feffffff0200f2052a0100000016001488530a9a98693045e301116057582a0200a0313b0000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa2490047304402201585411642ccada0d3fbd7bfc12062c43f5bbeccd6c2a91f64f1c978500c629c022036bfaa0977b4c324f978d4bd449f1ceb361c82916b46746baa5c222c23371b3e01000120000000000000000000000000000000000000000000000000000000000000000008000000',
    '000000204681a5634a63f81d6423b0ff6d913b1cf9221eb06f920ac99f2e4c3b2c030000dca20f88dcbdb6dfe20cbe5d525695509a77c0c210b37d018eb3b4bcd055ba4f700cdc6aae77031ed873050001020000000001010000000000000000000000000000000000000000000000000000000000000000ffffffff025a00feffffff0200f2052a0100000016001467115b1a91bc79ee5b4cb8b211a529903995691b0000000000000000776a24aa21a9ede2f61c3f71d1defd3fa999dfa36953755c690689799962b48bebd836974e8cf94c4fecc7daa2490047304402200ca2edba9cf6a9c18c4e5735c36b127711ed3228f89d679c79cbab1c98f38ac60220681e975f523bbd9ab27ba67e69e80857bea5bf1480decb76f6ab832c208ac50801000120000000000000000000000000000000000000000000000000000000000000000009000000',
]

class SignetParams:
    def __init__(self, challenge=None):
        # Prune to prevent disk space warning on CI systems with limited space,
        # when using networks other than regtest.
        if challenge is None:
            self.challenge = SIGNET_DEFAULT_CHALLENGE
            self.shared_args = ["-prune=550"]
        else:
            self.challenge = challenge
            self.shared_args = ["-prune=550", f"-signetchallenge={challenge}"]

class SignetBasicTest(BitcoinTestFramework):
    def set_test_params(self):
        self.chain = "signet"
        self.num_nodes = 6
        self.setup_clean_chain = True
        self.signets = [
            SignetParams(challenge='51'), # OP_TRUE
            SignetParams(), # default challenge
            # default challenge as a 2-of-2, which means it should fail
            SignetParams(challenge='5221039f9bb77d6060c9142655557c5c3396757007bf43772df4f91406d2a921a9c7a921037edd3e277bb236cb1f6108a6f0fe427a0482ed944473bd25f522fa55af6aced852ae')
        ]

        self.extra_args = [
            self.signets[0].shared_args, self.signets[0].shared_args,
            self.signets[1].shared_args, self.signets[1].shared_args,
            self.signets[2].shared_args, self.signets[2].shared_args,
        ]

    def setup_network(self):
        self.setup_nodes()

        # Setup the three signets, which are incompatible with each other
        self.connect_nodes(0, 1)
        self.connect_nodes(2, 3)
        self.connect_nodes(4, 5)

    def run_test(self):
        self.log.info("basic tests using OP_TRUE challenge")

        self.log.info('getblockchaininfo')
        def check_getblockchaininfo(node_idx, signet_idx):
            blockchain_info = self.nodes[node_idx].getblockchaininfo()
            assert_equal(blockchain_info['chain'], 'signet')
            assert_equal(blockchain_info['signet_challenge'], self.signets[signet_idx].challenge)
        check_getblockchaininfo(node_idx=1, signet_idx=0)
        check_getblockchaininfo(node_idx=2, signet_idx=1)
        check_getblockchaininfo(node_idx=5, signet_idx=2)

        self.log.info('getmininginfo')
        def check_getmininginfo(node_idx, signet_idx):
            mining_info = self.nodes[node_idx].getmininginfo()
            assert_equal(mining_info['blocks'], 0)
            assert_equal(mining_info['chain'], 'signet')
            assert 'currentblocktx' not in mining_info
            assert 'currentblockweight' not in mining_info
            assert_equal(mining_info['networkhashps'], Decimal('0'))
            assert_equal(mining_info['pooledtx'], 0)
            assert_equal(mining_info['signet_challenge'], self.signets[signet_idx].challenge)
        check_getmininginfo(node_idx=0, signet_idx=0)
        check_getmininginfo(node_idx=3, signet_idx=1)
        check_getmininginfo(node_idx=4, signet_idx=2)

        self.generate(self.nodes[0], 1, sync_fun=self.no_op)

        self.log.info("pregenerated signet blocks check")

        height = 0
        for block in signet_blocks:
            assert_equal(self.nodes[2].submitblock(block), None)
            height += 1
            assert_equal(self.nodes[2].getblockcount(), height)

        self.log.info("pregenerated signet blocks check (incompatible solution)")

        assert_equal(self.nodes[4].submitblock(signet_blocks[0]), 'bad-signet-blksig')

        self.log.info("test that signet logs the network magic on node start")
        with self.nodes[0].assert_debug_log(["Signet derived magic (message start)"]):
            self.restart_node(0)
        self.stop_node(0)
        self.nodes[0].assert_start_raises_init_error(extra_args=["-signetchallenge=abc"], expected_msg="Error: -signetchallenge must be hex, not 'abc'.")
        self.nodes[0].assert_start_raises_init_error(extra_args=["-signetchallenge=abc"] * 2, expected_msg="Error: -signetchallenge cannot be multiple values.")


if __name__ == '__main__':
    SignetBasicTest(__file__).main()
