# 02 — Wazuh Server Deployment

This document records the deployment of the Wazuh SIEM server from the official virtual appliance (OVA).

---

## Why the OVA?

Wazuh can be installed from scratch on a Linux host, but this requires installing and configuring three separate components — the Wazuh manager, the indexer, and the dashboard. The official **OVA appliance** ships these pre-installed and pre-configured. Using it removes setup friction and lets the project focus on the SOC work itself: monitoring, detection, and triage.

| Property | Value |
|----------|-------|
| Appliance | wazuh-4.14.5.ova |
| Wazuh version | 4.14.5 |
| Components | Manager + Indexer + Dashboard (all-in-one) |

---

## Import Settings

The OVA was imported into VirtualBox via **File → Import Appliance** with the following settings adjusted for the 16 GB host:

| Setting | Value | Reason |
|---------|-------|--------|
| Base Memory | 6144 MB | Comfortable for the Java-based indexer without starving the host |
| CPU | 2 vCPUs | Sufficient for a small lab; leaves cores for endpoints |
| Name | Wazuh-Server | Clarity |

---

## Network Configuration

After import, the VM's network adapter was attached to the lab network:

- **Adapter 1** → Attached to **NAT Network** → Name **SOC-Lab**

On first boot the server received the address **10.0.10.3** via DHCP. This address is recorded because every Wazuh agent installed later must be pointed at it.

### Dashboard Access

The Wazuh dashboard runs on HTTPS port 443 inside the isolated network. To reach it from the host browser, a port-forwarding rule was added to the `SOC-Lab` NAT Network:

```
VBoxManage natnetwork modify --netname "SOC-Lab" \
  --port-forward-4 "wazuh-dashboard:tcp:[]:8443:[10.0.10.3]:443"
```

| Rule | Host | Guest |
|------|------|-------|
| wazuh-dashboard | localhost:8443 | 10.0.10.3:443 |

The dashboard is then reached at **https://localhost:8443**.

---

## Credentials

| Access point | Username | Password |
|--------------|----------|----------|
| VM console / SSH | wazuh-user | wazuh |
| Wazuh dashboard | admin | admin |

> **Security note:** These are default credentials shipped with the appliance. In any real deployment they must be changed immediately. They are retained here only because the lab is fully isolated and non-production.

---

## Verification

- Wazuh server boots and reaches the login console. ✓
- Server obtains a lab IP address (10.0.10.3). ✓
- Wazuh dashboard loads at `https://localhost:8443` and accepts login. ✓

Milestone **M2 (Wazuh server deployed, dashboard accessible)** is complete.
