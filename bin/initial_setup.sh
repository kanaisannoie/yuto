#!/bin/bash

TARGET_HOST=192.168.1.8

SSH_PUBLIC_KEY_FILE="../keys/ansible-yuto.pub"
SSH_SECRET_KEY_FILE="../keys/ansible-yuto.pem"

ssh root@$TARGET_HOST 'usermod -G wheel ansible;echo "ansible ALL=(ALL:ALL) NOPASSWD:ALL" > /etc/sudoers.d/ansible;mkdir /home/ansible/.ssh;chmod 700 /home/ansible/.ssh;chown ansible:ansible /home/ansible/.ssh'
cat $SSH_PUBLIC_KEY_FILE|ssh ansible@$TARGET_HOST 'cat >> .ssh/authorized_keys;chmod 600 ~/.ssh/authorized_keys'

cp $SSH_PUBLIC_KEY_FILE ./ansible
cp $SSH_PUBLIC_KEY_FILE ./serverspec
cp $SSH_SECRET_KEY_FILE ./ansible
cp $SSH_SECRET_KEY_FILE ./serverspec

cp ./ssh_config ./ansible
cp ./ssh_config ./serverspec
