import subprocess
import sys

def install_with_pip(package):
    """Install a package using pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"Successfully installed {package}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install {package}: {e}")

def install_spacy_model(model):
    """Download a SpaCy language model."""
    try:
        subprocess.check_call([sys.executable, "-m", "spacy", "download", model])
        print(f"Successfully downloaded SpaCy model: {model}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to download SpaCy model {model}: {e}")

def install_npm_package(package):
    """Install a package using npm."""
    try:
        subprocess.check_call(["npm", "install", package])
        print(f"Successfully installed npm package: {package}")
    except FileNotFoundError:
        print("npm is not installed. Please install Node.js and npm to proceed.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install npm package {package}: {e}")

def main():
    # List of Python packages with specific versions
    python_packages = [
        "openai==1.55.0",
        "numpy==1.26.4",
        "pandas==2.2.2",
        "deepeval==1.4.5",
        "PyMuPDF==1.24.14",
        "PyPDF2==2.10.5",
        "spacy==3.7.6",
        "pymongo==4.10.1"
    ]

    # Install Python packages
    for package in python_packages:
        install_with_pip(package)

    # Install SpaCy language model
    install_spacy_model("en_core_web_sm")

    # Install npm package
    install_npm_package("cytoscape")

if __name__ == "__main__":
    main()
  
