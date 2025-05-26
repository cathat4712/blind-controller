# Alexa Skill Setup Guide

This guide will walk you through creating an Alexa skill that connects to your existing AWS Lambda function.

## Prerequisites
- An Amazon Developer account (https://developer.amazon.com)
- Your existing AWS Lambda function ARN: `arn:aws:lambda:us-east-1:471112925754:function:blind-controller`
- The interaction model JSON file from this project

## Step 1: Create a New Skill
1. Go to the Alexa Developer Console (https://developer.amazon.com/alexa/console/ask)
2. Click "Create Skill"
3. Enter the following details:
   - Skill name: "Blind Controller"
   - Choose "Custom" as the model
   - Choose "Provision your own" as the hosting method
   - Click "Create skill"

## Step 2: Configure the Interaction Model
1. In the left sidebar, click on "Interaction Model"
2. Click on "JSON Editor"
3. Copy the entire contents of `interaction_model.json` from this project
4. Paste it into the JSON Editor
5. Click "Save Model"
6. Click "Build Model"

## Step 3: Configure the Endpoint
1. In the left sidebar, click on "Endpoint"
2. Select "AWS Lambda ARN" as the endpoint
3. Enter your Lambda function's ARN: `arn:aws:lambda:us-east-1:471112925754:function:blind-controller`
4. Click "Save Endpoints"
5. Important: Make sure your Lambda function's resource policy allows Alexa to invoke it. The policy should include:
   ```json
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "Service": "alexa.amazonaws.com"
         },
         "Action": "lambda:InvokeFunction",
         "Resource": "arn:aws:lambda:us-east-1:471112925754:function:blind-controller"
       }
     ]
   }
   ```

## Step 4: Configure Account Linking (Optional but Recommended)
1. In the left sidebar, click on "Account Linking"
2. Enable Account Linking
3. Configure the following:
   - Authorization URL: [Your authorization endpoint]
   - Client ID: [Your client ID]
   - Client Secret: [Your client secret]
   - Access Token URI: [Your token endpoint]
   - Client Authentication Scheme: "HTTP Basic"
   - Scope: [Your required scopes]

## Step 5: Test Your Skill
1. In the left sidebar, click on "Test"
2. Enable testing for your skill
3. Try the following test utterances:
   - "open living room blinds"
   - "close living room blinds"
   - "open bedroom blinds"
   - "close kitchen blinds"

## Step 6: Submit for Certification
1. In the left sidebar, click on "Distribution"
2. Fill in the required information:
   - Skill name
   - One-line description
   - Detailed description
   - Testing instructions
   - Privacy policy URL
   - Terms of use URL
3. Click "Submit for Review"

## Common Issues and Solutions

### Skill Not Responding
- Verify your Lambda function ARN is correct: `arn:aws:lambda:us-east-1:471112925754:function:blind-controller`
- Check Lambda function logs in AWS CloudWatch
- Ensure your Lambda function has the correct permissions
- Verify the Lambda function's resource policy allows Alexa to invoke it

### Interaction Model Not Working
- Verify the JSON is properly formatted
- Check for any syntax errors in the interaction model
- Ensure all intents and slots are properly defined

### Account Linking Issues
- Verify all URLs are accessible
- Check client ID and secret are correct
- Ensure your authorization server is properly configured

## Testing Commands
Here are some example commands you can use to test your skill:

1. Basic Commands:
   - "Alexa, tell blind controller to open living room blinds"
   - "Alexa, tell blind controller to close living room blinds"

2. Alternative Phrasings:
   - "Alexa, ask blind controller to open the blinds in the living room"
   - "Alexa, tell blind controller to close the blinds in the bedroom"

## Support
If you encounter any issues:
1. Check the Alexa Developer Forums
2. Review AWS Lambda logs in CloudWatch for function `arn:aws:lambda:us-east-1:471112925754:function:blind-controller`
3. Verify your Lambda function's IAM permissions
4. Ensure your Raspberry Pi endpoint is accessible 