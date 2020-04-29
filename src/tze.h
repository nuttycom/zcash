// Copyright (c) 2020 The Zcash developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or https://www.opensource.org/licenses/mit-license.php .


#ifndef ZCASH_TZE_H
#define ZCASH_TZE_H

#include "serialize.h"
#include "primitives/transaction.h"

class TzeContext 
{
private:
    int height;
    const CTransaction& tx;

public:
    TzeContext(int heightIn, const CTransaction& txIn): tx(txIn) {
        height = heightIn;
    }

    ADD_SERIALIZE_METHODS;
    template <typename Stream, typename Operation>
    inline void SerializationOp(Stream& s, Operation ser_action) {
        READWRITE(height);
        READWRITE(tx);
    }
};

class TZE 
{
public:
    virtual bool check(const CTzeCall& predicate, const CTzeCall& witness, const TzeContext& ctx) const;
};

#endif // ZCASH_TZE_H
