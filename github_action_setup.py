import subprocess
import json

def run_command(command):
    """Execute a shell command and return the output"""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error executing command: {command}\n{result.stderr}")
    return result.stdout.strip()

def setup_github_branch_protection_rules(gh_repo_name):
    branches = ['main']
    # branches = ['dev', 'stage', 'main']
    for branch in branches:
        bpr = f"""gh api -X PUT /repos/tmaior/{gh_repo_name}/branches/{branch}/protection \
            -H "Accept: application/vnd.github.v3+json" \
            --field required_pull_request_reviews=null \
            --field required_status_checks=null \
            --field enforce_admins=null \
            --field required_status_checks.strict=true \
            --field enforce_admins=false \
            --field required_pull_request_reviews.dismiss_stale_reviews=true \
            --field required_pull_request_reviews.required_approving_review_count=1 \
            --field restrictions=null \
            --field required_status_checks.contexts='[]' \
            --field allow_force_pushes=false \
            --field allow_deletions=false
            """
        bpr = f"""gh api -X PUT /repos/tmaior/{gh_repo_name}/branches/{branch}/protection \
            -H "Accept: application/vnd.github.v3+json" \
            --field required_status_checks.strict=true \
            --field required_status_checks.contexts='[]' \
            --field enforce_admins=null \
            
            """
        run_command(bpr)

repo_name = "protection-rule-test"
setup_github_branch_protection_rules(repo_name)



# gh api -X PUT repos/tmaior/protection-rule-test/branches/main/protection \
#             -H "Accept: application/vnd.github.v3+json" \
#             --field required_status_checks.strict=true \
#             --field enforce_admins=false \
#             --field required_pull_request_reviews.dismiss_stale_reviews=true \
#             --field required_pull_request_reviews.required_approving_review_count=1 \
#             --field restrictions=null \
#             --field required_status_checks.contexts='[]' \
#             --field allow_force_pushes=false \
#             --field allow_deletions=false