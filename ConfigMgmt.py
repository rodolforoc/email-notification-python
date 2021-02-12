import difflib
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from netmiko import ConnectHandler

ip = '10.10.10.2'

# Tipo do dispositivo para o netmiko
device_type = 'arista_eos'

# Credenciais
username = 'admin'
password = 'python'

command = 'show running'

# Conectando via SSH
session = ConnectHandler(device_type = device_type, ip = ip, username = username, password = password, global_delay_factor = 3)

enable = session.enable()

output = session.send_command(command)

# Definindo arquivo para comparação
device_cfg_old = 'cfgfiles/' + ip + '_' + (datetime.date.today() - datetime.timedelta(days = 1)).isoformat()

# Escrevendo arquivo de hoje
with open('cfgfiles/' + ip + '_' + datetime.date.today().isoformat(), 'w') as device_cfg_new:
    device_cfg_new.write(output + '\n')

# Extraindo diferença entre os arquivos em HTML
with open(device_cfg_old, 'r') as old_file, open('cfgfiles/' + ip + '_' + datetime.date.today().isoformat(), 'r') as new_file:
    difference = difflib.HtmlDiff().make_file(fromlines = old_file.readlines(), tolines = new_file.readlines(), fromdesc = 'Yesterday', todesc = 'Today')
    
# Enviando diferenças por email
fromaddr = 'rodolforoc97@gmail.com'
toaddr = 'rodolforoc97@gmail.com'

msg = MIMEMultipart()
msg['From'] = fromaddr
msg['To'] = toaddr
msg['Subject'] = 'Daily Configuration Management Report'
msg.attach(MIMEText(difference, 'html'))

# Enviando email via Gmail's SMTP server - porta 587
server = smtplib.SMTP('smtp.gmail.com', 587)

server.starttls()

# Logando no gmail e enviando email
server.login('rodolfo.caetano', 'python')
server.sendmail(fromaddr, toaddr, msg.as_string())
server.quit()