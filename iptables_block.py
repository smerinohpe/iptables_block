import os
import time

while True:
  ip_to_block = list()
  ipset_black_list = list()
  white_list = list()
  white= open('whitelist.txt', 'r')
  for line in white:
   white_list.append((line).strip())
  print(white_list)

  os.system('sudo ipset list blacklist > blacklist.log')
  black_file = open('blacklist.log', 'r')
  n = 8
  p = 1

  for line in black_file:
    if p <= n:
      p = p+1
    else:
     ipset_black_list.append((line).strip())

  os.system('journalctl | grep error | grep authentication > iptable_to_block.log')
  journal_file = open('iptable_to_block.log', 'r')

  for line in journal_file:
    file_ip= line.split('from')
    if ((file_ip[1]).split('port')[0]).strip() not in ip_to_block and ((file_ip[1]).split('port')[0]).strip() not in ipset_black_list:
      ip_to_block.append(((file_ip[1]).split('port')[0]).strip())
      for x in white_list:
        if x in ip_to_block:
          ip_to_block.remove(x)
    else:
      None

  if not ip_to_block:
    print('All ok!!')
  else:
    s= ('New ips bloqued %s' %(ip_to_block))
    print(s)

  for ip in ip_to_block:
    command = ('sudo ipset add blacklist %s' % (ip))
    os.system(command)

  time.sleep(120)
