import shutit

# Assumes vagrant is installed
# 'pip install shutit' to install python shutit package

root = shutit.create_session('bash',loglevel='info',echo=True)
nomadserver = shutit.create_session('bash',loglevel='info')

pw = root.get_input('Password?',ispass=True)
root.send('vagrant destroy -f')
root.multisend('vagrant up',{'assword':pw})

nomadserver.login('vagrant ssh nomadserver')

if root.send_and_get_output('vagrant plugin list | grep landrush') == '':
	root.multisend('vagrant plugin install landrush',{'assword':pw})

nomadserver_ip = root.send_and_get_output("""vagrant landrush ls 2> /dev/null | grep -w ^nomadserver.vagrant.test | awk '{print $2}'""").strip()

nomadserver.send('curl https://raw.githubusercontent.com/hashicorp/nomad/master/demo/vagrant/server.hcl > server.hcl')
nomadserver.send('sudo nomad agent -config server.hcl > server.log 2>&1 &')
nomadserver.send('nomad server-members -address http://' + nomadserver_ip + ':4646 -config server.hcl',background=True)

nomadserver.send('curl https://raw.githubusercontent.com/hashicorp/nomad/master/demo/vagrant/client1.hcl > client1.hcl')
nomadserver.send("""sed -i 's/127.0.0.1/""" + nomadserver_ip + """/' client1.hcl""")
nomadserver.send('sudo nomad agent -config client1.hcl > client.log 2>&1 &')
nomadserver.pause_point('sudo nomad agent -config client1.hcl > client1.log 2>&1 &')

nomadserver.send('curl https://raw.githubusercontent.com/hashicorp/nomad/master/demo/vagrant/client2.hc2 > client2.hcl')
nomadserver.send("""sed -i 's/127.0.0.1/""" + nomadserver_ip + """/' client2.hcl""")
nomadserver.send('sudo nomad agent -config client2.hcl > client2.log 2>&1 &')


