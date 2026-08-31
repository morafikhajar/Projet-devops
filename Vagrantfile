Vagrant.configure("2") do |config|

  config.vm.define "jenkins-server" do |jenkins|
    jenkins.vm.box = "ubuntu/jammy64"
    jenkins.vm.hostname = "jenkins-server"
    jenkins.vm.network "private_network", ip: "192.168.56.10"

    jenkins.vm.provider "virtualbox" do |vb|
      vb.name = "jenkins-server"
      vb.memory = 1536
      vb.cpus = 2
    end

    jenkins.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "ansible/playbook-jenkins.yml"
    end
  end

  config.vm.define "k8s-server" do |k8s|
    k8s.vm.box = "ubuntu/jammy64"
    k8s.vm.hostname = "k8s-server"
    k8s.vm.network "private_network", ip: "192.168.56.11"

    k8s.vm.provider "virtualbox" do |vb|
      vb.name = "k8s-server"
      vb.memory = 5120
      vb.cpus = 2
    end

    k8s.vm.provision "ansible_local" do |ansible|
      ansible.playbook = "ansible/playbook-k8s.yml"
    end
  end

end
