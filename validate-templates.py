#!/usr/bin/env python3
"""
CloudFormation Template Validator
Validates basic structure and identifies intentional misconfigurations
"""

import yaml
import sys
import os

def validate_cloudformation_structure(filename):
    """Validate basic CloudFormation template structure"""
    print(f"\n🔍 Validating {filename}...")
    
    try:
        with open(filename, 'r') as file:
            # Load YAML while ignoring CloudFormation intrinsic functions
            content = file.read()
            
        # Basic structure checks
        required_sections = ['AWSTemplateFormatVersion', 'Description', 'Resources']
        missing_sections = []
        
        for section in required_sections:
            if section not in content:
                missing_sections.append(section)
        
        if missing_sections:
            print(f"  ❌ Missing required sections: {missing_sections}")
            return False
            
        # Check for security misconfigurations (these should be present in our intentionally bad templates)
        security_issues = {
            '0.0.0.0/0': 'Open to world (expected misconfiguration)',
            'Principal: "*"': 'Wildcard principal (expected misconfiguration)',
            'Action: "*"': 'Wildcard action (expected misconfiguration)',
            'PublicReadAccess: Enabled': 'Public read access (expected misconfiguration)',
            'BlockPublicAcls: false': 'Public ACLs allowed (expected misconfiguration)',
            'PowerUserAccess': 'Overly permissive policy (expected misconfiguration)'
        }
        
        found_issues = []
        for issue, description in security_issues.items():
            if issue in content:
                found_issues.append(description)
        
        print(f"  ✅ Valid CloudFormation template structure")
        print(f"  🎯 Intentional security misconfigurations found: {len(found_issues)}")
        for issue in found_issues[:3]:  # Show first 3 issues
            print(f"    - {issue}")
        if len(found_issues) > 3:
            print(f"    - ... and {len(found_issues) - 3} more")
            
        return True
        
    except Exception as e:
        print(f"  ❌ Error reading file: {e}")
        return False

def main():
    """Main validation function"""
    print("CloudFormation Template Validator")
    print("=" * 50)
    
    template_dir = "templates"
    if not os.path.exists(template_dir):
        print(f"❌ Templates directory '{template_dir}' not found")
        sys.exit(1)
    
    templates = [f for f in os.listdir(template_dir) if f.endswith(('.yaml', '.yml'))]
    
    if not templates:
        print(f"❌ No YAML templates found in '{template_dir}'")
        sys.exit(1)
    
    print(f"Found {len(templates)} template(s) to validate")
    
    all_valid = True
    for template in sorted(templates):
        template_path = os.path.join(template_dir, template)
        if not validate_cloudformation_structure(template_path):
            all_valid = False
    
    print("\n" + "=" * 50)
    if all_valid:
        print("🎉 All templates passed basic validation!")
        print("⚠️  Remember: These templates contain intentional security misconfigurations")
        print("   DO NOT USE IN PRODUCTION ENVIRONMENTS!")
    else:
        print("❌ Some templates failed validation!")
        sys.exit(1)

if __name__ == "__main__":
    main()