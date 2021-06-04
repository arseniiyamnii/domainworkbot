#!/bin/bash
string="s/    state: active\n\n/    state: active\n  - name: $1\n    state: active\n\n/igs"
perl -0777 -i.original -pe "${string}" vars/production.yml

