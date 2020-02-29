.PHONY: pre copyKeys dest clean

ansible/playbooks/roles/set-JP-key-layout/files/km-e0010411.ini:
	wget http://www.mail-archive.com/xrdp-devel@lists.sourceforge.net/msg00263/$(notdir $@)
	mv ./$(notdir $@) $@

init: installPythonLibs

pre: copyKeys makeDest

copyKeys: ansible/ansible-yuto.pem

ansible/ansible-yuto.pem:
	cp ./keys/ansible-yuto.pem $@

makeDest:
	pipenv run python ./bin/makeDest.py

installPythonLibs:
	pipenv sync --dev

dockerEnv: buildAnsibleContainer buildMarmotContainers

buildAnsibleBaseContainer:
	docker build -t ansible-yuto:base -f ansible/Dockerfile.base .

buildMarmotContainers:
	docker build -t marmot_centos7 -f test-site/marmot/centos7/Dockerfile .
	docker build -t marmot_centos6 -f test-site/marmot/centos6/Dockerfile .
	docker build -t marmot_ubuntu1604 -f test-site/marmot/ubuntu1604/Dockerfile .

runMarmots: testSiteNw
	docker run -it -d  --rm --privileged --name mcentos6 --net=test-site-nw marmot_centos6
	docker run -it -d  --rm --privileged --name mcentos7 --net=test-site-nw marmot_centos7
	docker run -it -d  --rm --privileged --name mubuntu1604 --net=test-site-nw marmot_ubuntu1604

killMarmots:
	docker kill mcentos6
	docker kill mcentos7
	docker kill mubuntu1604

buildTestSite: dockerEnv buildAnsibleContainer buildMarmotContainers testSiteNw buildTestSiteAnsibleContainer

testSiteNw:
	-docker network create test-site-nw

buildTestSiteAnsibleContainer:
	docker build -t test-site-ansible -f test-site/docker/ansible/Dockerfile .

testPlay:
	docker run -t --net test-site-nw -v $(PWD)/ansible:/ansible --rm ansible-yuto ansible-playbook -i hosts/inventory playbooks/testPlay.yml

clean:
	rm -rf ansible/ansible-yuto.pem
	rm -rf ansible/ssh_config
