# SOC Home Lab with SIEM

A hands-on Security Operations Centre (SOC) home lab built on the open-source SIEM platform **Wazuh**, with monitored Windows and Linux endpoints on an isolated virtual network.

This project demonstrates practical blue-team skills — SIEM deployment, endpoint telemetry, log collection, and alert triage — and is fully documented so the environment can be reproduced from scratch.

> **Status:** Complete _(last updated: 22 September 2026)_. The lab is built and operational, four attack simulations have been executed and triaged, four analyst-style incident reports have been written, and the full formal report is compiled at [`report/main.pdf`](report/main.pdf).

---

## What This Project Demonstrates

- Deploying and operating a SIEM (Wazuh) from scratch
- Configuring agent-based log collection across multiple operating systems
- Enabling detection-grade endpoint telemetry (Sysmon on Windows, auditd on Linux)
- Designing an isolated, safe lab network for security testing
- Documenting a technical build to a reproducible standard

---

## Lab Architecture

```
              Windows 11 Host — VirtualBox 7.2.8
                          |
         NAT Network "SOC-Lab" — 10.0.10.0/24 (isolated)
                          |
   ┌──────────────────────┼──────────────────────┐
   │                      │                      │
Wazuh Server      Windows Endpoint        Linux Endpoint
(SIEM/XDR)        Win 11 + Sysmon         Ubuntu + auditd
10.0.10.3         10.0.10.4               10.0.10.5
```

| VM | Role | OS |
|----|------|-----|
| Wazuh Server | SIEM — collection, correlation, alerting | Wazuh 4.14.5 |
| Windows Endpoint | Monitored host | Windows 11 + Sysmon |
| Linux Endpoint | Monitored host | Ubuntu + auditd |

---

## Build Progress

- [x] Isolated lab network designed and created
- [x] Wazuh SIEM server deployed, dashboard accessible
- [x] Windows endpoint, Wazuh agent enrolled
- [x] Windows endpoint, Sysmon installed and forwarded to Wazuh
- [x] Linux endpoint, Wazuh agent enrolled
- [x] Linux endpoint, auditd command monitoring configured
- [x] Attack simulations (4 completed) and alert capture
- [x] Incident reports written for all four simulations (INC-2026-001 to 004)
- [x] Full formal report compiled (Introduction, Literature Review, Methodology, Implementation, Evaluation, Discussion, Conclusions)

---

## Repository Contents

| Path | Description |
|------|-------------|
| `Initial Project Overview.md` | The project's scope, objectives, milestones, and limitations |
| `docs/` | Step-by-step build documentation |
| `screenshots/` | Evidence captured during the build |
| `report/` | The formal written report (LaTeX source + compiled `main.pdf`) |

### Documentation

- [`docs/01-environment-and-architecture.md`](docs/01-environment-and-architecture.md), lab design and network
- [`docs/02-wazuh-deployment.md`](docs/02-wazuh-deployment.md), SIEM server deployment
- [`docs/03-windows-endpoint.md`](docs/03-windows-endpoint.md), Windows endpoint, agent, and Sysmon
- [`docs/04-linux-endpoint.md`](docs/04-linux-endpoint.md), Linux endpoint, agent, and auditd

### Incident Reports

- [`incident-reports/INC-2026-001_Windows_Account_Creation.docx`](incident-reports/INC-2026-001_Windows_Account_Creation.docx), Windows local account creation with privilege escalation (Sim 1)
- [`incident-reports/INC-2026-002_Linux_Account_Creation.docx`](incident-reports/INC-2026-002_Linux_Account_Creation.docx), Linux local account creation with sudo privilege (Sim 2)
- [`incident-reports/INC-2026-003_Linux_Failed_Authentication.docx`](incident-reports/INC-2026-003_Linux_Failed_Authentication.docx), repeated failed sudo authentication (Sim 3)
- [`incident-reports/INC-2026-004_Windows_FIM_Detection_Gap.docx`](incident-reports/INC-2026-004_Windows_FIM_Detection_Gap.docx), FIM detection gap on the Windows hosts file (Sim 4, negative-result finding)

The compiled formal report is at [`report/main.pdf`](report/main.pdf).

---

## Tools Used

Oracle VirtualBox · Wazuh · Sysmon · auditd · Windows 11 · Ubuntu Linux

All software used is free or open-source.

---

## Note

The VM appliance and ISO files used to build the lab are **not** included in this repository — they are large and are downloaded directly from their vendors (links are in the documentation). The repository contains the project's own work: design, configuration, documentation, and the written report.

---

## Author

**Muhammad Ahmed Khalid** — BEng (Hons) Cybersecurity & Forensics

This is a self-initiated portfolio project.
