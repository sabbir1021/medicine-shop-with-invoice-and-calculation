
<!-- Update ubuntu Server -->
sudo apt update
sudo apt upgrade -y


<!-- Install Required Packages in ubuntu server -->
sudo apt install nginx python3 python3-pip python3-venv -y

<!-- clone github project -->

<!-- create virtual environment inside  Django App project for run project-->
python3 -m venv venv
<!-- active virtual environment -->
source venv/bin/activate
<!-- install  Django App dependency/package -->
pip install -r requirements.txt

<!-- run Django App with Gunicorn -->
gunicorn --workers 3 --bind 0.0.0.0:8000 myproject.wsgi:application -D
pkill gunicorn 

<!-- setup nginx -->

<!-- create a os_lab.conf file -->
sudo nano /etc/nginx/sites-available/os_lab.conf
<!-- insert this code on os_lab.conf file -->
server {
    listen 80;
    server_name app.dorjimahal.com;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

<!-- nginx enable -->
sudo ln -s /etc/nginx/sites-available/os_lab.conf /etc/nginx/sites-enabled/
<!-- check nginx setup -->
sudo nginx -t
<!-- restart nginx -->
sudo systemctl restart nginx




<!-- Enable Firewall (ufw) -->
sudo apt install ufw -y
sudo ufw allow 'Nginx Full'
sudo ufw allow OpenSSH
sudo ufw enable

<!-- Enable HTTPS (SSL/TLS) -->
<!-- Install Certbot: -->
sudo apt install certbot python3-certbot-nginx -y
<!-- Issue SSL: -->
sudo certbot --nginx -d app.dorjimahal.com 


<!-- Step 10: Install fail2ban -->
sudo apt install fail2ban -y
<!-- Enable basic config: -->
sudo systemctl enable fail2ban
sudo systemctl start fail2ban












3. Check logs
journalctl -u os_lab.service -f