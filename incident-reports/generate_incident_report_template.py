from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

doc = Document()

for section in doc.sections:
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.2)
    section.right_margin = Cm(2.2)

style = doc.styles['Normal']
style.font.name = 'Calibri'
style.font.size = Pt(11)

NAVY = (0x2E, 0x40, 0x57)
GREY = (110, 110, 110)


def set_font(run, bold=False, size=11, color=None, italic=False):
    run.font.name = 'Calibri'
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    if color:
        run.font.color.rgb = RGBColor(*color)


def hr(doc):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), '6')
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), '2E4057')
    pBdr.append(bottom)
    pPr.append(pBdr)


def h1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    set_font(p.add_run(text.upper()), bold=True, size=13, color=NAVY)
    hr(doc)


def h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    set_font(p.add_run(text), bold=True, size=12, color=NAVY)


def body(doc, text, italic=False, color=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    set_font(p.add_run(text), size=11, italic=italic, color=color)


def note(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    set_font(p.add_run('NOTE: '), bold=True, italic=True, size=10, color=GREY)
    set_font(p.add_run(text), italic=True, size=10, color=GREY)


def bullet(doc, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    set_font(p.add_run(text), size=11)


def kv_table(doc, rows):
    table = doc.add_table(rows=len(rows), cols=2)
    table.style = 'Light Shading Accent 1'
    for i, (k, v) in enumerate(rows):
        table.rows[i].cells[0].text = k
        table.rows[i].cells[1].text = v
        for cell in table.rows[i].cells:
            for para in cell.paragraphs:
                for run in para.runs:
                    run.font.name = 'Calibri'
                    run.font.size = Pt(10.5)


def timeline_table(doc, rows):
    table = doc.add_table(rows=1, cols=3)
    table.style = 'Medium Shading 1 Accent 1'
    hdr = table.rows[0].cells
    hdr[0].text = 'Timestamp'
    hdr[1].text = 'Event'
    hdr[2].text = 'Source'
    for k in hdr:
        for p in k.paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(10)
    for ts, ev, src in rows:
        row = table.add_row().cells
        row[0].text = ts
        row[1].text = ev
        row[2].text = src
        for cell in row:
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(10)


def alert_table(doc, rows):
    table = doc.add_table(rows=1, cols=4)
    table.style = 'Medium Shading 1 Accent 1'
    hdr = table.rows[0].cells
    for i, h in enumerate(['Rule ID', 'Rule Description', 'Level', 'Timestamp']):
        hdr[i].text = h
        for p in hdr[i].paragraphs:
            for r in p.runs:
                r.font.bold = True
                r.font.size = Pt(10)
    for rid, desc, lvl, ts in rows:
        row = table.add_row().cells
        row[0].text = rid
        row[1].text = desc
        row[2].text = lvl
        row[3].text = ts
        for cell in row:
            for p in cell.paragraphs:
                for r in p.runs:
                    r.font.size = Pt(10)


# ---------- TITLE ----------
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_font(p.add_run('SECURITY INCIDENT REPORT'), bold=True, size=20, color=NAVY)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_font(p.add_run('SOC Home Lab, Wazuh SIEM'), size=11, italic=True, color=GREY)

doc.add_paragraph()

# ---------- REPORT METADATA ----------
kv_table(doc, [
    ('Report Reference', 'INC-2026-001'),
    ('Date Compiled', '[DD Month YYYY]'),
    ('Analyst', 'Muhammad Ahmed Khalid'),
    ('System of Record', 'Wazuh SIEM (SOC Home Lab, 10.0.10.3)'),
    ('Classification', 'Internal, Training Exercise'),
    ('Status', 'Closed, post-incident review'),
    ('Overall Severity', 'Medium (highest Wazuh rule level observed: 12+)'),
])

# ---------- 1. EXECUTIVE SUMMARY ----------
h1(doc, '1. Executive Summary')
note(doc, 'Two to three sentences in plain language. What happened, on which system, current status. Non-technical audience should be able to follow this section alone.')
body(doc,
     'On [DATE] at [TIME], the Wazuh SIEM detected a suspicious sequence of Windows account management actions on the Windows-Endpoint host (10.0.10.4). A previously unknown local user account, "testuser", was created and then immediately elevated to the local Administrators group. This activity is consistent with post-compromise persistence and privilege escalation techniques (MITRE ATT&CK T1136.001 and T1078.003), and in a live environment would require immediate investigation of the originating session, credentials, and any lateral movement. This report was generated as part of a controlled training simulation to validate detection coverage and analyst workflow.'
)

# ---------- 2. INCIDENT DETAILS ----------
h1(doc, '2. Incident Details')
kv_table(doc, [
    ('Affected System', 'Windows-Endpoint, hostname WINDEV2407EVAL, IP 10.0.10.4'),
    ('Affected Account', 'testuser (newly created local account)'),
    ('Time of Activity', '[DD Month YYYY, HH:MM UTC]'),
    ('Time of Detection', '[DD Month YYYY, HH:MM UTC], within 60 seconds'),
    ('Detection Method', 'Wazuh SIEM correlation of Windows Security Event Log + Sysmon telemetry'),
    ('Attack Technique', 'Local account creation and administrative privilege escalation'),
    ('MITRE ATT&CK', 'T1136.001 (Local Account), T1078.003 (Valid Accounts: Local Accounts)'),
])

# ---------- 3. TIMELINE ----------
h1(doc, '3. Timeline of Events')
note(doc, 'Chronological ordering. Fill in real timestamps from your Wazuh alerts. Timestamp format: HH:MM:SS UTC.')
timeline_table(doc, [
    ('[HH:MM:SS]', 'Attacker session began on Windows-Endpoint (elevated PowerShell)', 'Sysmon (Event ID 1, Process Create)'),
    ('[HH:MM:SS]', 'Command executed: net user testuser P@ssw0rd123! /add', 'Sysmon + Windows Security Log (Event ID 4720)'),
    ('[HH:MM:SS]', 'Wazuh alert fired: "Users Group Changed" (rule level 8)', 'Wazuh SIEM'),
    ('[HH:MM:SS]', 'Command executed: net localgroup administrators testuser /add', 'Sysmon + Windows Security Log (Event ID 4732)'),
    ('[HH:MM:SS]', 'Wazuh alert fired: "Administrative Privilege Assigned" (rule level 12+)', 'Wazuh SIEM'),
    ('[HH:MM:SS]', 'Analyst identified alerts during Threat Hunting review', 'Wazuh dashboard'),
    ('[HH:MM:SS]', 'Simulated containment step: account disabled', 'Analyst action'),
])

# ---------- 4. DETECTION & ALERTING ----------
h1(doc, '4. Detection and Alerting')
body(doc,
     'The following Wazuh alerts fired in response to the simulated activity. Screenshots are included in Appendix A.'
)
alert_table(doc, [
    ('[####]', 'Users Group Changed', '8', '[HH:MM:SS]'),
    ('[####]', 'Administrative Privilege Assigned', '12+', '[HH:MM:SS]'),
    ('[####]', 'Domain Users Group Changed', '[X]', '[HH:MM:SS]'),
    ('[####]', 'A "net user" account discovery command was executed', '[X]', '[HH:MM:SS]'),
    ('[####]', 'Discovery activity spawned by PowerShell execution', '[X]', '[HH:MM:SS]'),
    ('[####]', 'Executable dropped in Windows directory', '[X]', '[HH:MM:SS]'),
])
note(doc, 'Fill in the exact rule IDs and timestamps from your Wazuh dashboard. Levels 12 and above would page an on-call analyst in a live SOC.')

# ---------- 5. TECHNICAL ANALYSIS ----------
h1(doc, '5. Technical Analysis')
body(doc,
     'Two commands were executed on the Windows-Endpoint host from an elevated PowerShell session:'
)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(2)
set_font(p.add_run('  net user testuser P@ssw0rd123! /add'), size=10)
p = doc.add_paragraph()
p.paragraph_format.space_after = Pt(8)
set_font(p.add_run('  net localgroup administrators testuser /add'), size=10)

body(doc,
     'These commands together create a new local user account and grant it full administrative privileges on the host. Individually, each is a routine Windows administrator action. Together, in rapid succession, they represent a well documented attacker post-compromise pattern:'
)
bullet(doc, 'T1136.001 Local Account, an attacker creates a local account for persistence, so they retain access even if the initial exploitation route is closed')
bullet(doc, 'T1078.003 Valid Accounts: Local Accounts, the attacker then uses the created account as if it were a legitimate user, evading behavioural detections that would flag anonymous activity')
body(doc,
     'Wazuh correlated the Sysmon process-creation events (net.exe spawned by powershell.exe) with the Windows Security Event Log events (4720 Account Created, 4732 Account Added to Privileged Local Group), and raised the corresponding alerts within seconds of the activity.'
)

# ---------- 6. IMPACT ASSESSMENT ----------
h1(doc, '6. Impact Assessment')
kv_table(doc, [
    ('Confidentiality', 'Direct: none, as no data was accessed. Potential (if unmitigated): full local access to any data readable by Administrators group on the host.'),
    ('Integrity', 'Direct: unauthorised local account created and elevated. Potential: complete host reconfiguration, log tampering, and installation of persistent malware.'),
    ('Availability', 'Direct: none. Potential: full host takeover including denial of service to legitimate users.'),
    ('Blast Radius', 'Currently limited to single host (Windows-Endpoint). Lateral movement paths from this host would need to be assessed in a live environment.'),
    ('Business Impact (simulated)', 'Low (training environment). In a production equivalent, likely Medium to High depending on host role.'),
])

# ---------- 7. RESPONSE ACTIONS ----------
h1(doc, '7. Response Actions')
h2(doc, 'Immediate (within first 5 minutes)')
bullet(doc, 'Disable the newly created account: net user testuser /active:no')
bullet(doc, 'Force logout of any sessions belonging to testuser: quser then logoff [ID]')
bullet(doc, 'Isolate the host from the network (in a production SOC, via EDR isolation or firewall block)')
h2(doc, 'Short-term (within first hour)')
bullet(doc, 'Identify the process and parent session that executed the "net user" commands using Sysmon Event ID 1 details (process, command line, parent, user)')
bullet(doc, 'Search for any additional accounts created within the same session window')
bullet(doc, 'Search for lateral movement indicators from this host (network connections, remote logins to other hosts)')
h2(doc, 'Follow-up')
bullet(doc, 'Full removal of testuser account after evidence preservation: net user testuser /delete')
bullet(doc, 'Password reset for any accounts that were logged into the host during the incident window')
bullet(doc, 'Update endpoint hardening baseline if the initial access vector is identified')

# ---------- 8. ROOT CAUSE ----------
h1(doc, '8. Root Cause and Findings')
body(doc,
     'This simulation was executed by the analyst intentionally, so root cause in the technical sense is not applicable. However, the exercise validated the following findings about the SOC lab detection posture:'
)
bullet(doc, 'Windows Security Event Log ingestion via Wazuh is working correctly, with expected alerts for account creation and privileged group changes')
bullet(doc, 'Sysmon telemetry with the SwiftOnSecurity baseline correctly identified the net.exe process spawn from powershell.exe as suspicious')
bullet(doc, 'Correlation between the Sysmon process events and the Windows Security events happened within the same alert window, indicating Wazuh rulesets are matching effectively')
bullet(doc, 'Alert triage from action to visible alert was under 60 seconds, which meets Tier 1 SOC time-to-detect expectations for this class of activity')

# ---------- 9. RECOMMENDATIONS ----------
h1(doc, '9. Recommendations')
h2(doc, 'Detection Improvements')
bullet(doc, 'Enable real-time File Integrity Monitoring (FIM) on high-value paths (see finding from FIM simulation, where a hosts file modification did not trigger a real-time alert)')
bullet(doc, 'Add a custom correlation rule to fire a single high-severity alert when a new local account is added to Administrators within the same session, rather than relying on operators to correlate multiple lower-severity alerts')
h2(doc, 'Process Improvements')
bullet(doc, 'Document standard analyst response steps as a runbook for the "unauthorised account creation" alert class')
bullet(doc, 'Baseline expected administrator activity on each host so anomalous privilege changes stand out more clearly')
h2(doc, 'Hardening Recommendations')
bullet(doc, 'Restrict local Administrator group membership to a documented list, with quarterly review')
bullet(doc, 'Enforce Just-In-Time privilege elevation for administrative tasks where practical')

# ---------- 10. LESSONS LEARNED ----------
h1(doc, '10. Lessons Learned')
bullet(doc, 'Multiple lower-severity alerts often tell a stronger story together than any single alert on its own; analyst intuition matters as much as tooling')
bullet(doc, 'Some Wazuh capabilities (like FIM) are not enabled in real-time by default and require deliberate configuration for critical paths')
bullet(doc, 'The 60-second detection window achieved in this simulation only holds because both endpoints are enrolled and telemetry is flowing; an unmanaged host would be blind')

# ---------- APPENDIX ----------
h1(doc, 'Appendix A, Evidence')
body(doc,
     'The following screenshots are provided as evidence, saved in the project screenshots folder:'
)
bullet(doc, 'M5-sim1-user-created and user-added-to-admins.png, Wazuh alert view for Windows-Endpoint immediately after the simulation')
bullet(doc, 'Additional related screenshots as needed for full evidence trail')

h1(doc, 'Appendix B, References')
bullet(doc, 'MITRE ATT&CK T1136.001, Create Account: Local Account, https://attack.mitre.org/techniques/T1136/001/')
bullet(doc, 'MITRE ATT&CK T1078.003, Valid Accounts: Local Accounts, https://attack.mitre.org/techniques/T1078/003/')
bullet(doc, 'Microsoft Windows Security Event 4720, A user account was created')
bullet(doc, 'Microsoft Windows Security Event 4732, A member was added to a security-enabled local group')
bullet(doc, 'Wazuh Documentation, https://documentation.wazuh.com')

# --------- FOOTER ---------
p = doc.add_paragraph()
p.paragraph_format.space_before = Pt(20)
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
set_font(p.add_run('End of Report'), size=9, italic=True, color=GREY)

out = r'C:\Users\ahmed\0.CLAUDE\Job\Projects\Project 1 - SOC Home Lab with SIEM\incident-reports\Incident_Report_Template.docx'
doc.save(out)
print(f'Saved: {out}')
