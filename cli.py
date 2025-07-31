import typer
from agents.recon_agent import run_recon
from agents.crypto_agent import run_crypto
from agents.script_analyzer import run_script_analysis
from agents.payload_helper import run_payload_helper

app = typer.Typer()

@app.command()
def recon(target: str):
  "Run initial recon with automated scanning and AI suggestions"
  run_recon(target)
  
@app.command()
def crypto(ciphertext: str):
  "Analyze and assist cracking a ciphertext"
  run_crypto(ciphertext)

@app.command()
def analyze_script(path: str):
  "Analyze script file for patterns or obfuscation"
  run_script_analysis(path)

@app.command()
def payload(technique: str):
  "Suggest or generate payload for a technique"
  run_payload_helper(technique)

if __name__== "__main__":
  app()

