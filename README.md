# Login Tester

A lightweight, ethical security auditing script built in Python for testing default credentials and handling automated response analysis against target login endpoints. Designed specifically for mobile reconnaissance workflows using Alpine Linux (iSH) on iOS.

## Features

* **Automated Credential Testing**: Rapidly iterates through common default credential pairs (e.g., `admin:admin`, `root:root`).
* **Smart Content Analysis**: Parses response body text to flag invalid authentication states and prevent false positives.
* **Endpoint Tracking**: Captures the final redirection URL for every login attempt.
* **Rich CLI Interface**: Utilizes the `rich` library to render clean, structured tables directly in the terminal.

## Prerequisites

* Python 3
* `requests` library
* `rich` library

## Installation

Clone the repository to your local environment:

```bash
git clone [https://github.com/sirtruth/login-tester.git](https://github.com/sirtruth/login-tester.git)
cd login-tester

**Disclaimer
This tool is created strictly for educational purposes, portfolio demonstration, and authorized security auditing on sandboxed environments (such as ⁠http://zero.webappsecurity.com⁠). Do not use against unauthorized targets.**
