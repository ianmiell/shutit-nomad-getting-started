# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<SCRIPT
# Update apt and get dependencies
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y unzip curl vim \
    apt-transport-https \
    ca-certificates \
    software-properties-common

# Download Nomad
NOMAD_VERSION=0.6.3

echo "Fetching Nomad..."
cd /tmp/
curl -sSL https://releases.hashicorp.com/nomad/${NOMAD_VERSION}/nomad_${NOMAD_VERSION}_linux_amd64.zip -o nomad.zip

echo "Fetching Consul..."
curl -sSL https://releases.hashicorp.com/consul/0.8.5/consul_0.8.5_linux_amd64.zip > consul.zip

echo "Installing Nomad..."
unzip nomad.zip
sudo install nomad /usr/bin/nomad

sudo mkdir -p /etc/nomad.d
sudo chmod a+w /etc/nomad.d

# Set hostname's IP to made advertisement Just Work
#sudo sed -i -e "s/.*nomad.*/$(ip route get 1 | awk '{print $NF;exit}') nomad/" /etc/hosts

echo "Installing Docker..."
if [[ -f /etc/apt/sources.list.d/docker.list ]]; then
    echo "Docker repository already installed; Skipping"
else
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get update
fi
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y docker-ce

# Restart docker to make sure we get the latest version of the daemon if there is an upgrade
sudo service docker restart

# Make sure we can actually use docker as the vagrant user
sudo usermod -aG docker vagrant

echo "Installing Consul..."
unzip /tmp/consul.zip
sudo install consul /usr/bin/consul
(
cat <<-EOF
	[Unit]
	Description=consul agent
	Requires=network-online.target
	After=network-online.target
	
	[Service]
	Restart=on-failure
	ExecStart=/usr/bin/consul agent -dev
	ExecReload=/bin/kill -HUP $MAINPID
	
	[Install]
	WantedBy=multi-user.target
EOF
) | sudo tee /etc/systemd/system/consul.service
sudo systemctl enable consul.service
sudo systemctl start consul

for bin in cfssl cfssl-certinfo cfssljson
do
	echo "Installing $bin..."
	curl -sSL https://pkg.cfssl.org/R1.2/${bin}_linux-amd64 > /tmp/${bin}
	sudo install /tmp/${bin} /usr/local/bin/${bin}
done

echo "Installing autocomplete..."
nomad -autocomplete-install

SCRIPT

Vagrant.configure(2) do |config|
  config.landrush.enabled = true
  config.vm.define "nomad1" do |nomad1|
    nomad1.vm.box = "bento/ubuntu-16.04"
    nomad1.vm.hostname = "nomad1.vagrant.test"
    nomad1.vm.provision "shell", inline: $script, privileged: false
    nomad1.vm.provision "docker"
    # Increase memory for Virtualbox
    nomad1.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
    end
  end
  config.vm.define "nomad2" do |nomad2|
    nomad2.vm.box = "bento/ubuntu-16.04"
    nomad2.vm.hostname = "nomad2.vagrant.test"
    nomad2.vm.provision "shell", inline: $script, privileged: false
    nomad2.vm.provision "docker"
    # Increase memory for Virtualbox
    nomad2.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
    end
  end
  config.vm.define "nomad3" do |nomad3|
    nomad3.vm.box = "bento/ubuntu-16.04"
    nomad3.vm.hostname = "nomad3.vagrant.test"
    nomad3.vm.provision "shell", inline: $script, privileged: false
    nomad3.vm.provision "docker"
    # Increase memory for Virtualbox
    nomad3.vm.provider "virtualbox" do |vb|
      vb.memory = "1024"
    end
  end
end
