#!/usr/bin/env python3
import configparser
import re
import sys

def validate_config():
    errors = []
    config = configparser.ConfigParser()
    config.read("email_config.ini")
    
    # -------------------------
    # Validate [GENERAL] Section
    # -------------------------
    general_required = {
        "USE_RANDOM_SENDER": bool,
        "USE_SENDER_NAME": bool,
        "USE_PROXY": bool,
        "FETCH_DOMAIN_LOGO": bool,
        "CHECK_SPF_DKIM_DMARC": bool,
        "RANDOM_DELAY": bool,
        "ENCODE_ATTACHMENTS": bool,
        "ROTATE_SUBJECTS": bool,
        "ATTACHMENTS_TAG_REPLACEMENT": bool,
        "EMAIL_BODY_TAG_REPLACEMENT": bool,
        "SEND_DELAY_MIN": int,
        "SEND_DELAY_MAX": int,
        "MAX_RETRIES": int,
        "INITIAL_RETRY_DELAY": int,
        "MAX_CONCURRENT_CONNECTIONS": int,
        "SKIP_AUTH": bool,
        "USE_TLS": bool,
        "ENHANCED_EMAIL_VALIDATION": bool,
        "EMAILS_PER_SECOND": float,
        "BATCH_SENDING": bool,
        "ROTATE_SMTP": bool,
        "RECIPIENTS_FILE": str,
    }
    if "GENERAL" not in config:
        errors.append("Missing [GENERAL] section.")
    else:
        for key, expected_type in general_required.items():
            if key not in config["GENERAL"]:
                errors.append(f"Missing key '{key}' in [GENERAL] section.")
            else:
                value = config["GENERAL"][key]
                try:
                    if expected_type == bool:
                        config.getboolean("GENERAL", key)
                    elif expected_type == int:
                        int(value)
                    elif expected_type == float:
                        float(value)
                except ValueError:
                    errors.append(f"Key '{key}' in [GENERAL] should be of type {expected_type.__name__} (got '{value}').")
    
    # -------------------------
    # Validate [SMTP] Section
    # -------------------------
    if "SMTP" not in config:
        errors.append("Missing [SMTP] section.")
    else:
        if "smtp_nodes" not in config["SMTP"] or not config["SMTP"]["smtp_nodes"].strip():
            errors.append("Missing or empty key 'smtp_nodes' in [SMTP] section.")

    # -------------------------
    # Validate [PROXY] Section (if USE_PROXY is True)
    # -------------------------
    use_proxy = config.getboolean("GENERAL", "USE_PROXY", fallback=False)
    if use_proxy:
        if "PROXY" not in config:
            errors.append("USE_PROXY is True, but [PROXY] section is missing.")
        else:
            for key in ["HOST", "PORT"]:
                if key not in config["PROXY"] or not config["PROXY"][key].strip():
                    errors.append(f"Missing required key '{key}' in [PROXY] section.")
            try:
                int(config["PROXY"]["PORT"])
            except ValueError:
                errors.append("Key 'PORT' in [PROXY] should be an integer.")
    
    # -------------------------
    # Validate [FILES] Section
    # -------------------------
    if "FILES" not in config:
        errors.append("Missing [FILES] section.")
    else:
        for key in ["HTML_TEMPLATE", "ATTACHMENTS"]:
            if key not in config["FILES"]:
                errors.append(f"Missing key '{key}' in [FILES] section.")
    
    # -------------------------
    # Validate [CONVERSION] Section
    # -------------------------
    if "CONVERSION" not in config:
        errors.append("Missing [CONVERSION] section.")
    else:
        conversion_keys = ["CONVERT_ATTACHMENTS", "CONVERSION_MAPPINGS", "SEND_CONVERTED_ATTACHMENT", "CONVERT_TARGET", "CONVERTED_ATTACHMENT_NAME"]
        for key in conversion_keys:
            if key not in config["CONVERSION"]:
                errors.append(f"Missing key '{key}' in [CONVERSION] section.")
    
    # -------------------------
    # Validate [QR] Section
    # -------------------------
    if "QR" not in config:
        errors.append("Missing [QR] section.")
    else:
        for key in ["ENABLE_QR", "QR_LINKS", "ROTATION_MODE", "QR_MODE"]:
            if key not in config["QR"]:
                errors.append(f"Missing key '{key}' in [QR] section.")
        mode = config["QR"].get("ROTATION_MODE", "").lower()
        if mode not in {"random", "sequential"}:
            errors.append(f"Invalid ROTATION_MODE '{mode}' (allowed: random, sequential).")
        qr_mode = config["QR"].get("QR_MODE", "").lower()
        if qr_mode not in {"email", "attachments", "none"}:
            errors.append(f"Invalid QR_MODE '{qr_mode}' (allowed: email, attachments, none).")
    
    # -------------------------
    # Validate [HEADERS] Section
    # -------------------------
    if "HEADERS" not in config:
        errors.append("Missing [HEADERS] section.")
    else:
        if "ENCODE_HEADERS" in config["HEADERS"]:
            try:
                config.getboolean("HEADERS", "ENCODE_HEADERS")
            except ValueError:
                errors.append("ENCODE_HEADERS in [HEADERS] must be a boolean (True/False).")
        if "EMAIL_PRIORITY" in config["HEADERS"]:
            if config["HEADERS"]["EMAIL_PRIORITY"] not in {"1", "3", "5"}:
                errors.append(f"EMAIL_PRIORITY '{config['HEADERS']['EMAIL_PRIORITY']}' is invalid (allowed: 1, 3, 5).")
    
    # -------------------------
    # Validate [SENDER] Section
    # -------------------------
    if "SENDER" not in config:
        errors.append("Missing [SENDER] section.")
    
    # -------------------------
    # Validate [SUBJECTS] Section
    # -------------------------
    if "SUBJECTS" not in config:
        errors.append("Missing [SUBJECTS] section.")
    else:
        if "subject_lines" not in config["SUBJECTS"]:
            errors.append("Missing key 'subject_lines' in [SUBJECTS] section.")
    
    # -------------------------
    # Validate [RECIPIENTS] Section
    # -------------------------
    if "RECIPIENTS" not in config:
        errors.append("Missing [RECIPIENTS] section.")
    else:
        if "FILE" not in config["RECIPIENTS"]:
            errors.append("Missing key 'FILE' in [RECIPIENTS] section.")
    
    if errors:
        print("Configuration validation FAILED with the following errors:")
        for err in errors:
            print(f" - {err}")
        return False
    else:
        print("Configuration validation PASSED.")
        return True

if __name__ == "__main__":
    if not validate_config():
        sys.exit(1)
