"""
ORION-X Model Downloader
Downloads free models for Ollama.
"""

import subprocess
import sys

# Practical models that fit on 8-16GB VRAM
OLLAMA_MODELS = [
    "llama3.2:3b",
    "llama3.2:1b",
    "mistral:7b",
    "phi3:mini",
    "qwen2.5:7b",
    "gemma2:2b",
    "deepseek-r1:1.5b",
    "codellama:7b",
    "nomic-embed-text",
]

# Hugging Face - enable at https://huggingface.co/settings/local-apps
# Run: ollama run hf.co/Nanbeige/Nanbeige4.1-3B
# (Downloads on first use)
HF_SMALL = [
    "hf.co/Nanbeige/Nanbeige4.1-3B",
    "hf.co/openbmb/MiniCPM-SALA",
    "hf.co/lm-provers/QED-Nano",
]

# TOO LARGE for consumer PCs (need 100GB+ VRAM):
# MiniMax-M2.5 (229B), Qwen3.5-397B (403B), GLM-5 (754B), Ring-2.5 (1T)
# Kimi-K2.5 (171B) - would need ~80GB+


def main():
    print("ORION-X Model Downloader\n")
    print("1. Ollama native (recommended)")
    print("2. Ollama + Hugging Face small models")
    choice = input("Choice (1 or 2) [1]: ").strip() or "1"

    for m in OLLAMA_MODELS:
        print(f"\n>>> Pulling {m}...")
        subprocess.run(["ollama", "pull", m], check=False)

    if choice == "2":
        print("\n--- Hugging Face (enable Ollama in HF settings first) ---")
        for m in HF_SMALL:
            print(f"\n>>> {m} (run to download)")
            subprocess.run(["ollama", "run", m, "hi"], check=False)

    print("\nDone! ollama list")


if __name__ == "__main__":
    main()
