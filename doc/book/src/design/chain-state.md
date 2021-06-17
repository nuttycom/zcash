# Chain state

1. Lightweight noncontextual checks.
2. Check that the block correctly connects to its parents.
3. Height-contextual checks.
4. ConnectBlock (calls CheckBlock again)
5. CoinsView-related checks 

Chain state is the state that is mutated when a block is added to the block index
or when a rollback occurs. This is the CoinsDB database.

We have extended the CoinsDB to encompass additional forms of chainstate -
the global commitment trees and the nullifier sets.

TBD
