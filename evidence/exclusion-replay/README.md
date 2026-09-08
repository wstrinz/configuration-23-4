# Independent replay of the 5,393-action exclusion join

Status: **SUPPORTED at the corrected concrete scope**. Authority remains
`INDEPENDENT_REPLAY_CANDIDATE`, with `decides=[]` and `graph_effect=NONE`.

The packet requested “Temperance 0.1.0” replay of “all 5,393 certificates.” No
package or checker with that name or version exists in the pinned workspace,
and 5,393 is the number of excluded **action loci**, not the number of separate
certificate files. The actual proof corpus combines direct action records,
shared quotient templates, and point-line duality transports. This replay
therefore used the independent standard-library checkers that are actually
retained with the evidence and explicitly records the scope revision.

Results:

| item | result |
|---|---:|
| direct action proof records replayed | 5,136 distinct IDs |
| direct-record failures | 0 |
| shared BS21 quotient templates passing | 34, covering 453 actions |
| final action-digest duality join | 5,395 primal = 5,395 dual |
| terminal exclusions | 5,393 |
| terminal positive residuals | 2, exactly E1 and E2 |
| total wall time | 835.203 seconds |

Fourteen interim capped, unresolved, or pre-duality rows are all closed by
later proof records. They are retained in `summary.json`; none is a terminal
failure. The shared-template checker’s broader universe includes eight
intentionally uncertified templates, so its internal `ALL_PASS=false` is
expected; the 34 templates used by this coverage join all pass.

The original independent duality program depends on NetworkX and cannot run
under `python -S`. The retained `duality_join_stdlib.py` replacement hash-checks
the frozen independent-census records, verifies the 5,395-element primal and
dual digest multisets and exact reciprocal cell counts, and does not claim to
recompute the canonical digests.

Primary receipts:

- `summary.json`: commands, timings, reconciliation, and scope limitations.
- `per-certificate-results.jsonl`: one row per replayed direct proof record.
- `events.jsonl`: chronological command ledger.
- `receipt-manifest.json`: hashes of generated receipts.
- `duality-join.json`: standard-library duality join.
- `run_replay.py`, `finalize_summary.py`, `duality_join_stdlib.py`: replay and
  collation code.
