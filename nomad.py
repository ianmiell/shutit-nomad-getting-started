import shutit

# Assumes vagrant is installed
# 'pip install shutit' to install python shutit package

root = shutit.create_session('bash',loglevel='info',echo=True)
nomadserver = shutit.create_session('bash',loglevel='info')
nomadclient1 = shutit.create_session('bash',loglevel='info')
nomadclient2 = shutit.create_session('bash',loglevel='info')

pw = root.get_input('Password?',ispass=True)
root.send('vagrant destroy -f')
root.multisend('vagrant up',{'assword':pw})

nomadserver.login('vagrant ssh nomadserver')
nomadclient1.login('vagrant ssh nomadclient1')
nomadclient2.login('vagrant ssh nomadclient2')

if root.send_and_get_output('vagrant plugin list | grep landrush') == '':
	shutit.multisend('vagrant plugin install landrush',{'assword':pw})

nomadserver_ip = root.send_and_get_output("""vagrant landrush ls 2> /dev/null | grep -w ^nomadserver.vagrant.test | awk '{print $2}'""").strip()
nomadclient1_ip = root.send_and_get_output("""vagrant landrush ls 2> /dev/null | grep -w ^nomadclient1.vagrant.test | awk '{print $2}'""").strip()
nomadclient2_ip = root.send_and_get_output("""vagrant landrush ls 2> /dev/null | grep -w ^nomadclient2.vagrant.test | awk '{print $2}'""").strip()

nomadserver.send('curl https://raw.githubusercontent.com/hashicorp/nomad/master/demo/vagrant/server.hcl > server.hcl')
nomadserver.send('sudo nomad agent nomad node-status -address http://' + nomadserver_ip + ':4646 -config server.hcl',background=True)
nomadserver.pause_point('')

nomadclient1.send('curl https://raw.githubusercontent.com/hashicorp/nomad/master/demo/vagrant/client1.hcl > client1.hcl')
nomadclient1.send("""sed -i 's/127.0.0.1/""" + nomadserver_ip + """/' client1.hcl""")
nomadclient1.send('sudo nomad agent -config client1.hcl',background=True)

nomadclient2.send('curl https://raw.githubusercontent.com/hashicorp/nomad/master/demo/vagrant/client1.hc2 > client2.hcl')
nomadclient2.send("""sed -i 's/127.0.0.1/""" + nomadserver_ip + """/' client2.hcl""")
nomadclient2.send('sudo nomad agent -config client2.hcl',background=True)

