// Copyright (c) 2009-2010 Satoshi Nakamoto
// Copyright (c) 2009-2013 The Bitcoin Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or https://www.opensource.org/licenses/mit-license.php .

#ifndef BITCOIN_MINER_H
#define BITCOIN_MINER_H

#include "primitives/block.h"

#include <boost/optional.hpp>
#include <boost/shared_ptr.hpp>
#include <stdint.h>

class CBlockIndex;
class CChainParams;
class CScript;
namespace Consensus { struct Params; };

static const bool DEFAULT_GENERATE = false;
static const int DEFAULT_GENERATE_THREADS = 1;

static const bool DEFAULT_PRINTPRIORITY = false;

class InvalidMinerAddress {
public:
    friend bool operator==(const InvalidMinerAddress &a, const InvalidMinerAddress &b) { return true; }
    friend bool operator<(const InvalidMinerAddress &a, const InvalidMinerAddress &b) { return true; }
};

typedef boost::variant<InvalidMinerAddress, libzcash::SaplingPaymentAddress, boost::shared_ptr<CReserveScript>> MinerAddress;

class KeepMinerAddress : public boost::static_visitor<>
{
public:
    KeepMinerAddress() {}

    void operator()(const InvalidMinerAddress &invalid) const {}
    void operator()(const libzcash::SaplingPaymentAddress &pa) const {}
    void operator()(const boost::shared_ptr<CReserveScript> &coinbaseScript) const {
        coinbaseScript->KeepScript();
    }
};

class IsValidMinerAddress : public boost::static_visitor<bool>
{
public:
    IsValidMinerAddress() {}

    bool operator()(const InvalidMinerAddress &invalid) const {
        return false;
    }
    bool operator()(const libzcash::SaplingPaymentAddress &pa) const {
        return true;
    }
    bool operator()(const boost::shared_ptr<CReserveScript> &coinbaseScript) const {
        // Return false if no script was provided.  This can happen
        // due to some internal error but also if the keypool is empty.
        // In the latter case, already the pointer is NULL.
        return coinbaseScript.get() && !coinbaseScript->reserveScript.empty();
    }
};

struct CBlockTemplate
{
    CBlock block;
    std::vector<CAmount> vTxFees;
    std::vector<int64_t> vTxSigOps;
};

/** Generate a new block, without valid proof-of-work */
CBlockTemplate* CreateNewBlock(const CChainParams& chainparams, const MinerAddress& minerAddress);

#ifdef ENABLE_MINING
/** Get -mineraddress */
void GetMinerAddress(MinerAddress &minerAddress);
/** Modify the extranonce in a block */
void IncrementExtraNonce(CBlock* pblock, const CBlockIndex* pindexPrev, unsigned int& nExtraNonce);
/** Run the miner threads */
void GenerateBitcoins(bool fGenerate, int nThreads, const CChainParams& chainparams);
#endif

void UpdateTime(CBlockHeader* pblock, const Consensus::Params& consensusParams, const CBlockIndex* pindexPrev);

#endif // BITCOIN_MINER_H
