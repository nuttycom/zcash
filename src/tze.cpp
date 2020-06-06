// Copyright (c) 2020 The Zcash developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or https://www.opensource.org/licenses/mit-license.php .

#include "tze.h"
#include "librustzcash.h"

/**
 * Singleton implementation of librustzcash-backed TZE
 */
class LibrustzcashTZE : public TZE {
public:
    static LibrustzcashTZE& getInstance()
    {
        static LibrustzcashTZE instance; 
        return instance;
    }

    virtual bool check(uint32_t consensusBranchId, const CTzeData& predicate, const CTzeData& witness, const TzeContext& ctx) const {
        CDataStream ss(SER_DISK, CLIENT_VERSION);
        ss << ctx.tx;

        return librustzcash_tze_verify(
                consensusBranchId,
                predicate.extensionId,
                predicate.mode,
                &predicate.payload[0],
                predicate.payload.size(),
                witness.extensionId,
                witness.mode,
                &witness.payload[0],
                witness.payload.size(),
                ctx.height,
                (unsigned char*)&ss[0],
                ss.size());
    }

    // disable copy-constructor and assignment
    LibrustzcashTZE(LibrustzcashTZE const&) = delete;
    void operator=(LibrustzcashTZE const&)  = delete;
private:
    LibrustzcashTZE() {}
};
