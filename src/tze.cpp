// Copyright (c) 2020 The Zcash developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or https://www.opensource.org/licenses/mit-license.php .

#include "tze.h"
#include "librustzcash.h"

/**
 * Singleton implementation of librustzcash-backed TZE
 */
class LibrustzcashTZE : TZE {
public:
    static LibrustzcashTZE& getInstance()
    {
        static LibrustzcashTZE instance; 
        return instance;
    }

    bool check(const CTzeCall& predicate, const CTzeCall& witness, const TzeContext& ctx) const {
        return false;
    }

    // disable copy-constructor and assignment
    LibrustzcashTZE(LibrustzcashTZE const&) = delete;
    void operator=(LibrustzcashTZE const&)  = delete;
private:
    LibrustzcashTZE() {}
};
