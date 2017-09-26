import shutit

root = shutit.create_session('bash',loglevel='debug')
nomad1 = shutit.create_session('bash',loglevel='debug')
nomad2 = shutit.create_session('bash',loglevel='debug')
nomad3 = shutit.create_session('bash',loglevel='debug')

nomad1.send('vagrant destroy -f')
nomad1.send('vagrant up')

nomad1.login('vagrant ssh nomad1')
nomad2.login('vagrant ssh nomad2')
nomad3.login('vagrant ssh nomad3')

if root.send_and_get_output('vagrant plugin list | grep landrush') == '':
	shutit.multisend('vagrant plugin install landrush')

nomad1_ip = root.send_and_get_output("""vagrant landrush ls 2> /dev/null | grep -w nomad1.vagrant.test | awk '{print $2}'""")
nomad2_ip = root.send_and_get_output("""vagrant landrush ls 2> /dev/null | grep -w nomad2.vagrant.test | awk '{print $2}'""")
nomad3_ip = root.send_and_get_output("""vagrant landrush ls 2> /dev/null | grep -w nomad3.vagrant.test | awk '{print $2}'""")

nomad1.pause_point('' + nomad1_ip)

nomad1.send('curl https://raw.githubusercontent.com/hashicorp/nomad/master/demo/vagrant/server.hcl > server.hcl')
nomad1.send('sudo nomad agent -config server.hcl',background=True)
nomad2.send('curl https://raw.githubusercontent.com/hashicorp/nomad/master/demo/vagrant/client1.hcl > client1.hcl')
nomad2.send('sudo nomad agent -config client1.hcl',background=True)
nomad3.send('curl https://raw.githubusercontent.com/hashicorp/nomad/master/demo/vagrant/client1.hc2 > client2.hcl')
nomad3.send('sudo nomad agent -config client2.hcl',background=True)

