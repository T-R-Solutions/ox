# Tasks evidence fields supplement — historical product 39d517

These observations extend AC-11 only for the Tasks view. They do not replace the
integral maintained native review and do not establish all five evidence states
or native coverage for other views.

Attempt 01 failed with `timeout: surface S03` after its second navigation. The
focused path control received the keyboard shortcut. Its result, observer source,
compositor/Wayland logs and captures are retained. Separate driver streams were
not present when retention occurred; they have not been recreated.

Attempt 02 used pointer priming and the public File → Escape → Tab × 3 → Go To
anchor before the same real task producer/oracle flow. It ended naturally with
exit 0, no recorded error and no changed source inputs. The product SHA-256 was
`39d517bb89494ba73725c4da2e7e7fd8b326f1abd3c38dce21a88a3593e03f86` before and after.
The observer source is retained as `02/observer.py.bin`; its run identified the
maintained method SHA `8cc3b7c49d32a323ae7b8b03ba96d8317393e5a4ad125eb9a463309c95835ae0`.

The inspected `02/task-verified.png` shows the approved badge, criterion
`result:<task-id>:attempt-1:1`, run reference, observation time/manual freshness
note, four observed paths, task-oracle identifier and execution history with exit
0. Both root and independent review inspected the actual image. Repeated captures
may share bytes/sample receipt; they are not separate rendered-frame proofs or a
latency measurement. `frame_time` is a sample receipt time, not presentation time.

The 51 retained files and their original paths/sizes/hashes are listed in
`retention-manifest.json`. Failed observations remain failed. These results stay
bound to their historical inputs if a later UI/dependency build changes them.
