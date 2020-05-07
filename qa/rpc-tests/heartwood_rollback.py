#!/usr/bin/env python3
#
# Copyright (c) 2020 The Zcash developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or https://www.opensource.org/licenses/mit-license.php .

from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import (assert_equal, assert_true,
    initialize_chain_clean, start_nodes, start_node, connect_nodes_bi,
    bitcoind_processes)
from test_framework.mininode import (
    nuparams, OVERWINTER_BRANCH_ID, SAPLING_BRANCH_ID, HEARTWOOD_BRANCH_ID)

import re
import logging

HAS_SAPLING = [nuparams(OVERWINTER_BRANCH_ID, 10), nuparams(SAPLING_BRANCH_ID, 30), "-debug"]
HAS_HEARTWOOD = [nuparams(OVERWINTER_BRANCH_ID, 10), nuparams(SAPLING_BRANCH_ID, 30), nuparams(HEARTWOOD_BRANCH_ID, 50), "-debug"]

class HeartwoodRollbackTest(BitcoinTestFramework):
    def setup_chain(self):
        logging.info("Initializing test directory "+self.options.tmpdir)
        initialize_chain_clean(self.options.tmpdir, 2)

    # This mirrors how the network was setup in the bash test
    def setup_network(self, split=False):
        logging.info("Initializing the network in "+self.options.tmpdir)
        self.nodes = start_nodes(2, self.options.tmpdir, extra_args=[
                HAS_SAPLING, # The first two nodes have a correct view of the network,
                HAS_HEARTWOOD
        ])
        connect_nodes_bi(self.nodes,0,1)
        self.is_network_split=False 
        self.sync_all()

    def run_test(self):
        # Generate shared state up to the network split
        logging.info("Generating initial blocks.")
        self.nodes[0].generate(45)
        self.sync_all() 
        self.nodes[0].generate(15)
        self.nodes[1].generate(15)

        assert_true(self.nodes[0].getbestblockhash() != self.nodes[1].getbestblockhash(), "Split chains have not diverged!")

        self.nodes[0].stop()
        self.nodes[1].stop()
        bitcoind_processes[0].wait()
        bitcoind_processes[1].wait()

        # Restart the nodes, reconnect, and sync the network. This succeeds if "-reindex" is passed.
        logging.info("Reconnecting the network...")

        # expect an exception; the node will refuse to fully start because its last point of
        # agreement with the rest of the network was prior to the network upgrade activation
        self.nodes[1] = start_node(1, self.options.tmpdir, extra_args=HAS_HEARTWOOD) # + ["-reindex"])
        self.nodes[0] = start_node(0, self.options.tmpdir, extra_args=HAS_HEARTWOOD) # + ["-reindex"])
        connect_nodes_bi(self.nodes,0,1)
        self.is_network_split=False 
        self.sync_all()

        assert_true(self.nodes[0].getbestblockhash() == self.nodes[1].getbestblockhash(), "Unified network has diverged!")

if __name__ == '__main__':
    HeartwoodRollbackTest().main()
