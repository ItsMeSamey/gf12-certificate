# CLI maintenance checks for v0.1.1

The maintenance fix handles a Python process started with unavailable stdin. On the verified CPython 3.14.8 Linux environment, closing file descriptor 0 before execution makes `sys.stdin` equal to `None`. The CLI now returns structured `input_error` JSON and exit 2 for that condition.

The independent reviewer ran the following five cases through subprocess calls on the sealed checker. These POSIX shell commands reproduce the same inputs from the package directory. Each error case intentionally returns a nonzero status; run commands individually if your shell exits on errors.

| Case | Command | Expected result |
| --- | --- | --- |
| Unavailable stdin | `python3 -I -S -B gf12_checker.py - <&-` | Exit 2, `input_error`, `file_io`, message `Standard input is unavailable` |
| Empty readable stdin | `python3 -I -S -B gf12_checker.py - </dev/null` | Exit 2, `invalid_certificate`, `json_syntax` |
| Missing file | `python3 -I -S -B gf12_checker.py /path/to/nonexistent-certificate.json` | Exit 2, `input_error`, `file_io` |
| Directory input | `python3 -I -S -B gf12_checker.py .` | Exit 2, `input_error`, `file_io` |
| Valid stdin | `python3 -I -S -B gf12_checker.py - <certificate.json` | Exit 0, `verified`, 144 basis pairs, zero mismatches |

Choose a missing-file path that actually does not exist. All five cases should produce one JSON report on stdout and no stderr. File-error message text depends on the operating system and supplied path. The unavailable-stdin message is fixed by the checker.

The retained verification compared empty-readable and valid-stdin stdout byte-for-byte with prior accepted outputs on the same interpreter. Python version metadata varies across interpreters, so a different version can produce different report bytes while retaining the same certificate result. See `CLI_VERIFICATION.json` for the tested identities and outcomes.

The 35-case suite was not rerun. The single valid-stdin regression evaluated all 144 basis pairs and reused the prior positive output as its expected result.
