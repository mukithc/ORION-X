"""
ORION-X - Download all practical open-source models for Ollama
Only models that fit on 8-24GB VRAM. Skips 100B+ (need enterprise hardware).
"""

import subprocess
import sys

# Ollama native - all open source (Apache/MIT)
OLLAMA = [
    "llama3.2:3b", "llama3.2:1b", "mistral:7b", "phi3:mini",
    "qwen2.5:7b", "gemma2:2b", "deepseek-r1:1.5b", "codellama:7b",
    "qwen2.5-coder:7b", "nomic-embed-text", "llama3.1:8b",
]

# Hugging Face - GGUF format for Ollama, open source
# Enable at: https://huggingface.co/settings/local-apps
HF_MODELS = [
    ("Edge-Quant/Nanbeige4.1-3B-Q4_K_M-GGUF", 4),
    ("Nanbeige/Nanbeige4.1-3B", 4),
    ("lm-provers/QED-Nano", 4),
    ("openbmb/MiniCPM-SALA", 9),
    ("openbmb/MiniCPM-o-4_5-gguf", 8),
    ("mmnga-o/NVIDIA-Nemotron-Nano-9B-v2-Japanese-gguf", 9),
    ("unsloth/gpt-oss-20b-GGUF", 21),
    ("unsloth/GLM-4.7-Flash-REAP-23B-A3B-GGUF", 23),
    ("unsloth/GLM-4.7-Flash-GGUF", 30),
    ("unsloth/Qwen3-Coder-30B-A3B-Instruct-GGUF", 31),
]


def pull_ollama(model: str) -> bool:
    try:
        subprocess.run(["ollama", "pull", model], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def pull_hf(model: str) -> bool:
    try:
        subprocess.run(["ollama", "run", f"hf.co/{model}", "hi"], check=True, timeout=300)
        return True
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False


def main():
    print("ORION-X - Download Open Source Models")
    print("=" * 50)
    print("1. Ollama native only (fastest)")
    print("2. Ollama + Hugging Face (enable HF Ollama first)")
    print("3. Hugging Face only")
    choice = input("\nChoice [1]: ").strip() or "1"

    if choice in ("1", "2"):
        print("\n--- Ollama Native ---")
        for m in OLLAMA:
            print(f"\n>>> {m}")
            pull_ollama(m)

    if choice in ("2", "3"):
        print("\n--- Hugging Face GGUF ---")
        print("Enable at: https://huggingface.co/settings/local-apps\n")
        for model, size in HF_MODELS:
            print(f">>> {model} ({size}B)")
            pull_hf(model)

    print("\n" + "=" * 50)
    print("Done! ollama list")


if __name__ == "__main__":
    main()
