# 01 — Environment & Architecture

This document describes the lab architecture, the network design, and the host environment the SOC home lab is built on.

---

## Host Environment

| Component | Specification |
|-----------|---------------|
| CPU | AMD Ryzen 5 8400F — 6 cores / 12 threads |
| RAM | 16 GB |
| Storage | ~297 GB free |
| Host OS | Windows 11 |
| Hypervisor | Oracle VirtualBox 7.2.8 |

Because the host has 16 GB of RAM, the lab is operated with the SIEM server plus **one** endpoint running at a time during heavy work. Both endpoints can run together for lighter tasks. This is a deliberate resource-management decision, not a limitation of the design.

---

## Lab Architecture

The lab consists of three virtual machines on a single isolated network:

```
                 ┌─────────────────────────────┐
                 │   Windows 11 Host (16 GB)   │
                 │   VirtualBox 7.2.8          │
                 └──────────────┬──────────────┘
                                │
              NAT Network "SOC-Lab" — 10.0.10.0/24
                                │
        ┌───────────────────────┼───────────────────────┐
        │                       │                       │
┌───────▼────────┐    ┌─────────▼────────┐    ┌──────────▼────────┐
│  Wazuh Server  │    │ Windows Endpoint │    │  Linux Endpoint   │
│  (SIEM/XDR)    │    │  Windows 11 +    │    │  Ubuntu 26.04 +   │
│  Wazuh 4.14.5  │    │  Sysmon + agent  │    │  auditd + agent   │
└────────────────┘    └──────────────────┘    └───────────────────┘
     collects  ◄───────── log telemetry ──────────►  sends
```

| VM | Role | OS | Planned RAM |
|----|------|-----|-------------|
| Wazuh Server | SIEM — collects, correlates, alerts | Wazuh 4.14.5 OVA appliance | 6 GB |
| Windows Endpoint | Monitored host | Windows 11 | 4 GB |
| Linux Endpoint | Monitored host | Ubuntu 26.04 Desktop | 2 GB |

---

## Network Design

A dedicated VirtualBox **NAT Network** named `SOC-Lab` is used for the entire lab.

| Property | Value |
|----------|-------|
| Network name | SOC-Lab |
| Subnet | 10.0.10.0/24 |
| Gateway | 10.0.10.1 |
| DHCP | Enabled |
| IPv6 | Disabled |

### Why a NAT Network?

- **VM-to-VM communication** — endpoints can reach the Wazuh server to send telemetry.
- **Internet access** — VMs can download updates and agent packages.
- **Isolation** — the lab is walled off from the host's real home network. This matters because the lab is used to simulate attacks; that activity must never touch a production network.

Dashboard access from the host browser is provided by a single port-forwarding rule (documented in `02-wazuh-deployment.md`).

### Planned Addressing

DHCP assigns addresses in the 10.0.10.0/24 range. The actual address of each VM is recorded as it is built. The Wazuh server address, once known, becomes the address every agent is pointed at.

| VM | Address |
|----|---------|
| Gateway | 10.0.10.1 |
| Wazuh Server | 10.0.10.3 |
| Windows Endpoint | 10.0.10.4 |
| Linux Endpoint | _to be recorded_ |

---

## Tooling Summary

| Tool | Version | Role |
|------|---------|------|
| Oracle VirtualBox | 7.2.8 | Hypervisor |
| Wazuh | 4.14.5 (OVA) | SIEM / XDR platform |
| Ubuntu Desktop | 26.04 | Linux endpoint OS |
| Windows | 11 | Windows endpoint OS |
| Sysmon | latest | Enhanced Windows logging |
| auditd | distro default | Linux system auditing |

---

## Build Sequence

1. **Environment & network** — VirtualBox + the `SOC-Lab` NAT Network _(this document)_.
2. **Wazuh server** — import and boot the OVA, access the dashboard.
3. **Windows endpoint** — build the VM, install Sysmon, enrol the Wazuh agent.
4. **Linux endpoint** — build the VM, configure auditd, enrol the Wazuh agent.
5. **Attack simulations** — generate security events and capture alerts.
6. **Incident reporting** — triage alerts and write up findings.
