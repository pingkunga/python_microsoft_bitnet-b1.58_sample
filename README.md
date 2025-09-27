# BitNet API - Local LLM Inference

This project provides a FastAPI-based OpenAI-compatible API for running BitNet LLM models locally on Windows or Linux.

## Project Structure & Usage Notes

- **LLM.py**: Example script for running a single prompt/response with the BitNet model directly from the command line. Useful for quick local testing.
- **LLM_Terminal.py**: Interactive terminal chat script for BitNet. Allows you to chat with the model in a loop from your terminal.
- **bitnet-api/**: Contains the FastAPI server code that exposes an OpenAI-compatible API for use with Open WebUI or other clients. Use this if you want to connect Open WebUI or similar tools to your local BitNet model.

See comments in each file for more details and usage examples.

## Requirements
- Python 3.12 or newer
- `python3-venv` (for Linux)
- Visual Studio Build Tools (Windows, for PyTorch):
  - Install from https://visualstudio.microsoft.com/visual-cpp-build-tools/
  - Select "Desktop development with C++"
  - Ensure `cl.exe` is in your PATH (use Developer Command Prompt or add manually)

## Setup

### 1. Clone the repository
```
git clone <your-repo-url>
cd 2025Bitnet
```

### 2. Create and activate a virtual environment
#### Windows
```
python -m venv bitnet-env
bitnet-env\Scripts\Activate.ps1
# or
bitnet-env\Scripts\activate.bat
```
#### Linux
```
python3 -m venv bitnet-env
source bitnet-env/bin/activate
```

### 3. Install dependencies
```
pip install --upgrade pip
pip install torch==2.7.0 transformers==4.52.4 numpy==1.26.4 accelerate
pip install git+https://github.com/huggingface/transformers.git@096f25ae1f501a084d8ff2dcaf25fbc2bd60eba4
```

### 4. (Windows only) Set up Visual Studio environment
```
"C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvarsall.bat" x64
```
Or use the Developer Command Prompt for VS.

## Running the API

### 1. Start the FastAPI server
```
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 2. Access the API
- OpenAPI docs: http://localhost:8000/docs
- Health check: http://localhost:8000/health
- Chat completions: POST to http://localhost:8000/v1/chat/completions

## Docker
Build and run with Docker:
```
docker build -t bitnet-api .
docker run --restart unless-stopped -p 8000:8000 bitnet-api
```

## Troubleshooting
- If you see `RuntimeError: Compiler: cl is not found.`, ensure Visual Studio Build Tools are installed and `cl.exe` is in your PATH.
- For PyTorch C++ errors, see:
  - https://github.com/pytorch/pytorch/issues/154127
  - https://learn.microsoft.com/en-us/windows/ai/windows-ml/tutorials/pytorch-installation

## References
- [BitNet Model](https://onedollarvps.com/blogs/how-to-run-bitnet-b1-58-locally.html#general-installation-steps)
- [HuggingFace Transformers](https://github.com/huggingface/transformers)
- [PyTorch](https://pytorch.org/)

---

For more details, see the included `readme.txt`.

## Further Reading
- [Blog: Create a REST API for the Microsoft BitNet B1.58 Model and Integrate it with an Open WebUI (English)](https://naiwaen.debuggingsoft.com/2025/07/create-a-rest-api-for-the-microsoft-bitnet-b1-58-model-and-integrate-it-with-an-open-webui-english/)
