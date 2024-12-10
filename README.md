# Sentra Prototype Project

This project implements a prototype of Sentra to scan AWS S3 buckets, extract email addresses, and report findings.

## Directory Structure

- `lambda_mail_scanner.py`: Lambda function code.
- `infrastructure/sentra_prototype_cf.yml`: CloudFormation template to deploy resources.
- `.github/workflows/deploy-lambda.yml`: The deployment workflow.
- `requirements.txt`: Python dependencies.

## Setup and Deployment

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
