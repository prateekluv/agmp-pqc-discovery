AGMP PQC Discovery Toolkit – Usage Guide

This document provides practical examples of how to run the toolkit in real environments.
The goal is to help users generate meaningful discovery outputs that can be used for internal security assessments, cryptographic inventories, and PQC readiness planning.

1. Running a TLS Scan

TLS scans help identify how external or internal services are configured. This includes TLS version, cipher suite, and certificate information.

1.1 Create a targets file

Create a file such as targets.txt with hostnames and ports:

api.company.com:443
login.company.com:443
internal-gateway:8443

1.2 Run the TLS scan
python pqc_discovery.py --tls-targets targets.txt --out-prefix tls_output

1.3 Output files

This command will generate:

tls_output_tls.json
tls_output_tls.csv


These files contain one row per endpoint and include the protocol version, cipher suite, certificate subject, issuer, and validity period.

2. Running a Code Scan

Code scans help identify where cryptography is used inside applications.
This is useful when modernizing encryption, phasing out weak algorithms, or preparing for PQC migration.

2.1 Scan a source code directory
python pqc_discovery.py --code-root /path/to/source --out-prefix code_output


Examples:

python pqc_discovery.py --code-root ./backend --out-prefix backend_scan
python pqc_discovery.py --code-root ~/projects/microservice1 --out-prefix ms1_scan

2.2 Output files

The scan generates:

code_output_code.json
code_output_code.csv


Each finding contains:

File path

Language

Pattern matched

Short code snippet showing crypto usage

Use this output to begin mapping your cryptographic dependencies.

3. Combined TLS and Code Scan

The toolkit can scan both endpoints and code in the same run.

Example:

python pqc_discovery.py --tls-targets targets.txt --code-root ./app --out-prefix full_scan


This produces four files:

full_scan_tls.csv
full_scan_tls.json
full_scan_code.csv
full_scan_code.json


This is useful when assessing a complete system or microservice.

4. Using the Output for Security Reviews

The output of this tool can be used as part of:

4.1 Cryptographic Bill of Materials (CBOM)

A CBOM typically includes:

Algorithms used

Key lengths

Certificate types

Crypto libraries

Identity and signing mechanisms

The CSV and JSON files produced by the toolkit provide the starting data points.

4.2 PQC Migration Planning

The output helps identify:

Legacy or weak algorithms

Services running RSA based key exchanges

Certificates that will need replacement

Code that relies on older crypto libraries

4.3 Architecture and Design Documentation

Security teams can import the output into:

Internal dashboards

GRC or inventory systems

Architecture review documents

5. Suggestions for Larger Codebases or Environments
5.1 Exclude build directories

If your repository contains compiled or generated code, exclude those directories when running scans.

Example:

python pqc_discovery.py --code-root ./service --out-prefix service_scan


Recommended exclusions:

node_modules

build

dist

target

vendor

A future version of the tool will include configurable exclusions.

5.2 Run the tool in CI

Add the tool to your CI pipeline to automatically check for new crypto usage patterns.
This can help catch insecure implementations early.

6. Notes and Limitations

The toolkit is intentionally simple. It does not:

Validate certificate trust chains

Detect all cryptographic operations

Provide a full risk score or advisory

Parse compiled binaries

It is intended as an early stage discovery tool that you can extend based on your environment.

7. Example Workflows
7.1 Initial cryptographic inventory
python pqc_discovery.py --tls-targets external_services.txt --code-root ./platform --out-prefix inventory_v1

7.2 Weekly certificate monitoring
python pqc_discovery.py --tls-targets prod_endpoints.txt --out-prefix weekly_tls_scan

7.3 Microservice crypto audit
python pqc_discovery.py --code-root ./services/auth --out-prefix auth_crypto_audit


This document will grow as the toolkit evolves. For suggestions or improvements, please open an issue in the repository.
