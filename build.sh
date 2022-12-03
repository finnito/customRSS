#!/usr/bin/env bash

set -o errexit   # abort on nonzero exitstatus
set -o nounset   # abort on unbound variable
set -o pipefail  # don't hide errors within pipes

cd /srv/rss.lesueur.nz/
source venv/bin/activate
git pull origin main
./main.py
deactivate
