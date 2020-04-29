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

    bool check(const CTzeCall& predicate, const CTzeCall& witness, const TzeContext& ctx) const {
        std::vector<uint8_t> txser;
        // TODO: serialize ctx.tx into txser
        return librustzcash_tze_verify(
                predicate.extensionId,
                predicate.mode,
                &predicate.payload[0],
                witness.extensionId,
                witness.mode,
                &witness.payload[0],
                ctx.height,
                &txser[0]);
    }

    // disable copy-constructor and assignment
    LibrustzcashTZE(LibrustzcashTZE const&) = delete;
    void operator=(LibrustzcashTZE const&)  = delete;
private:
    LibrustzcashTZE() {}
};
