# OpenCode layered config (base + local -> generated)

This directory uses a layered config workflow:

- `*.base.jsonc`: shared and tracked in git
- `*.local.jsonc`: machine-local overrides and ignored by git
- `*.jsonc`: generated final output consumed by OpenCode/OMO

## Files

- `opencode.base.jsonc` (tracked)
- `opencode.local.jsonc` (ignored)
- `opencode.jsonc` (generated, ignored)
- `oh-my-opencode.base.jsonc` (tracked)
- `oh-my-opencode.local.jsonc` (ignored)
- `oh-my-opencode.jsonc` (generated, ignored)
- `merge_config.py` (tracked)
- `gen.sh` (tracked)

## Merge rules

- object: recursive merge
- array: local replaces base
- scalar: local replaces base
- optional: local `null` deletes key when `--delete-null` is used

## Usage

1. Create local files from examples:
   - `cp opencode.local.jsonc.example opencode.local.jsonc`
   - `cp oh-my-opencode.local.jsonc.example oh-my-opencode.local.jsonc`
2. Generate final configs:
   - `./gen.sh`
3. Optional flags:
   - `./gen.sh --delete-null`
   - `./gen.sh --sort-keys`

`gen.sh` runs:

- `opencode.base.jsonc` + `opencode.local.jsonc` -> `opencode.jsonc`
- `oh-my-opencode.base.jsonc` + `oh-my-opencode.local.jsonc` -> `oh-my-opencode.jsonc`

If a local file is missing, base-only generation is used.

## Direct CLI

`merge_config.py` can be called directly:

```bash
./merge_config.py \
  --base opencode.base.jsonc \
  --local opencode.local.jsonc \
  --out opencode.jsonc \
  --missing-local-ok
```

Flags:

- `--missing-local-ok`: local file is optional
- `--delete-null`: local `null` deletes object key
- `--sort-keys`: stable key ordering in output

## Minimal verification

Create test files:

```jsonc
// base
{"a": {"key1": "value1", "key2": "value2"}}
```

```jsonc
// local
{"a": {"key1": "new_value"}}
```

Run merge and verify output:

```bash
./merge_config.py --base base.jsonc --local local.jsonc --out out.json --missing-local-ok
```

Expected output:

```json
{
  "a": {
    "key1": "new_value",
    "key2": "value2"
  }
}
```

## Team workflow across devices

1. Pull tracked files (`*.base.jsonc`, scripts, README)
2. Keep per-device `*.local.jsonc` only on that device
3. Run `./gen.sh`
4. OpenCode/OMO read generated `*.jsonc`

## Discipline

- Do not hand-edit generated files:
  - `opencode.jsonc`
  - `oh-my-opencode.jsonc`
- Edit only:
  - `*.base.jsonc` for shared defaults
  - `*.local.jsonc` for machine-specific overrides

## Note on existing tracked generated files

`.gitignore` now ignores generated files, but git keeps tracking files that were already tracked.

If you want to fully enforce "generated files not in git", untrack once:

```bash
git rm --cached opencode.jsonc oh-my-opencode.jsonc
```

This removes them from version control without deleting local files.
