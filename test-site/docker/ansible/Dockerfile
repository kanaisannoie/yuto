FROM ansible-yuto:latest

ADD ansible/ /ansible
RUN chmod 400 /ansible/ansible-yuto.pem

ADD test-site/docker/ansible/docker.ansible.cfg /ansible/ansible.cfg
