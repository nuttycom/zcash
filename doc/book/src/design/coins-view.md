# "Coins" view

A "coin" is a transaction output, which may be either spent or
unspent. The term "coin" is ordinarily used to refer to a transparent
output, though the "Coins" view encapsulates both transparent coins
and Sapling and Orchard notes.
TBD

## Notes

- This is the main context in which `CTxOut::IsNull()` is used. The other is a
  single spot in the mempool code. Once we've backported the
  [per-txout CoinsDB](https://github.com/bitcoin/bitcoin/pull/10195) we can
  hopefully eliminate this method.
