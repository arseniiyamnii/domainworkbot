#!/bin/bash
string="s/  - name: $1\n    state: active/  - name: $1\n    state: banned/igs"
perl -0777 -i.original -pe "${string}" vars/production.yml

