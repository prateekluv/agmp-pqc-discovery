# agmp-pqc-discovery
AGMP PQC Discovery Toolkit

The AGMP PQC Discovery Toolkit is a lightweight and practical tool designed to help organizations identify where cryptography is used across their systems.
This is a foundational step for planning and executing a transition to Post-Quantum Cryptography (PQC).

Cryptography is used in many places: APIs, internal services, cloud workloads, certificates, CI/CD pipelines, and third-party integrations.
Most organizations do not have a complete inventory of where cryptography exists.
This toolkit helps you build that visibility by scanning TLS endpoints and analyzing source code for cryptographic usage.

This is an early version of the project and is meant to be extended based on your internal requirements.

Features
TLS Scanner

The toolkit can scan a list of host:port targets and extract:

TLS version

Cipher suite

Certificate subject and issuer

Certificate validity period

Connection or handshake errors

This helps identify outdated or weak configurations.

Source Code Scanner

The toolkit can walk through a source code directory and detect the use of common cryptographic libraries in:

Python

JavaScript and TypeScript

Java

Go

C#

The scanner looks for imports and patterns that indicate encryption, hashing, signing, or key generation.

Output Format

Scan results are written to CSV and JSON files:

<prefix>_tls.csv

<prefix>_tls.json

<prefix>_code.csv

<prefix>_code.json

These files can be used to build an internal Cryptographic Bill of Materials (CBOM).

Installation
git clone https://github.com/<your-username>/agmp-pqc-discovery.git
cd agmp-pqc-discovery

python3 -m venv .venv
source .venv/bin/activate   # On Windows: .venv\Scripts\activate

pip install -r requirements.txt


The toolkit currently has no external dependencies.

Usage
TLS Scan Example

Update the file examples/tls_targets.txt with hostnames you want to test.
Then run:

python pqc_discovery.py --tls-targets examples/tls_targets.txt --out-prefix scan1

Code Scan Example
python pqc_discovery.py --code-root /path/to/project --out-prefix code_scan

Combined Scan Example
python pqc_discovery.py --tls-targets examples/tls_targets.txt --code-root /path/to/project --out-prefix full_scan

Roadmap

Planned enhancements:

Add a basic quantum risk scoring model

Extract certificate key lengths and algorithms

Detect RSA or elliptic-curve usage in more detail

Add support for scanning cloud KMS configurations

Create a unified CBOM output format

Add optional HTML or dashboard-style reporting

Contributing

Contributions are welcome.
Please open an issue or a pull request to discuss improvements.

License

This project is licensed under the Apache License 2.0.
See the LICENSE file for details.

Maintained by agmppartners.com

For consulting, enterprise support, or enhancements, visit:
AGMPConsulting.com
