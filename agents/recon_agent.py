import subprocess
import os
import re
from transformers import pipeline

def run_recon(target):
    print(f"[+] Starting automated recon on: {target}\n")
    print("[*] This may take a while...\n")
    print("[*] Running nmap scan...")
    nmap_cmd = ["nmap", "-sC", "-sV", "-T4", "-oN", "recon_nmap.txt", target]
    subprocess.run(nmap_cmd)

    # TODO: Add some more options like rustscan etc.

    print("[*] Running httpx scan (if applicable)...")
    httpx_cmd = f"echo {target} | httpx -title -tech-detect -status -o recon_httpx.txt"
    os.system(httpx_cmd)

    print("[*] Running whatweb (if HTTP service exists)...")
    whatweb_cmd = f"whatweb {target} > recon_whatweb.txt"
    os.system(whatweb_cmd)

    print("[*] Parsing results...\n")
    parse_nmap_output("recon_nmap.txt")
    print("\n[*] You can now check: recon_httpx.txt and recon_whatweb.txt for more info.")


def parse_nmap_output(path):
    if not os.path.exists(path):
        print("[!] Nmap output not found.")
        return

    with open(path) as f:
        content = f.read()

    ports = re.findall(r"(\d{1,5})/tcp\s+open", content)
    if ports:
        print("[+] Open TCP Ports Found:", ", ".join(ports))
        suggest_from_ports(ports)
        ai_suggest_next_steps()
    else:
        print("[!] No open TCP ports found.")

def suggest_from_ports(ports):
    suggestions = {
        "21": "[*] FTP detected. Try anonymous login or brute-force with hydra.",
        "22": "[*] SSH detected. Try user enumeration or weak credentials.",
        "80": "[*] HTTP detected. Consider gobuster, nikto, or wfuzz.",
        "443": "[*] HTTPS detected. Test with sslscan, dirb, etc.",
        "139": "[*] SMB port detected. Enum4linux, smbclient, etc.",
        "445": "[*] SMB port detected. Search for EternalBlue, enum4linux-ng.",
        "3306": "[*] MySQL open. Try mysql -u root -p or sqlmap.",
        "8080": "[*] Alternate HTTP. Look for web services, admin panels.",
    }
    for port in ports:
        if port in suggestions:
            print(suggestions[port])
        else:
            print(f"[*] Port {port} open - check manually for associated service.")

def ai_suggest_next_steps(open_ports, banners=None):
    print("\n[+] AI Suggestions based on recon results:")
    prompt = f"Given the open ports {', '.join(open_ports)}"
    if banners:
        prompt += f" and the following service info: {banners}"
    prompt += ". Suggest next penetration testing steps."

    try:
        generator = pipeline("text-generation", model="gpt2")
        ai_response = generator(prompt, max_length=150, num_return_sequences=1)[0]['generated_text']
        print("[AI]:", ai_response.strip())
    except Exception as e:
        print("[!] AI suggestion failed:", e)