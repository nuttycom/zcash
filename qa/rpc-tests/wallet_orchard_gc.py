#!/usr/bin/env python3
# Copyright (c) 2022 The Zcash developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://www.opensource.org/licenses/mit-license.php .

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import (
    NU5_BRANCH_ID,
    assert_equal,
    get_coinbase_address,
    nuparams,
    start_nodes,
    stop_nodes,
    wait_bitcoinds,
    wait_and_assert_operationid_status,
)

from decimal import Decimal

# Test wallet behaviour with the Orchard protocol
class WalletOrchardGCTest(BitcoinTestFramework):
    def __init__(self):
        super().__init__()
        self.num_nodes = 4

    def setup_nodes(self):
        return start_nodes(self.num_nodes, self.options.tmpdir, [[
            nuparams(NU5_BRANCH_ID, 201),
        ]] * self.num_nodes)

    def run_test(self):
        # Sanity-check the test harness
        assert_equal(self.nodes[0].getblockcount(), 200)

        # Generate enough blocks to activate and have a full set
        # of checkpoints at the zero bridge length.
        self.sync_all()
        self.nodes[0].generate(110)
        self.sync_all()

        # Send some funds to our Orchard address.
        acct0 = self.nodes[0].z_getnewaccount()['account']
        ua0 = self.nodes[0].z_getaddressforaccount(acct0, ['sapling', 'orchard'])['address']
        recipients = [{"address": ua0, "amount": Decimal('12.5')}]
        myopid = self.nodes[0].z_sendmany(get_coinbase_address(self.nodes[0]), recipients, 1, 0, 'AllowRevealedSenders')
        wait_and_assert_operationid_status(self.nodes[0], myopid)

        # Mine the tx 
        self.sync_all()
        self.nodes[0].generate(1)
        self.sync_all()

        assert_equal(
                {'pools': {'orchard': {'valueZat': 12_5000_0000}}, 'minimum_confirmations': 1},
                self.nodes[0].z_getbalanceforaccount(acct0))

        # Split the network
        self.split_network()

        self.sync_all()
        self.nodes[0].generate(1)
        self.nodes[2].generate(10)
        self.sync_all()

        self.join_network()

        assert_equal(
                {'pools': {'orchard': {'valueZat': 12_5000_0000}}, 'minimum_confirmations': 1},
                self.nodes[0].z_getbalanceforaccount(acct0))

        # Send to a new orchard-only unified address
        acct1 = self.nodes[1].z_getnewaccount()['account']
        ua1 = self.nodes[1].z_getaddressforaccount(acct1, ['orchard'])['address']
        recipients = [{"address": ua1, "amount": Decimal('0.5')}]
        myopid = self.nodes[0].z_sendmany(ua0, recipients, 1, 0)
        wait_and_assert_operationid_status(self.nodes[0], myopid)

        self.sync_all()
        self.nodes[0].generate(1)
        self.sync_all()

        assert_equal(
                {'pools': {'orchard': {'valueZat': 12_0000_0000}}, 'minimum_confirmations': 1},
                self.nodes[0].z_getbalanceforaccount(acct0))

        assert_equal(
                {'pools': {'orchard': {'valueZat': 5000_0000}}, 'minimum_confirmations': 1},
                self.nodes[1].z_getbalanceforaccount(acct1))

if __name__ == '__main__':
    WalletOrchardGCTest().main()

