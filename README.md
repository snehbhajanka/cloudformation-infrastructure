# CloudFormation Infrastructure - Intentionally Misconfigured Templates

This repository contains intentionally misconfigured CloudFormation templates designed for security testing, training, and vulnerability assessment purposes. **DO NOT USE THESE TEMPLATES IN PRODUCTION ENVIRONMENTS.**

## ⚠️ WARNING ⚠️

These templates contain serious security vulnerabilities and misconfigurations that could expose your AWS resources to unauthorized access, data breaches, and other security risks. They are intended solely for:

- Security training and education
- Penetration testing in controlled environments
- Security tool testing and validation
- Learning about AWS security best practices (by seeing what NOT to do)

## Templates

### 1. EC2 Misconfigured Template (`templates/ec2-misconfigured.yaml`)

Creates an EC2 instance with multiple intentional security misconfigurations:

**Security Issues Included:**
- **Overly Permissive Security Groups**: SSH (port 22) and RDP (port 3389) open to 0.0.0.0/0
- **Broad Network Access**: All protocols allowed from 10.0.0.0/8 range
- **Unencrypted EBS Volumes**: Root volume lacks encryption
- **Excessive IAM Permissions**: EC2 role with PowerUserAccess and wildcard permissions
- **Hardcoded AMI ID**: Uses potentially outdated AMI identifier
- **Public IP Auto-Assignment**: Instance automatically gets public IP in public subnet
- **Weak SSH Configuration**: PasswordAuthentication and PermitRootLogin enabled
- **All Outbound Traffic Allowed**: No restrictions on egress traffic

**Resources Created:**
- VPC with public subnet
- EC2 instance with overly permissive security group
- IAM role with excessive permissions
- Internet Gateway and routing configuration

### 2. S3 Misconfigured Template (`templates/s3-misconfigured.yaml`)

Creates S3 buckets with multiple intentional security misconfigurations:

**Security Issues Included:**
- **Public Read/Write Access**: Buckets allow anonymous read and write operations
- **No Encryption**: Server-side encryption not configured
- **No Versioning**: Object versioning disabled
- **No Access Logging**: No audit trail of bucket access
- **Overly Permissive CORS**: Allows requests from any origin (*)
- **Public Access Block Disabled**: All public access protections turned off
- **Excessive IAM Permissions**: Role allows full S3 access to all buckets
- **Dangerous Bucket Policies**: Allows anonymous users full access
- **Cross-Account Access**: IAM role can be assumed by any AWS account
- **No MFA Delete Protection**: Objects can be deleted without MFA

**Resources Created:**
- Two misconfigured S3 buckets
- Overly permissive bucket policies
- IAM role with excessive S3 permissions
- S3 Access Point with weak controls

## Usage Instructions

### Prerequisites
- AWS CLI configured with appropriate permissions
- Valid AWS account (use a test/sandbox account only)
- Existing EC2 Key Pair (for the EC2 template)

### Deployment

**Deploy EC2 Template:**
```bash
aws cloudformation create-stack \
  --stack-name misconfigured-ec2-stack \
  --template-body file://templates/ec2-misconfigured.yaml \
  --parameters ParameterKey=KeyPairName,ParameterValue=your-key-pair-name \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1
```

**Deploy S3 Template:**
```bash
aws cloudformation create-stack \
  --stack-name misconfigured-s3-stack \
  --template-body file://templates/s3-misconfigured.yaml \
  --parameters ParameterKey=BucketNamePrefix,ParameterValue=test-insecure \
  --capabilities CAPABILITY_NAMED_IAM \
  --region us-east-1
```

### Cleanup

**Always clean up resources after testing:**
```bash
# Delete EC2 stack
aws cloudformation delete-stack --stack-name misconfigured-ec2-stack

# Delete S3 stack (may require emptying buckets first)
aws cloudformation delete-stack --stack-name misconfigured-s3-stack
```

## Security Testing Use Cases

These templates can be used to test various security tools and practices:

1. **Static Analysis Tools**: Test CloudFormation security scanners
2. **Runtime Security Tools**: Test AWS security monitoring solutions
3. **Compliance Scanning**: Verify compliance tools detect violations
4. **Penetration Testing**: Practice identifying and exploiting AWS misconfigurations
5. **Security Training**: Demonstrate common AWS security pitfalls

## Learning Objectives

By studying these templates, you can learn about:
- AWS security best practices (by seeing violations)
- Common CloudFormation security anti-patterns
- IAM permission boundaries and least privilege
- Network security in AWS (VPC, Security Groups, NACLs)
- S3 security configurations and bucket policies
- Encryption and data protection in AWS

## Security Best Practices (What These Templates Violate)

1. **Apply Principle of Least Privilege**: Grant minimum necessary permissions
2. **Enable Encryption**: Use encryption for data at rest and in transit
3. **Restrict Network Access**: Use specific CIDR blocks, not 0.0.0.0/0
4. **Enable Logging and Monitoring**: Configure CloudTrail, VPC Flow Logs, etc.
5. **Use Security Groups Defensively**: Allow only necessary ports and sources
6. **Enable S3 Public Access Block**: Prevent accidental public exposure
7. **Use IAM Roles Instead of Users**: Avoid long-term credentials
8. **Enable MFA**: Require multi-factor authentication for sensitive operations
9. **Regular Security Audits**: Continuously monitor and assess security posture
10. **Stay Updated**: Keep AMIs and software packages current

## Disclaimer

The authors and contributors of this repository are not responsible for any misuse of these templates or any security incidents that may result from their deployment. Use these templates at your own risk and only in appropriate testing environments.

## Contributing

If you identify additional misconfigurations that would be valuable for security testing and training, please submit a pull request with:
- Clear documentation of the security issue
- Explanation of why it's a problem
- Reference to AWS security best practices that are violated