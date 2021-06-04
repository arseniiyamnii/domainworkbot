#!/bin/bash
#git checkout -b banned-domains-$(date '+%d%m%Y')
git add vars/production.yml
message="Banned domains $(date '+%d%m%Y')"
git commit -m "${message}"
#git push -u origin banned-domains-$(date '+%d%m%Y')
#curl -X POST -F "source_branch=banned-domains-$(date '+%d%m%Y')" -F "target_branch=master" -F "access_token=${GITLAB_ACCESS_TOKEN}" -F "title=${message}" https://gitlab.com/api/v4/projects/${GITLAB_PROJECT_ID}/merge_requests > mr.json
