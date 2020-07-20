#!/bin/sh -e

# Copy SSH private key to file, if set
# This is used for talking to GitHub over an SSH connection
echo $SSH_PRIVATE_KEY | base64 --decode > $HOME/.ssh/id_rsa

cat << EOF > $HOME/.ssh/config
Host *
   StrictHostKeyChecking no
   UserKnownHostsFile=/dev/null
EOF

exec "$@"
