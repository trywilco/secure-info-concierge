from transformers import AutoTokenizer
import os
import sys
import gc
import subprocess
import time
import platform

# Avoid importing torch and model libraries at the top level to save memory

def get_transformers_version():
    """Get the installed transformers version"""
    try:
        cmd = [
            sys.executable,
            "-c",
            "import transformers; print(transformers.__version__)"
        ]
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        version = result.stdout.strip()
        print(f"Detected transformers version: {version}")
        return version
    except Exception as e:
        print(f"Error detecting transformers version: {str(e)}")
        return "0.0.0"

def download_opt_model():
    """Download OPT-1.3B tokenizer and model files using a separate process"""
    # Check if transformers version supports OPT
    version = get_transformers_version()
    from packaging import version as pkg_version
    if pkg_version.parse(version) < pkg_version.parse("4.18.0"):
        print(f"Transformers version {version} does not support OPT (requires >= 4.18.0)")
        print("Please upgrade transformers to use OPT model")
        return False
        
    model_id = "facebook/opt-1.3b"
    print(f"Downloading {model_id} tokenizer...")
    tokenizer_success = False
    model_success = False
    
    try:
        # Download tokenizer only first
        cmd = [
            sys.executable, 
            "-c", 
            "from transformers import AutoTokenizer; "
            f"tokenizer = AutoTokenizer.from_pretrained('{model_id}')"
        ]
        subprocess.run(cmd, check=True)
        print(f"✓ {model_id} tokenizer downloaded")
        tokenizer_success = True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading {model_id} tokenizer: {str(e)}")
    
    # Only try to download model if tokenizer was successful
    if tokenizer_success:
        try:
            # Then download model in a separate process - try with reduced precision
            print(f"Downloading {model_id} model...")
            cmd = [
                sys.executable, 
                "-c", 
                "from transformers import AutoModelForCausalLM; "
                "import torch; import gc; "
                f"model = AutoModelForCausalLM.from_pretrained('{model_id}', torch_dtype=torch.float16); "
                "del model; gc.collect()"
            ]
            subprocess.run(cmd, check=True)
            print(f"✓ {model_id} model downloaded")
            model_success = True
        except subprocess.CalledProcessError as e:
            print(f"Error downloading {model_id} model with float16: {str(e)}")
            
            # Try again without specifying dtype
            try:
                print(f"Attempting to download {model_id} model without specifying dtype...")
                cmd = [
                    sys.executable, 
                    "-c", 
                    "from transformers import AutoModelForCausalLM; "
                    "import gc; "
                    f"model = AutoModelForCausalLM.from_pretrained('{model_id}'); "
                    "del model; gc.collect()"
                ]
                subprocess.run(cmd, check=True)
                print(f"✓ {model_id} model downloaded without dtype specification")
                model_success = True
            except subprocess.CalledProcessError as e:
                print(f"Error downloading {model_id} model without dtype: {str(e)}")
    
    return tokenizer_success and model_success

def download_sentence_transformer():
    """Download sentence transformer model using a separate process"""
    print("Downloading sentence transformer...")
    try:
        cmd = [
            sys.executable, 
            "-c", 
            "from sentence_transformers import SentenceTransformer; "
            "import gc; "
            "model = SentenceTransformer('paraphrase-MiniLM-L6-v2'); "
            "del model; gc.collect()"
        ]
        subprocess.run(cmd, check=True)
        print("✓ Sentence transformer downloaded")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading sentence transformer: {str(e)}")
        return False

def download_distilroberta_classifier():
    """Download smaller zero-shot classification model using a separate process"""
    print("Downloading zero-shot classification model...")
    try:
        # Download tokenizer first
        cmd = [
            sys.executable, 
            "-c", 
            "from transformers import AutoTokenizer; "
            "tokenizer = AutoTokenizer.from_pretrained('cross-encoder/nli-distilroberta-base')"
        ]
        subprocess.run(cmd, check=True)
        print("✓ Zero-shot tokenizer downloaded")
        
        # Then download model files
        print("Downloading zero-shot model...")
        cmd = [
            sys.executable, 
            "-c", 
            "from transformers import AutoModelForSequenceClassification; "
            "import gc; "
            "model = AutoModelForSequenceClassification.from_pretrained('cross-encoder/nli-distilroberta-base'); "
            "del model; gc.collect()"
        ]
        subprocess.run(cmd, check=True)
        print("✓ Zero-shot model downloaded")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error downloading zero-shot model: {str(e)}")
        return False

def download_models():
    """Download Gemma model and other required models using separate processes to manage memory"""
    print("\n===== Starting model downloads =====\n")
    start_time = time.time()
    
    # Create the cache directory if it doesn't exist
    cache_dir = os.path.expanduser("~/.cache/huggingface")
    os.makedirs(cache_dir, exist_ok=True)
    
    # Print system information
    print(f"Python version: {sys.version}")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.machine()}")
    
    # Download models one by one with explicit garbage collection between each
    success = True
    
    # Download OPT-1.3B model
    if not download_opt_model():
        success = False
    gc.collect()
    
    if not download_sentence_transformer():
        success = False
    gc.collect()
    
    # Finally the smaller zero-shot model
    if not download_distilroberta_classifier():
        success = False
    gc.collect()
    
    elapsed_time = time.time() - start_time
    print(f"\n===== Model download completed in {elapsed_time:.1f} seconds =====\n")
    print(f"Models cached at: {cache_dir}")
    
    return success

if __name__ == "__main__":
    print("Starting memory-efficient model downloader")
    success = download_models()
    
    if not success:
        print("⚠️ Some models failed to download. They will be downloaded at runtime.")
        # Don't exit with error code, let the app try to start anyway
        sys.exit(0)
    else:
        print("✅ All models successfully downloaded and cached!")
        sys.exit(0)
