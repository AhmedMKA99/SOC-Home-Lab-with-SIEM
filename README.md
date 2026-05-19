# SOC Home Lab with SIEM

A hands-on Security Operations Centre (SOC) home lab built on the open-source SIEM platform **Wazuh**, with monitored Windows and Linux endpoints on an isolated virtual network.

This project demonstrates practical blue-team skills — SIEM deployment, endpoint telemetry, log collection, and alert triage — and is fully documented so the environment can be reproduced from scratch.

> **Status:** In progress. The lab is built and operational; attack simulations and the full written report are being completed. Build progress is tracked below.

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
- [x] Windows endpoint — Wazuh agent enrolled
- [x] Windows endpoint — Sysmon installed and forwarded to Wazuh
- [x] Linux endpoint — Wazuh agent enrolled
- [ ] Linux endpoint — auditd command monitoring configured
- [ ] Attack simulations and alert capture
- [ ] Analyst triage and incident reporting
- [ ] Full written report completed

---

## Repository Contents

| Path | Description |
|------|-------------|
| `Initial Project Overview.md` | The project's scope, objectives, milestones, and limitations |
| `docs/` | Step-by-step build documentation |
| `screenshots/` | Evidence captured during the build |
| `report/` | The formal written report (LaTeX source + compiled `main.pdf`) |

### Documentation

- [`docs/01-environment-and-architecture.md`](docs/01-environment-and-architecture.md) — lab design and network
- [`docs/02-wazuh-deployment.md`](docs/02-wazuh-deployment.md) — SIEM server deployment
- [`docs/03-windows-endpoint.md`](docs/03-windows-endpoint.md) — Windows endpoint, agent, and Sysmon

The compiled report is at [`report/main.pdf`](report/main.pdf).

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
