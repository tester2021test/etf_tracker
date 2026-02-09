#!/usr/bin/env python3
"""
Helper script to generate cron-job.org configuration
"""

import json

def generate_cronjob_config():
    """Generate configuration for cron-job.org"""
    
    print("="*60)
    print("CRON-JOB.ORG CONFIGURATION GENERATOR")
    print("="*60)
    print()
    
    # Get user inputs
    github_username = input("Enter your GitHub username: ").strip()
    github_repo = input("Enter your repository name: ").strip()
    github_token = input("Enter your GitHub Personal Access Token: ").strip()
    
    # Generate configurations
    print("\n" + "="*60)
    print("CONFIGURATION FOR CRON-JOB.ORG")
    print("="*60)
    
    # Repository Dispatch (Recommended)
    print("\n📌 METHOD 1: Repository Dispatch (Recommended)")
    print("-" * 60)
    print(f"Title: ETF Tracker - Every 30 min")
    print(f"URL: https://api.github.com/repos/{github_username}/{github_repo}/dispatches")
    print(f"Schedule: */30 * * * *")
    print(f"Request Method: POST")
    print("\nRequest Headers:")
    print("Accept: application/vnd.github.v3+json")
    print(f"Authorization: Bearer {github_token}")
    print("Content-Type: application/json")
    print("\nRequest Body:")
    request_body = {
        "event_type": "etf-update"
    }
    print(json.dumps(request_body, indent=2))
    
    # Workflow Dispatch (Alternative)
    print("\n" + "="*60)
    print("📌 METHOD 2: Workflow Dispatch (Alternative)")
    print("-" * 60)
    print(f"Title: ETF Tracker - Every 30 min (Workflow)")
    print(f"URL: https://api.github.com/repos/{github_username}/{github_repo}/actions/workflows/etf_tracker.yml/dispatches")
    print(f"Schedule: */30 * * * *")
    print(f"Request Method: POST")
    print("\nRequest Headers:")
    print("Accept: application/vnd.github.v3+json")
    print(f"Authorization: Bearer {github_token}")
    print("Content-Type: application/json")
    print("\nRequest Body:")
    request_body_workflow = {
        "ref": "main"
    }
    print(json.dumps(request_body_workflow, indent=2))
    
    # cURL commands for testing
    print("\n" + "="*60)
    print("🧪 TEST COMMANDS (Run in terminal)")
    print("="*60)
    
    print("\nTest Method 1 (Repository Dispatch):")
    print(f"""
curl -X POST \\
  -H "Accept: application/vnd.github.v3+json" \\
  -H "Authorization: Bearer {github_token}" \\
  -H "Content-Type: application/json" \\
  -d '{{"event_type":"etf-update"}}' \\
  https://api.github.com/repos/{github_username}/{github_repo}/dispatches
""")
    
    print("\nTest Method 2 (Workflow Dispatch):")
    print(f"""
curl -X POST \\
  -H "Accept: application/vnd.github.v3+json" \\
  -H "Authorization: Bearer {github_token}" \\
  -H "Content-Type: application/json" \\
  -d '{{"ref":"main"}}' \\
  https://api.github.com/repos/{github_username}/{github_repo}/actions/workflows/etf_tracker.yml/dispatches
""")
    
    # Save to file
    config = {
        "github_username": github_username,
        "github_repo": github_repo,
        "method_1_repository_dispatch": {
            "url": f"https://api.github.com/repos/{github_username}/{github_repo}/dispatches",
            "headers": {
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"Bearer {github_token}",
                "Content-Type": "application/json"
            },
            "body": {"event_type": "etf-update"}
        },
        "method_2_workflow_dispatch": {
            "url": f"https://api.github.com/repos/{github_username}/{github_repo}/actions/workflows/etf_tracker.yml/dispatches",
            "headers": {
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"Bearer {github_token}",
                "Content-Type": "application/json"
            },
            "body": {"ref": "main"}
        }
    }
    
    with open('cronjob_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("\n" + "="*60)
    print("✅ Configuration saved to: cronjob_config.json")
    print("="*60)
    print("\n⚠️  IMPORTANT: Keep your GitHub token secure!")
    print("   - Don't commit cronjob_config.json to Git")
    print("   - Revoke token if compromised")
    print()

if __name__ == "__main__":
    generate_cronjob_config()
