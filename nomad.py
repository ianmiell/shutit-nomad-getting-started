import shutit

# Assumes vagrant, and vagrant landrush are installed

root = shutit.create_session('bash',loglevel='info',echo=True)
nomad_server = shutit.create_session('bash',loglevel='info')
nomad_client1 = shutit.create_session('bash',loglevel='info')
nomad_client2 = shutit.create_session('bash',loglevel='info')

pw = root.get_input('Password?',ispass=True)
root.send('vagrant destroy -f')
root.multisend('vagrant up',{'assword':pw})

nomad_server.login('vagrant ssh nomad1')
nomad_client1.login('vagrant ssh nomad2')
nomad_client2.login('vagrant ssh nomad3')

if root.send_and_get_output('vagrant plugin list | grep landrush') == '':
	shutit.multisend('vagrant plugin install landrush')

nomad_server_ip = root.send_and_get_output("""vagrant landrush ls 2> /dev/null | grep -w nomad1.vagrant.test | awk '{print $2}'""")
nomad_client1_ip = root.send_and_get_output("""vagrant landrush ls 2> /dev/null | grep -w nomad2.vagrant.test | awk '{print $2}'""")
nomad_client2_ip = root.send_and_get_output("""vagrant landrush ls 2> /dev/null | grep -w nomad3.vagrant.test | awk '{print $2}'""")


nomad_server.send('curl https://raw.githubusercontent.com/hashicorp/nomad/master/demo/vagrant/server.hcl > server.hcl')
nomad_server.send('sudo nomad agent -config server.hcl',background=True)

nomad_client1.send('curl https://raw.githubusercontent.com/hashicorp/nomad/master/demo/vagrant/client1.hcl > client1.hcl')
nomad_client1.send("""sed -i 's/127.0.0.1/""" + nomad_server_ip + """/' client1.hcl""")
nomad_client1.send('sudo nomad agent -config client1.hcl',background=True)

nomad_client2.send('curl https://raw.githubusercontent.com/hashicorp/nomad/master/demo/vagrant/client1.hc2 > client2.hcl')
nomad_client2.send("""sed -i 's/127.0.0.1/""" + nomad_server_ip + """/' client2.hcl""")
nomad_client2.send('sudo nomad agent -config client2.hcl',background=True)

