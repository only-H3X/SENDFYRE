import importlib.util
import subprocess
import sys
import os

def install_package(package_name):
    """
    Installs the package using pip.
    """
    try:
        print(f"Installing {package_name} ...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while installing {package_name}: {e}")
        sys.exit(1)

def ensure_dependency(package_name, import_name=None):
    """
    Checks if a package is installed (using its import name).
    If not, installs it using pip.
    If import_name is not provided, it defaults to package_name.
    """
    if import_name is None:
        import_name = package_name

    spec = importlib.util.find_spec(import_name)
    if spec is None:
        install_package(package_name)
        # After installing, try again
        spec = importlib.util.find_spec(import_name)
        if spec is None:
            print(f"Failed to import {import_name} even after installation.")
            sys.exit(1)
    # Optionally, add the module's path to sys.path if needed.
    module = importlib.import_module(import_name)
    module_path = os.path.dirname(module.__file__)
    if module_path not in sys.path:
        sys.path.append(module_path)
    print(f"{import_name} is installed and available.")
    return module

def check_install_dependencies():
    """
    List all required packages and their corresponding import names.
    This list can be modified as needed.
    """
    dependencies = {
        "dnspython": "dns",                 # pip package: dnspython, import: dns
        "requests": "requests",             # pip package: requests
        "aiosmtplib": "aiosmtplib",         # pip package: aiosmtplib
        "PySocks": "socks",                 # pip package: PySocks, import: socks
        "validate_email_address": "validate_email_address",  # pip package: validate_email_address
        "python-docx": "docx",              # pip package: python-docx, import: docx
        "PyPDF2": "PyPDF2",                 # pip package: PyPDF2
        "fpdf": "fpdf",                     # pip package: fpdf
        "qrcode": "qrcode",                 # pip package: qrcode
        "Pillow": "PIL",                    # pip package: Pillow, import: PIL
        # xhtml2pdf is optional; if not installed, the script will warn.
        "xhtml2pdf": "xhtml2pdf"
    }
    for pkg, imp in dependencies.items():
        # Try to import the module; if not found, install it.
        try:
            ensure_dependency(pkg, imp)
        except Exception as e:
            print(f"An error occurred while ensuring dependency {pkg}: {e}")
            sys.exit(1)

if __name__ == "__main__":
    check_install_dependencies()
