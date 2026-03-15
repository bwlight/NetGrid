NetGrid Master Validator
The NetGrid Master Validator is a full‑featured command‑line tool that runs all schema validators across the project. It supports fast developer workflows, CI pipelines, selective execution, quiet modes, JSON output, timing, and short‑flag combos for common actions.

Overview
The validator discovers all validate_*.py scripts inside the validators/ directory (excluding validate_all.py itself) and executes them in order. Each validator is responsible for validating a specific data domain (abilities, passives, cyberkin, status effects, etc.).

The master validator:

Runs validators individually or as a suite

Collects and consolidates errors

Prints a clean summary

Supports multiple output modes

Works in both local and CI environments

Provides short‑flag combos for fast iteration

Usage
Code
python validate_all.py [options]
Short Flags (Common Actions)
These are the flags you’ll use constantly during development. They can be combined like Unix tools:

Code
python validate_all.py -eqf
Short Flags
Short	Long	Description
-v	--validator	Run only a specific validator
-s	--skip	Skip one or more validators
-e	--only-errors	Show only error lines
-q	--quiet	Suppress live output (summary + error report only)
-c	--no-color	Disable ANSI colors
-f	--fail-fast	Stop on the first failure
-t	--timing	Show timing for each validator
Short flags can be combined:

Code
python validate_all.py -tq
python validate_all.py -cef
python validate_all.py -eq
Long Flags (Advanced Features)
These flags provide extended functionality and are kept long‑form for clarity.

Flag	Description
--json	Output results in JSON format
--summary-only	Only print the summary (no live output)
--errors-only	Only print the final error report
--list	List all validators and exit
--root	Override the project root directory
--dry-run	Show which validators would run without executing them
--ci	CI mode: quiet + fail-fast + JSON output
--exit-zero	Always exit with code 0 (useful for exploratory runs)
--strict	Treat warnings as errors (reserved for future use)
--no-legacy-skip	Validate .LEGACY folders instead of skipping them
Examples
Run everything normally
Code
python validate_all.py
Run only the abilities validator
Code
python validate_all.py -v validate_abilities.py
Run everything but hide [OK] lines
Code
python validate_all.py -e
Quiet mode (summary + error report only)
Code
python validate_all.py -q
Fail fast + timing
Code
python validate_all.py -ft
Skip specific validators
Code
python validate_all.py -s validate_status.py validate_passives.py
CI mode
Code
python validate_all.py --ci
JSON output
Code
python validate_all.py --json
Dry run (show what would run)
Code
python validate_all.py --dry-run
Output Structure
Live Output
Depending on flags, the validator prints:

Per‑validator status ([OK] / [ERROR] / [FAIL])

Colorized output (unless --no-color)

Timing (if -t)

Summary
Always includes:

Code
=== Validation Summary ===
X / Y validators passed.
Final Error Report
If any validator fails:

Code
=== Error Report ===
validate_abilities.py: [ERROR] data/abilities/...: <message>
validate_status.py: [ERROR] data/status/...: <message>
JSON Mode
When --json is used, output includes:

Validator names

Return codes

Raw output

Timing

Error list

Validator Discovery
The master validator automatically loads:

Code
validators/validate_*.py
Except:

validate_all.py (itself)

Anything inside .LEGACY unless --no-legacy-skip is used

Exit Codes
Code	Meaning
0	All validators passed OR --exit-zero was used
1	One or more validators failed
Notes
Short flags are designed for speed and can be combined.

Long flags provide clarity and advanced control.

The validator is safe for both local development and CI pipelines.