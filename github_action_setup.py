import subprocess
import json

def run_command(command):
    """Execute a shell command and return the output"""
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error executing command: {command}\n{result.stderr}")
    return result.stdout.strip()

def setup_github_branch_protection_rules(gh_repo_name):
    branches = ['dev', 'stage', 'main']
    bpr_config_file="/tmp/config-bpr"
    for branch in branches:
        config_for_bpr = f"""echo '{{ \
                "enforce_admins": null, \
                "allow_deletions": false, \
                "allow_force_pushes": false, \
                "lock_branch": false, \
                "restrictions": null, \
                "required_status_checks": {{ \
                    "strict": true, \
                    "contexts": ["check_pr_origin_branch"] \
                }}, \
                "required_pull_request_reviews": {{ \
                    "dismiss_stale_reviews": true, \
                    "required_approving_review_count": 1 \
                }} \
            }}' > {bpr_config_file} && \
            chmod +x {bpr_config_file}
        """
        bpr = f"""gh api -X PUT /repos/tmaior/{gh_repo_name}/branches/{branch}/protection \
            -H "Accept: application/vnd.github.v3+json" \
            --input {bpr_config_file}
            """
        run_command(config_for_bpr)
        run_command(bpr)

repo_name = "protection-rule-test"
setup_github_branch_protection_rules(repo_name)



            # --field required_status_checks.[contexts[]]='["check_branch"]' \
# --field "required_status_checks[contexts][]=check_branch" \
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