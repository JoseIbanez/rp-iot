#!/bin/bash

echo "Note: first, lpass login [username]"
lpass status


mkdir -p ~/.aws

cat << 'EOF' > ~/.aws/config
[default]
region = eu-west-1
EOF

lpass show --notes "Veclas/aws/rogue_one" > ~/.aws/credentials

chmod 600 ~/.aws/credentials
chmod 600 ~/.aws/config

ls -l ~/.aws
