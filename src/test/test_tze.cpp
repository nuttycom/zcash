// Copyright (c) 2020 The Zcash developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or https://www.opensource.org/licenses/mit-license.php .

#include "tze.h"

class MockTZE : public TZE {
public:
    static MockTZE& getInstance()
    {
        static MockTZE instance; 
        return instance;
    }

    virtual bool check(uint32_t consensusBranchId, const CTzeCall& predicate, const CTzeCall& witness, const TzeContext& ctx) const {
        return true;
    }

    // disable copy-constructor and assignment
    MockTZE(MockTZE const&) = delete;
    void operator=(MockTZE const&)  = delete;
private:
    MockTZE() {}
};
