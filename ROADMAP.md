# AGMP PQC Discovery Toolkit – Roadmap

This document describes the planned evolution of the AGMP PQC Discovery Toolkit.  
The goal is to move from a basic discovery helper to a more complete cryptographic inventory and assessment tool.

---

## Current Version: v0.1

Scope:
- TLS endpoint scanning
- Basic source code scanning for common cryptographic libraries
- CSV and JSON output for TLS and code findings

Intended use:
- Early stage cryptographic discovery
- Building an initial Cryptographic Bill of Materials (CBOM)
- Feeding results into internal risk and architecture reviews

---

## Planned Milestones

### v0.2 – Better Insight into TLS and Certificates

- Extract certificate key lengths and algorithms
- Identify weak or legacy algorithms and key sizes
- Add basic tagging of endpoints by risk (for example: legacy, warning, modern)
- Improve error reporting for TLS connections

### v0.3 – More Accurate Code Scanning

- Add more language-specific patterns for:
  - Key generation
  - Encryption and decryption functions
  - Signature operations
- Add a configuration file to control:
  - File extensions to scan
  - Patterns per language
  - Excluded paths or directories

### v0.4 – Unified CBOM Output

- Combine TLS and code findings into a single CBOM-like JSON format
- Add identifiers for systems, services, or repositories
- Allow export of results in a format that can be stored in a central inventory system

### v0.5 – Basic Quantum Risk View

- Add a simple scoring model for findings
- Mark algorithms that are not quantum safe
- Allow grouping of results by:
  - System or application
  - Algorithm type
  - Risk level

### v0.6 and Beyond – Cloud and PQC Awareness

- Optional integrations with:
  - Cloud KMS (AWS, Azure, GCP)
  - Certificate management platforms
- Early support for identifying:
  - Hybrid or PQC related configurations where available
- Hooks to integrate with other tools:
  - Dashboards
  - SIEM or GRC systems

---

## Contribution to the Roadmap

If you have specific needs or ideas:
- Open a GitHub issue with the label `enhancement`
- Describe your use case, environment, and what you would like to see

This roadmap is a living document and will be updated as the project evolves.
