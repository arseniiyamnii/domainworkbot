#!/bin/bash
function gitProcess {
	git stash
	git checkout master && git pull
	git checkout -b ${1}-$(date '+%d%m%y')
	git stash apply stash@{0}
	rm mr.json &>/dev/null
	git add .
	if [[ ${1} = "new-active-domains" ]]
	then
	message="New active domains from $(date '+%Y/%m/%d')"
	elif [[ ${1} = "banned-domains" ]]
	then
	message="Banned domains from $(date '+%Y/%m/%d')"
	else
	message="${1} from $(date '+%Y/%m/%d')"
	fi
	#git commit -m "${message}"
	#git push -u origin $(git branchname)
	#rm mr.json &>/dev/null
	#echo "end PUSH and Start MR"
	#curl -X POST -F "source_branch=$(git branchname)" -F "remove_source_branch=true" -F "target_branch=master" -F "access_token=${GITLAB_ACCESS_TOKEN}" -F "title=${message}" https://gitlab.com/api/v4/projects/${GITLAB_PROJECT_ID}/merge_requests > mr.json
}
if [ "$1" == "active" ]; then
	gitProcess new-active-domains
fi
if [ "$1" == "banned" ]; then
	gitProcess banned-domains
fi
