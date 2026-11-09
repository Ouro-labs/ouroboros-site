# Current release gate

`python docs-src/verify-release-content.py` is the Pages pre-build gate. It
requires a separately reviewed `release-evidence.json` and exactly four regular
files in root `release-review/`: `semantic-review.md`, `outbound-review.md`,
`mac-codex.md`, and `validation.md`. These root files are outside the deployed
`site/` and outside the pending input inventory, so the verifier checks their
exact set and bytes separately. No real approval record is provided yet: its
absence intentionally blocks deployment. Missing approval has no fallback.

Legacy `verify-content.py`, `link_evidence.py`, and historical evidence stay
unchanged. The semantic manifest flag remains false and historical review
statuses remain pending. The new approval authorizes the current input snapshot;
it does not retrospectively approve those historical records. Sync still emits
pending inputs. The user must separately approve merge/deployment.

## Record contract (not an approval template)

The verifier constants `REPORTS` and `CHECKS` are the exact schema authority.
The record has only these keys:

- `schema`: integer 1; `scope`: `documentation-release-current-snapshot`;
  `status`: `approved` only after actual independent review.
- `baseline_snapshot_sha256`: the fixed original 413-input pending snapshot
  `5c15731dd3c8a7cb7c4f6bf851b50494641185db45443bba884376ce2276c660`.
  This is a provenance label, not an assertion that it was approved.
- `snapshot_sha256`: SHA256 of the final pending snapshot's exact bytes.
  The input count increases when this verifier, tests and documentation are added.
- `generator_sha256`: must match the final snapshot's generator metadata.
- `reviews`: exactly `semantic`, `outbound`, `mac_codex`, `validation`. Each has
  only `status`, `reviewer`, `reviewed_at_utc` (valid UTC `YYYY-MM-DDTHH:MM:SSZ`),
  `snapshot_sha256`, `report_sha256`, and `checks`. Status must be approved,
  target snapshot must match, report bytes must match, and each required check
  must be `pass`. Do not put `pass` against unobserved or failed requirements.
- `other_hosts`: nonempty list of unique `{host, status: followup, reason}`
  records listing remaining supported host paths. Mac Codex cannot be deferred:
  its installation, manual discovery/read, product first task, results, actual
  model use and three diagnosis scenarios must be evidenced in its report.

Semantic/outbound reviewers must cover historical unresolved review decisions
and later changes, not merely the final four pages. Reports identify exact
revisions, reviewed contexts, reused evidence and impact, unresolved findings,
and limitations. Validation covers full tests, strict build, search/export/
sitemaps, canonical sync, desktop/mobile/keyboard change impact, and public
information exposure. This does not require an unsupported claim of complete
screen-reader or every-browser testing. Mac evidence distinguishes real product
worker/model use from synthetic/manual/proxy observations. Raw private paths,
credentials and user DB contents must not be copied into public reports.

## Finalization order and limits

Finish implementation and test edits, verify canonical sync and tests, capture
a new pending snapshot, and rerun input-bound validation. Review that exact
snapshot and write actual report/approval records only after independent semantic
review and Mac confirmation. Root evidence files avoid a hash cycle with the
snapshot; they are themselves reviewed in the final PR. A new input invalidates
the old release approval even if the pending snapshot is recaptured. Do not
restore approval by mechanically rebinding hashes. Failed validation blocks
upload; the remaining build/export steps must still pass on the same checkout.

The release verifier checks actual current pending inputs and the full historical
pending child, then rechecks inputs/reports after the child. It neither locks the
filesystem nor proves reviewer identity, truthfulness, independence, or actual
model behavior from JSON strings. Signed identity infrastructure is not added.
Repository review/protected-main controls and the user's deployment decision
remain the trust boundary. A party able to rewrite code, approval and reports
can fabricate an internally consistent record; hashes do not prevent that.

Public CI can verify generator metadata, not rerun a private canonical repo or
Mac trial. The local canonical workspace check and private raw evidence need
separate receipts bound to the reviewed snapshot/source revisions. Generated
`site/docs/` is excluded from the input snapshot: strict build and post-build
checks/output receipts cover rendered output. The baseline digest is fixed
provenance; historical byte integrity is enforced by the unchanged pending chain.

The tests use clearly labelled synthetic approvals only inside disposable test
fixtures to exercise the technical success path. They do not create approval
files in the real worktree and do not authorize publication.
