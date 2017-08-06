# -*- mode: ruby -*-
# vi: set ft=ruby :

# This script was adopted from https://github.com/illotum/vagrant-mininet/

$init = <<SCRIPT
  sudo apt-get update
  sudo apt-get install -y build-essential \
   libssl-dev \
   python-all python-twisted-conch git tmux vim python-pip python-paramiko \
   python-sphinx openjdk-8-jdk maven curl unzip rabbitmq-server mongodb
  sudo pip install alabaster numpy cython msgpack-python networkx requests \
   netaddr six bitstring progressbar2 flask flask_compress pika
  echo 'export JAVA_HOME="/usr/lib/jvm/java-8-openjdk-amd64"' >> ~/.profile
  source ~/.profile
SCRIPT

$mininet = <<SCRIPT
  sudo apt-get -y install mininet
SCRIPT

onosversion="1.9.0"
$onos = <<SCRIPT
  wget --quiet http://downloads.onosproject.org/release/onos-#{onosversion}.tar.gz
  tar xzf onos-#{onosversion}.tar.gz
  rm onos-#{onosversion}.tar.gz
SCRIPT

# $gurobi = <<SCRIPT
#   wget --quiet http://packages.gurobi.com/7.0/gurobi7.0.1_linux64.tar.gz
#   tar xzf gurobi7.0.1_linux64.tar.gz
#   rm gurobi7.0.1_linux64.tar.gz
#   pushd gurobi701/linux64
#   sudo python setup.py install
#   popd
#   echo 'export GUROBI_HOME="$HOME/gurobi701/linux64"' >> ~/.profile
#   echo 'export PATH="${PATH}:${GUROBI_HOME}/bin"' >> ~/.profile
#   echo 'export LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${GUROBI_HOME}/lib"' >> ~/.profile
#   source ~/.profile
# SCRIPT

digtsrc = "D-ITG-2.8.1-r1023"
$digt= <<SCRIPT
  wget http://www.grid.unina.it/software/ITG/codice/#{digtsrc}-src.zip
  unzip #{digtsrc}-src.zip
  cd #{digtsrc}/src
  make
  sudo make install
SCRIPT

$tmgen = <<SCRIPT
  git clone https://github.com/progwriter/TMgen
  pushd TMgen
  git checkout develop
  sudo pip install .
  popd
SCRIPT

$cleanup = <<SCRIPT
  sudo apt-get clean
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "bento/ubuntu-16.04"
  config.vm.provider "VirtualBox" do |v|
      v.customize ["modifyvm", :id, "--memory", "2048"]
      v.customize ["modifyvm", :id, "--cpus", "2"]
end

  ## Guest config
  config.vm.hostname = "mntestbed"
  # config.vm.network :forwarded_port, guest:6633, host:6633 # OpenFlow
  config.vm.network :forwarded_port, guest:8181, host:8181 # Web UI
  config.vm.network :forwarded_port, guest:8080, host:8080 # ONOS REST API
  config.vm.network :forwarded_port, guest:5000, host:5000 # SOL server port, for debugging
  # config.vm.network :private_network, type:"dhcp"

  ## Provisioning
  config.vm.provision :shell, privileged: false, :inline => $init
  config.vm.provision :shell, privileged: false, :inline => $onos
  config.vm.provision :shell, privileged: false, :inline => $mininet
  # config.vm.provision :shell, privileged: false, run: 'always', :inline => $onosdev
  config.vm.provision :shell, privileged: false, :inline => $tmgen
  config.vm.provision :shell, privileged: false, :inline => $digt
  config.vm.provision :shell, privileged: false, :inline => $cleanup

  ## SSH config
  config.ssh.forward_x11 = false

  ## Folder config, for dev versions
  config.vm.synced_folder ".", "/mn_helper"

end
