# AGMP PQC Discovery Toolkit – Architecture Overview

This document provides a high-level view of how the toolkit is structured and how it works internally.

---

## Core Components

### 1. TLS Scanner

File: `pqc_discovery.py`

The TLS scanner:
- Reads a list of host:port targets from a text file
- Connects to each target using Python's `ssl` and `socket` modules
- Extracts:
  - TLS protocol version
  - Cipher suite
  - Certificate subject and issuer
  - Certificate validity period
- Records any connection or handshake errors

Output is written as:
- `<prefix>_tls.csv`
- `<prefix>_tls.json`

The scanner currently ignores certificate validation and focuses on gathering information only.

---

### 2. Source Code Scanner

File: `pqc_discovery.py`

The code scanner:
- Walks the directory tree starting from a given root path
- Selects files by extension:
  - `.py`, `.js`, `.ts`, `.java`, `.go`, `.cs`
- Uses simple regular expression patterns per language to detect:
  - Imports of cryptographic libraries
  - Common crypto related functions

For each match, the scanner records:
- File path
- Language
- Pattern used
- A short snippet of surrounding code

Output is written as:
- `<prefix>_code.csv`
- `<prefix>_code.json`

---

### 3. Command Line Interface

The `main()` function in `pqc_discovery.py` provides a basic CLI:

Arguments:
- `--tls-targets`: path to a file with host:port entries
- `--code-root`: path to a source code directory
- `--out-prefix`: prefix used for output file names

At least one of `--tls-targets` or `--code-root` must be provided.

---

## Design Principles

- Keep the core tool simple and easy to run
- Prefer clear and readable code over heavy abstraction
- Avoid external dependencies where possible
- Make it easy to extend:
  - More patterns
  - More file types
  - Additional output formats

---

## Extension Points

Ideas for where to extend the toolkit:

- Add configuration files (for example: YAML or JSON) to control scanning behavior
- Add more languages and patterns
- Add modules for:
  - Certificate parsing and analysis
  - Cloud provider API calls
  - Integration with internal inventory systems

---

This document is intended as an introduction for engineers who want to understand or extend the toolkit.
