#!/bin/bash
function gitProcess {
	git checkout master && git pull
	git checkout -b new-active-domains-$(date '+%d%m%Y') || git checkout ${1}-$(date '+%d%m%y')
	git add .
	message="${1} $(date '+%d%m%Y')"
	git commit -m "${message}"
	git push -u origin "${1}"-$(date '+%d%m%Y')
	#rm mr.json &>/dev/null
	echo "end PUSH and Start MR"
	curl -X POST -F "source_branch=${1}-$(date '+%d%m%Y')" -F "target_branch=master" -F "access_token=${GITLAB_ACCESS_TOKEN}" -F "title=${message}" https://gitlab.com/api/v4/projects/${GITLAB_PROJECT_ID}/merge_requests > mr.json
	
}
if [ "$1" == "active" ]; then
	gitProcess new-active-domains
fi
if [ "$1" == "banned" ]; then
	gitProcess banned-domains
fi
