import os

os.makedirs("data/public", exist_ok=True)
os.makedirs("data/confidential", exist_ok=True)

docs = {
    "data/public/password_reset.txt": """IT Helpdesk Guide: Password Reset
Employees can reset their password at the self-service portal.
Step 1: Open the portal and click 'Forgot Password'.
Step 2: Enter your employee ID and company email.
Step 3: Click the link sent to your email and set a new password.
Passwords must be at least 12 characters long.
If the portal does not work, contact the IT Helpdesk.""",

    "data/public/vpn_setup.txt": """IT Helpdesk Guide: VPN Setup
The company VPN lets employees work securely from home.
Step 1: Download the VPN client from the software portal.
Step 2: Sign in with your company email and password.
Step 3: Approve the login request on your phone (multi-factor authentication).
If the VPN disconnects often, restart the client and check your internet.""",

    "data/public/it_policy.txt": """Company IT Security Policy
Employees must lock their computer when away from their desk.
Never share your password with anyone, including IT staff.
Report suspicious emails to the security team.
Only install software approved by the IT department.""",

    "data/confidential/admin_notes.txt": """CONFIDENTIAL: IT Admin Only
Server admin account: admin_root
Server admin password: FakePass@2026!
Database backup server: 10.0.0.25
Emergency API key: sk-FAKE-1234567890
Do not share these details with regular employees.""",
}

for path, text in docs.items():
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Created:", path)