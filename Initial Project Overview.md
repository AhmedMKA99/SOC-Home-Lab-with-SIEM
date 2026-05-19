# Initial Project Overview (IPO)
## Project 1 — SOC Home Lab with Open-Source SIEM

_Author: Muhammad Ahmed Khalid_
_Document type: Initial Project Overview_
_Status: Planning_

---

## 1. Background & Context

Security Operations Centre (SOC) analysts spend their working day inside a Security Information and Event Management (SIEM) platform — collecting logs from across an organisation, investigating alerts, and deciding whether an event is a genuine threat or a false positive.

The problem for a graduate: almost every junior SOC analyst job description asks for SIEM familiarity (Splunk, Microsoft Sentinel, Elastic, or Wazuh), yet university degrees rarely provide hands-on SIEM time. This project closes that gap by building a working, monitored SOC environment from scratch using only free, open-source tooling.

This project also serves as the foundation for **Project 2 (Detection Engineering)** — the lab built here becomes the testing ground for that follow-on work.

---

## 2. Aim

To design, deploy, and operate a functional SOC home lab using a free open-source SIEM, capable of collecting and analysing security logs from multiple endpoints, generating alerts, and supporting a realistic analyst triage workflow.

---

## 3. Objectives

1. Deploy a Wazuh SIEM server (manager, indexer, and dashboard) on a dedicated virtual machine.
2. Configure two monitored endpoints — a Windows 10/11 VM and an Ubuntu Linux VM — each running a Wazuh agent.
3. Enable enhanced host logging: Sysmon on Windows and auditd on Linux.
4. Centralise log collection and verify successful ingestion into the SIEM dashboard.
5. Establish a baseline of normal activity for each endpoint.
6. Simulate a defined set of security events (e.g. brute-force login, unauthorised file access, suspicious process execution, new user creation).
7. Observe, investigate, and triage the resulting alerts — classifying each as true or false positive.
8. Produce at least one analyst-style incident report for a simulated scenario.
9. Document the entire build as a reproducible, recruiter-facing GitHub repository.

---

## 4. Scope

### In Scope
- One SIEM server VM (Wazuh all-in-one deployment).
- Two monitored endpoint VMs (Windows + Linux).
- Host-based monitoring: endpoint logs, file integrity monitoring, process monitoring.
- Alerting using Wazuh's built-in ruleset.
- Host-level attack simulations using safe, benign techniques.
- Full written documentation and GitHub publication.

### Out of Scope
- Network-tier detection (NIDS, full packet capture) — referenced conceptually only.
- Cloud-hosted SIEM deployment.
- Production-scale tuning, high availability, or multi-node clustering.
- Automated active response / SOAR — noted as future work.
- Real malware samples — only benign emulated behaviour is used.

---

## 5. Milestones & Indicative Timeline

Estimated duration: 5–6 weeks, part-time.

| Milestone | Description | Target |
|-----------|-------------|--------|
| M1 | Environment setup — VirtualBox, base VMs, internal network | Week 1 |
| M2 | Wazuh server deployed, dashboard accessible | Week 1–2 |
| M3 | Endpoint agents installed and reporting; Sysmon/auditd configured | Week 2–3 |
| M4 | Log ingestion verified, baseline activity established | Week 3 |
| M5 | Attack simulations executed, alerts captured | Week 4 |
| M6 | Alert triage completed, incident report written | Week 5 |
| M7 | Documentation finalised, repository published | Week 5–6 |

---

## 6. Tools & Technologies

| Category | Tool | Purpose |
|----------|------|---------|
| Virtualisation | Oracle VirtualBox | Hosts all VMs |
| SIEM / XDR | Wazuh | Log collection, correlation, alerting, dashboard |
| Endpoint OS | Windows 10/11 VM | Monitored Windows host |
| Endpoint OS | Ubuntu Linux VM | Monitored Linux host |
| Windows logging | Sysmon | Detailed process/network/file telemetry |
| Linux logging | auditd | System call and file access auditing |
| Documentation | Markdown, diagrams | Reproducible project record |

All tools are free and open-source or free-to-use.

---

## 7. Methodology

An iterative **build → test → document** approach. Each component is verified working before the next is added, and every step is documented at the time it is performed so the final repository is fully reproducible by a third party.

---

## 8. Limitations

- **Scale:** A single-machine virtualised lab cannot represent enterprise traffic volume, endpoint count, or alert noise.
- **Ruleset:** Uses Wazuh's built-in detection ruleset with limited custom tuning (custom rules are the focus of Project 2).
- **Attacks are emulated:** Simulated benign techniques are used, not live malware.
- **No network visibility:** Detection is host-based only; no firewall or NIDS telemetry.
- **Single analyst:** No shift handover, escalation tiers, or team workflow.
- **Hardware-bound:** The number of concurrent VMs is constrained by available RAM.

---

## 9. Realism

The architecture — a central SIEM receiving agent telemetry from endpoints with enhanced logging — directly mirrors how real SOC environments are built. Wazuh is genuinely deployed in industry, so the operational skills (agent management, log review, alert triage) transfer directly to a workplace.

The honest caveat is **scale and noise**: a real SOC processes orders of magnitude more data and far more false positives. The workflows and concepts demonstrated here are realistic; the volume is not. This limitation is stated openly in the project documentation rather than hidden.

---

## 10. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Insufficient host RAM for multiple VMs | Allocate resources carefully; limit concurrent VMs; 16GB host RAM recommended |
| Wazuh setup complexity / version drift | Document exact versions and every command used |
| Scope creep extending the timeline | Hold to milestone checkpoints; defer extras to future work |
| Misconfiguration breaking log flow | Verify ingestion at each stage before proceeding |

---

## 11. Future Work

- Add network-tier detection by integrating Suricata or Zeek with Wazuh.
- Integrate threat intelligence feeds for IOC enrichment.
- Add automated active response / SOAR-style playbooks.
- **Extend into Project 2 — Detection Engineering with MITRE ATT&CK** (the planned follow-on).
- Feed in a vulnerability scanner for unified visibility.

---

## 12. Expected Deliverables

- A fully documented public GitHub repository.
- A step-by-step setup and reproduction guide.
- An architecture diagram of the lab.
- Attack simulation walkthroughs with screenshots.
- At least one analyst-style incident report.
- A recruiter-facing README explaining the project and its value.

---

## 13. Success Criteria

The project is considered successful when:

- The SIEM is operational with two or more endpoints actively reporting.
- At least five distinct security events have been simulated and detected.
- Each detection is documented with triage notes and a true/false-positive classification.
- A third party can reproduce the lab by following the published guide.
