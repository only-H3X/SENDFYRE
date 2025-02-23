# Email Sender

**Email Sender** is an asynchronous Python tool for sending customizable email campaigns. It includes advanced features such as multi-node SMTP support, proxy usage, file conversion and encoding, inline QR code generation, custom header/priority settings, enhanced email validation, custom sender configuration, and send rate control.

## Table of Contents

- [Features](#features)
- [Directory Structure](#directory-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Dependency Management](#dependency-management)
- [Configuration Validation](#configuration-validation)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Features

- **Asynchronous Email Sending:** Uses `asyncio` and `aiosmtplib` to send emails concurrently.
- **SMTP Multi-Node Support:** Randomly select or choose specific SMTP nodes.
- **Proxy & Open-Relay Support:** Optionally use a proxy; supports open-relay configuration (skip authentication, disable TLS).
- **File Conversion & Encoding:** Converts TXT, DOCX, and image files to PDF and can Base64-encode attachments.
- **QR Code Generation:** Generates inline QR codes from a list of URLs; if an attachment is specified as a URL, a QR code image is generated.
- **Custom Headers & Priority:** Set custom headers (e.g., "X-Custom-Header"), email priority (using "X-Priority" and "Priority" headers), and enable header encoding (RFC 2047).
- **Custom Sender Information:** Override SMTP node sender details with custom values.
- **Enhanced Email Validation:** Checks email format with a regex, filters disposable domains, and verifies MX records.
- **Send Rate Control:** Limit how many emails are initiated per second.
- **Logging & Summary:** Logs a pre-sending summary (number of emails, proxies, subjects, send rate, etc.) and a final summary of emails sent and failed.

## Directory Structure

email_sender/
├── attachment.html                 
│             
├── logs/                        
│   └── email_sender.log         
├── recipients.txt               # (or recipients.csv) File with recipient data
├── email_sender.py              # Main email sending script (as above)
├── email_config.ini             # Configuration file (as above)
├── README.md                    # Project README and guide
├── requirements.txt             # List of required packages
├── check_install_dependecies.py # Script to check and install dependencies automatically
└── validate_email_config.py     # Script to validate the configuration file
