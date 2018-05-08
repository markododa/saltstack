#!/bin/bash
#

DOMAIN=`salt 'va-directory' va_directory.get_cur_domain | tail -n 1 | sed -e 's/ //g'`

# echo user@$DOMAIN
# echo 'va-directory' va_directory.add_group Marketing '{"description":"Marketing department", "email":"'user@$DOMAIN'"}'

salt 'va-directory' va_directory.add_user ursula.wilmer xP74d.qEEwx5^KA Ursula Wilmer '' None False 
salt 'va-directory' va_directory.add_user tiffany.odell 8PE75dqEx5^KA Tiffany Odell '' None False 
salt 'va-directory' va_directory.add_user nika.gisela 8PE7dq6E.x5^KA Nika Gisela '' None False 
salt 'va-directory' va_directory.add_user diana.evgeniy 8PE77dwEEx5^KA Diana Evgeniy '' None False '{"description":"Marketing manager", "email":"'diana@$DOMAIN'"}'
salt 'va-directory' va_directory.add_user terra.urs fE7dqE8x5^KA Terra Urs '' None False 
salt 'va-directory' va_directory.add_user marciano.bonolo 8PwuE.dqEEx5^KA Marciano Bonolo '' None False 
salt 'va-directory' va_directory.add_user whitney.hollie 8PE7dgqEx5^KA Whitney Hollie '' None False 
salt 'va-directory' va_directory.add_user ramona.augustin gPEf7.dqEEx5^KA Ramona Augustin '' None False '{"description":"Logistics Manager", "email":"'ramona@$DOMAIN'"}'
salt 'va-directory' va_directory.add_user laura.lorenz 8E7dqEEvx5^A Laura Lorenz '' None False '{"description":"Database specialist", "email":"'laura@$DOMAIN'"}'
salt 'va-directory' va_directory.add_user alfreda.kara 8PE7dqdwEEx5^A Alfreda Kara '' None False '{"description":"Sales manager", "email":"'alfreda@$DOMAIN'"}'
salt 'va-directory' va_directory.add_user serafim.lavina 8PE7gd.qEE5^KA Serafim Lavina '' None False 
salt 'va-directory' va_directory.add_user diana.wilmer 8PE7dqE.Ebx5^K Diana Wilmer '' None False 
salt 'va-directory' va_directory.add_user stewart.souchon 8PE7d.qxEx5^KA Stewart Souchon '' None False '{"description":"CEO", "email":"'stewart@$DOMAIN'"}'
salt 'va-directory' va_directory.add_user johnny.ramos w8PE7dqEawx5^KA Johnny Ramos '' None False 
salt 'va-directory' va_directory.add_user nelson.freitas 8P7dq.qEEx5^KA Nelson Freitas '' None False '{"description":"Finance manager", "email":"'nelson.freitas@$DOMAIN'"}'
salt 'va-directory' va_directory.add_user philippe.monteiro PE7d1.qEEx5^KA Philippe Monteiro '' None False '{"description":"Head of IT", "email":"'philippe.monteiro@$DOMAIN'"}'
salt 'va-directory' va_directory.add_user sharon.van.etten 21.qEEx5^KA Sharon 'Van Etten' '' None False '{"description":"HR Responsible", "email":"'hr@$DOMAIN'"}'
salt 'va-directory' va_directory.add_user eva.gainsbourg 22221.qEEx5KA Eva Gainsbourg '' None False '{"description":"Secretary", "email":"'info@$DOMAIN'"}'

salt 'va-directory' va_directory.add_group 'Marketing' '{"description":"Marketing department", "mail":"'marketing@$DOMAIN'"}'
salt 'va-directory' va_directory.add_group 'Sales' '{"description":"Sales department", "mail":"'sales@$DOMAIN'"}'
salt 'va-directory' va_directory.add_group 'Management' '{"description":"Managers", "mail":"'management@$DOMAIN'"}'
salt 'va-directory' va_directory.add_group 'IT Support' '{"description":"IT department", "mail":"'it@$DOMAIN'"}'
salt 'va-directory' va_directory.add_group 'Logistics' '{"description":"Logistics department", "mail":"'logistics@$DOMAIN'"}'
salt 'va-directory' va_directory.add_group 'Finance' '{"description":"Finance department", "mail":"'finance@$DOMAIN'"}'

salt 'va-directory' va_directory.add_group 'VPN Users' '{"description":"VPN Access from home"}'
salt 'va-directory' va_directory.add_group 'DB Access' '{"description":"Access to finance data base"}'



salt 'va-directory' va_directory.add_user_to_group ursula.wilmer 'Marketing'
salt 'va-directory' va_directory.add_user_to_group tiffany.odell 'Marketing'
salt 'va-directory' va_directory.add_user_to_group nika.gisela 'Marketing'
salt 'va-directory' va_directory.add_user_to_group diana.evgeniy 'Marketing'
salt 'va-directory' va_directory.add_user_to_group diana.evgeniy 'Management'

salt 'va-directory' va_directory.add_user_to_group johnny.ramos 'Sales'
salt 'va-directory' va_directory.add_user_to_group alfreda.kara 'Sales'
salt 'va-directory' va_directory.add_user_to_group alfreda.kara 'Management'

salt 'va-directory' va_directory.add_user_to_group whitney.hollie 'Finance'
salt 'va-directory' va_directory.add_user_to_group diana.wilmer 'Finance'
salt 'va-directory' va_directory.add_user_to_group nelson.freitas 'Management'

salt 'va-directory' va_directory.add_user_to_group philippe.monteiro 'Management' 
salt 'va-directory' va_directory.add_user_to_group philippe.monteiro 'IT Support'
salt 'va-directory' va_directory.add_user_to_group serafim.lavina 'IT Support'
salt 'va-directory' va_directory.add_user_to_group laura.lorenz 'IT Support'


salt 'va-directory' va_directory.add_user_to_group terra.urs 'Logistics'
salt 'va-directory' va_directory.add_user_to_group marciano.bonolo 'Logistics'
salt 'va-directory' va_directory.add_user_to_group ramona.augustin 'Logistics'
salt 'va-directory' va_directory.add_user_to_group ramona.augustin 'Management'

salt 'va-directory' va_directory.add_user_to_group stewart.souchon 'Management'


salt 'va-directory' va_directory.create_organizational_unit 'Office users' 'Employees working in the office'
salt 'va-directory' va_directory.create_organizational_unit 'Remote users' 'Part-time and remote users'
salt 'va-directory' va_directory.create_organizational_unit 'Cloud servers' 'Special OU for policies'


salt 'va-directory' va_directory.action_add_dns A web-proxy 192.168.11.5
salt 'va-directory' va_directory.action_add_dns A website 192.168.11.15
salt 'va-directory' va_directory.action_add_dns A mailer21 192.168.11.21
salt 'va-directory' va_directory.action_add_dns A sales_portal 192.168.11.122
salt 'va-directory' va_directory.action_add_dns AAAA sales_portal_v6 '2001:0db8:85a3:0000:0000:8a2e:0370:7332'
salt 'va-directory' va_directory.action_add_dns MX mail21 'mailer21 20'
salt 'va-directory' va_directory.action_add_dns entry_type='CNAME' entry_name='email' entry_data='mail21'
salt 'va-directory' va_directory.action_add_dns entry_type='CNAME' entry_name='mail' entry_data='mail21'
salt 'va-directory' va_directory.action_add_dns entry_type='CNAME' entry_name='webmail' entry_data='mail21'

