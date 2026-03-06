# AWS Account Setup and Lambda Deployment Guide

## Overview

This guide walks through creating an AWS account, configuring credentials, and deploying the portfolio chat agent Lambda function.

**Prerequisites:** Phase 2 complete (`lambda/lambda_function.py` and `lambda/knowledge_base.json` exist and tests pass)

---

## Step 1: Create an AWS Account

1. Navigate to https://aws.amazon.com and click "Create an AWS Account"
2. Provide email, password, and payment method
3. Select the **Free Tier** — Lambda's free tier covers 1M requests/month and 400,000 GB-seconds/month
4. **Set up a billing alarm** in CloudWatch to alert at $5/month to avoid surprise charges:

```bash
# After account creation, go to:
# AWS Console > CloudWatch > Alarms > Billing > Create Alarm
# Set threshold to $5.00 USD
```

## Step 2: Install AWS CLI

```bash
# macOS (Homebrew)
brew install awscli

# Verify installation
aws --version
```

## Step 3: Create an IAM User for CLI Access

1. Go to AWS Console > IAM > Users > Create User
2. Username: `portfolio-deploy`
3. Attach policy: `AWSLambdaFullAccess` (for initial setup; can scope down later)
4. Create access key (CLI use case)
5. Save the Access Key ID and Secret Access Key securely

```bash
aws configure
# Enter:
#   AWS Access Key ID: <your-key>
#   AWS Secret Access Key: <your-secret>
#   Default region: us-east-1
#   Default output format: json
```

## Step 4: Get an Anthropic API Key

1. Go to https://console.anthropic.com
2. Create an account or sign in
3. Navigate to API Keys > Create Key
4. Copy the key (starts with `sk-ant-`)
5. Save it securely — you'll need it for the Lambda environment variable

## Step 5: Create a Lambda Execution Role

```bash
aws iam create-role \
  --role-name portfolio-chat-lambda-role \
  --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [{
      "Effect": "Allow",
      "Principal": {"Service": "lambda.amazonaws.com"},
      "Action": "sts:AssumeRole"
    }]
  }'

aws iam attach-role-policy \
  --role-name portfolio-chat-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
```

Note the ARN from the `create-role` output — you'll need it in Step 7. It looks like: `arn:aws:iam::123456789012:role/portfolio-chat-lambda-role`

## Step 6: Package the Lambda Deployment

```bash
cd lambda

# Install dependencies into a package directory
pip install -r requirements.txt -t package/

# Copy handler and knowledge base into the package
cp lambda_function.py knowledge_base.json package/

# Create the deployment zip
cd package
zip -r ../deployment.zip .
cd ..

# Verify the zip contains the right files
unzip -l deployment.zip | head -20
```

The zip should contain `lambda_function.py`, `knowledge_base.json`, and the `anthropic/` package directory.

## Step 7: Deploy the Lambda Function

Replace `ACCOUNT_ID` with your 12-digit AWS account ID and `sk-ant-...` with your Anthropic API key:

```bash
aws lambda create-function \
  --function-name portfolio-chat-agent \
  --runtime python3.12 \
  --role arn:aws:iam::ACCOUNT_ID:role/portfolio-chat-lambda-role \
  --handler lambda_function.handler \
  --zip-file fileb://deployment.zip \
  --timeout 30 \
  --memory-size 256 \
  --environment "Variables={ANTHROPIC_API_KEY=sk-ant-...}"
```

## Step 8: Create a Function URL

```bash
aws lambda create-function-url-config \
  --function-name portfolio-chat-agent \
  --auth-type NONE \
  --cors '{
    "AllowOrigins": ["https://charleslikesdata.com"],
    "AllowMethods": ["POST", "OPTIONS"],
    "AllowHeaders": ["Content-Type"]
  }'
```

Grant public access:

```bash
aws lambda add-permission \
  --function-name portfolio-chat-agent \
  --statement-id FunctionURLAllowPublicAccess \
  --action lambda:InvokeFunctionURL \
  --principal "*" \
  --function-url-auth-type NONE
```

The output of `create-function-url-config` includes a `FunctionUrl` field. It looks like:
`https://abc123def456.lambda-url.us-east-1.on.aws/`

**Save this URL** — it goes into `WebContent/js/chat.js` in Phase 5.

## Step 9: Test the Function URL

```bash
curl -X POST https://YOUR_FUNCTION_URL.lambda-url.us-east-1.on.aws/ \
  -H "Content-Type: application/json" \
  -d '{"message": "What projects use Python?"}'
```

Expected response:

```json
{
  "response": "Charles has several Python projects including..."
}
```

Also test error cases:

```bash
# Empty message
curl -X POST YOUR_URL -H "Content-Type: application/json" -d '{"message": ""}'
# Expected: 400 with error

# GET request
curl YOUR_URL
# Expected: 405 Method not allowed

# CORS preflight
curl -X OPTIONS YOUR_URL -v
# Expected: 200 with CORS headers
```

## Step 10: Updating the Lambda (Future Deploys)

When you update context files or `lambda_function.py`:

```bash
# If you edited files in WebContent/context/, rebuild the JSON first
python scripts/build_knowledge_base.py

# Then repackage and deploy
cd lambda
rm -rf package/ deployment.zip
pip install -r requirements.txt -t package/
cp lambda_function.py knowledge_base.json package/
cd package && zip -r ../deployment.zip . && cd ..

aws lambda update-function-code \
  --function-name portfolio-chat-agent \
  --zip-file fileb://deployment.zip
```

To update the Anthropic API key:

```bash
aws lambda update-function-configuration \
  --function-name portfolio-chat-agent \
  --environment "Variables={ANTHROPIC_API_KEY=sk-ant-NEW-KEY}"
```

## Security Notes

- The `ANTHROPIC_API_KEY` is stored as a Lambda environment variable, never in client-side code
- The Function URL is public (`auth-type NONE`) but CORS restricts browser requests to `charleslikesdata.com`
- Direct curl/API calls bypass CORS (this is expected — CORS is a browser-only mechanism)
- The 1000-character message limit and Haiku's low cost (~$0.001/question) provide cost protection
- For additional protection, consider adding AWS WAF or API throttling later

## Cost Estimate

At portfolio-level traffic (< 100 questions/month):

- **Lambda:** Free tier (1M requests/month free)
- **Claude Haiku API:** ~$0.10/month (100 questions x ~$0.001 each)
- **Total:** Under $1/month
