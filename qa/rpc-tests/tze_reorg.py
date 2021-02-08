#!/usr/bin/env python3
# Copyright (c) 2014-2016 The Bitcoin Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://www.opensource.org/licenses/mit-license.php .

#
# Test re-org scenarios with a mempool that contains TZE transactions
# that spend (directly or indirectly) coinbase transactions.
#

from test_framework.test_framework import BitcoinTestFramework
from test_framework.authproxy import JSONRPCException
from test_framework.util import (
    assert_equal, 
    assert_raises, 
    start_node, 
    connect_nodes, 
    nuparams,
    BLOSSOM_BRANCH_ID,
    HEARTWOOD_BRANCH_ID,
    CANOPY_BRANCH_ID,
    FUTURE_BRANCH_ID,
)


class TzeReorgTest(BitcoinTestFramework):
    def __init__(self):
        super().__init__()
        self.num_nodes = 4
        self.setup_clean_chain = True

    alert_filename = None  # Set by setup_network

    def start_node_with(self, index, extra_args=[]):
        args = [
            nuparams(BLOSSOM_BRANCH_ID, 1),
            nuparams(HEARTWOOD_BRANCH_ID, 2),
            nuparams(CANOPY_BRANCH_ID, 3),
            nuparams(FUTURE_BRANCH_ID, 4),
            "-nurejectoldversions=false",
            "-printtoconsole",
        ]
        return start_node(index, self.options.tmpdir, args + extra_args)

    def setup_network(self):
        self.nodes = []
        self.nodes.append(self.start_node_with(0))
        self.nodes.append(self.start_node_with(1))
        self.nodes.append(self.start_node_with(2))
        self.nodes.append(self.start_node_with(3))
        connect_nodes(self.nodes[1], 0)
        self.is_network_split = False
        self.sync_all()

    def create_tx(self, from_txid, amount):
        print("Creating a new transaction")
        tx = CTransaction()
        tx.vin = [CTxIn(outpoint = COutPoint(from_txid, 0))]
                
        # Demo predicate
        tze_p = bytes([
            0xd2, 0x3c, 0x00, 0xda, 0xc4, 0x47, 0x39, 0xd7,
            0x0b, 0x25, 0x04, 0xc4, 0xf3, 0xe7, 0x1a, 0x68,
            0xdb, 0x92, 0x3b, 0x30, 0xde, 0x5a, 0x09, 0x72,
            0x10, 0xf7, 0x4e, 0xe5, 0x2f, 0x53, 0x94, 0xb8 ])
        
        tx.tzeout = [CTzeOut(nValue = amount, predicate = CTzeData(extensionId=0, mode=0, payload=tze_p))]
        rawtx = tx.serialize().hex()

        print("Attempting to sign transaction")
        signresult = self.nodes[0].signrawtransaction(rawtx)
        assert_equal(signresult["complete"], True)
        f = io.BytesIO(unhexlify(signresult['hex']))

        tx.deserialize(f)
        tx.rehash()
        return tx

    def run_test(self):
        print("Test is running.")
        # Mine blocks into the zfuture zone.
        # 101, 102, and 103 are spend-able.
        new_blocks = self.nodes[1].generate(6)
        self.sync_all()

        b = [ self.nodes[0].getblockhash(n) for n in range(1, 6) ]
        coinbase_txids = [ self.nodes[0].getblock(h)['tx'][0] for h in b ]

        self.split_network()

        # Generate a new TZE transaction
        print("mining transaction on node 0")
        spend_101_raw = self.create_tx(coinbase_txids[1], 10)
        spend_101_id = self.nodes[0].sendrawtransaction(spend_101_raw)

        # Check that we have the tx in the mempool
        assert_equal(set(self.nodes[0].getrawmempool()), set([ spend_101_id ]))

        # Mine the TZE transaction
        self.nodes[0].generate(1)
        self.sync_all()

        # The transaction should no longer be in the mempool
        assert_equal(set(self.nodes[0].getrawmempool()), set())

        # mine some blocks on node 2 - this should cause a reorg on node 1
        # when we re-join the network
        last_block = self.nodes[2].generate(3)
        self.sync_all()

        # re-join the network - the transaction should be rolled back
        self.join_network()

        # Check that the spend has been returned to the mempool on node 0
        assert_equal(set(self.nodes[0].getrawmempool()), set([ spend_101_id ]))
        self.sync_all()

        # mempool should be empty.
        assert_equal(set(self.nodes[0].getrawmempool()), set())

if __name__ == '__main__':
    TzeReorgTest().main()
