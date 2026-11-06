# Review and undo settings GUI changes

Use this guide when editing configuration in the Ouroboros settings GUI. It describes the save and Undo behavior in public product main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0). A host plugin, published package, and server or CLI on your machine can be different versions; check the installed help before relying on these details.

## Before changing a setting

The GUI is opened by running `ouroboros config` in the CLI environment. Depending on the environment, it can open a terminal UI or a browser-served interface. Confirm that this is the machine, user, and configuration directory used by the host or server you intend to change. A standalone CLI may read a different configuration from a host-launched MCP server.

Review the current value and the setting's meaning before editing. Some settings affect new sessions or require an MCP server reconnect. Saving configuration does not by itself prove the running host has reloaded it.

## Save, then verify

1. Make the intended edits and select **Save**. The GUI stages edits until this action; no changes reports `No changes to save.`
2. Read the result. On success, the status line reports `Saved.` and summarizes changed values. For backend-related settings it warns that changes apply to new sessions and says to reconnect the MCP server to pick them up now.
3. Confirm the intended setting in the same configuration context. If the change should affect a host server, reconnect that server as appropriate and verify its actual tool/connection state. A saved value alone does not establish that a host reloaded it.

The GUI validates key paths against the shared configuration schema, writes the YAML, and then calls the configuration loader to check the resulting configuration. If a previous `config.yaml` existed, only after that validation and a successful temporary backup write does this save replace `config.yaml.bak` with the previous file bytes. Thus a successful GUI save advances the one-step Undo snapshot. If there was no previous configuration file, the GUI has no old file bytes to place in that backup.

## If Save reports an error

Read the full error text. For write or post-write validation errors, the GUI attempts to restore the previous configuration bytes; when there was no previous file, it attempts to remove the newly created file. A message beginning `Configuration rolled back.` reports that this restoration attempt completed. The error itself still needs correction before another save.

If the message says `Configuration rollback also failed`, do not assume the current file is either the old or new valid configuration. Preserve the error and stop further writes. Check the actual configuration file and existing `.bak` in the correct user's configuration directory, and get help before retrying or invoking Undo. This message means the attempted restoration raised its own I/O error; it does not establish which bytes remain on disk. The GUI's temporary backup cleanup also suppresses cleanup errors, so absence of a reported cleanup error is not evidence that every filesystem operation was fault-free.

Key-path and nested-section errors are rejected before the write phase. A failed validation or save does not intentionally advance the Undo snapshot; however, the source does not provide a general filesystem transaction or a guarantee that every possible hardware, process termination, or concurrent-write failure is recovered. Do not promise rollback beyond the error actually reported.

## Undo and the command-line `config set` path

`ouroboros config undo` first checks that both files exist and that the backup is UTF-8, then writes the backup bytes to `config.yaml` and asks the configuration loader to validate the new file. Only after that validation succeeds does it write the previous current bytes to `.bak`, so running Undo again redoes the change. If validation fails, the command attempts to restore the current file bytes and aborts. Review the target directory and backup before using it: Undo affects the whole configuration file, not just the field changed most recently.

However, Undo is not a filesystem transaction. It writes the backup bytes to `config.yaml` **before** validating them; on a validation error it attempts to rewrite the previous current bytes. Only after validation succeeds does it write those previous bytes directly to `.bak`. If either write raises an I/O error, the command has no complete rollback around that write. In particular, failure of the final `.bak` write can leave the configuration already changed while the backup is uncertain. An error, interruption, or missing success message does not establish that Undo left both files unchanged.

In main `592c667f`, `ouroboros config set KEY VALUE` is a distinct write path. It validates the key and value, then calls `_save_config` **outside** the `try` that wraps the later loader validation. `_save_config` writes directly to the target file. A write error can therefore happen before validation rollback begins. If the post-write loader validation fails, the command attempts to restore the previous bytes, but that restoration write is not itself guarded; an I/O error there can leave the result uncertain. The command does **not** advance the GUI's `config.yaml.bak` snapshot on a successful set. A later Undo can therefore restore the previous successful GUI backup rather than undoing the most recent `config set`. The command path also performs its own key/value parsing and event-store path check; do not assume every detail of the GUI batch save is shared.

Before using Undo or `config set`, preserve **both** the current `config.yaml` and `config.yaml.bak` in a separate, access-controlled location if they exist. They may contain credentials or private settings. If either operation reports an I/O error, stops unexpectedly, or its result is unclear, do not immediately repeat it or run Undo as a second guess. Keep the original files and error, inspect the actual current config and backup, and determine which version is valid before deciding on recovery. A normal swap is expected only when the command reports success; the source does not guarantee recovery from write failures, process interruption, or storage errors. For scripted edits, inspect the exact setting, current value, installed version, and Undo backup before choosing `config set`.

## Evidence and scope

This guide follows the public main [`592c667f`](https://github.com/Q00/ouroboros/tree/592c667f076c3dad7ef68d7844e91480d80135d0): [settings GUI persistence](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/config_tui/persistence.py), [GUI save and status message](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/config_tui/app.py), [CLI config commands](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/src/ouroboros/cli/commands/config.py), and [CLI reference](https://github.com/Q00/ouroboros/blob/592c667f076c3dad7ef68d7844e91480d80135d0/docs/cli-reference.md). These claims are static source comparisons, not a live GUI or fault-injection test. No user's configuration was read or changed. Compatibility with historical guide source `722172ef`, published release `0.59.9`, actual host reload behavior, and rollback under real disk/process failures was not tested. Check the installed command help and inspect the actual files before taking action.
