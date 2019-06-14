Notes from Lukasz:

Assuming

 - WebAnno 3.5.7 "Tomcat embedded" JAR installed on a Rosalind VM, as per instructions.
 - Rosalind proxying configured to expose the WebAnno front end to an external address (annotate.rosalind.kcl.ac.uk in this case)

Take a VM snapshot before the work below begins.

Below are the steps that were carried out on the WebAnno vm.

* Install apache2, enable the service and relevant modules (mod_proxy, mod_proxy_ajp and ssl)
sudo apt-get install apache2
sudo a2enmod proxy_ajp
sudo a2enmod proxy
sudo a2enmod ssl
sudo systemctl enable apache2


* modify the default apache2 ssl configuration (/etc/apache2/sites-available/default-ssl.conf) to include the following block (based on https://eur03.safelinks.protection.outlook.com/?url=https%3A%2F%2Fwebanno.github.io%2Fwebanno%2Freleases%2F3.4.7%2Fdocs%2Fadmin-guide.html%23_running_the_standalone_behind_httpd&amp;data=01%7C01%7Cangus.roberts%40kcl.ac.uk%7C84424f43954b4eb9b59308d6efe9d053%7C8370cf1416f34c16b83c724071654356%7C0&amp;sdata=u3en0ml6VdAjuEI6llHhtOQtWf%2BsPHKMQcB4DmNFirM%3D&amp;reserved=0):
ProxyPreserveHost On

                ProxyPass / ajp://localhost:18009/ timeout=1200
                ProxyPassReverse / http://localhost/

* enable the default ssl site:
sudo a2ensite default-ssl

* modify the /srv/webanno/settings.properties file (based on https://eur03.safelinks.protection.outlook.com/?url=https%3A%2F%2Fwebanno.github.io%2Fwebanno%2Freleases%2F3.4.7%2Fdocs%2Fadmin-guide.html%23_running_the_standalone_behind_httpd&amp;data=01%7C01%7Cangus.roberts%40kcl.ac.uk%7C84424f43954b4eb9b59308d6efe9d053%7C8370cf1416f34c16b83c724071654356%7C0&amp;sdata=u3en0ml6VdAjuEI6llHhtOQtWf%2BsPHKMQcB4DmNFirM%3D&amp;reserved=0) to include the following lines:

tomcat.ajp.port=18009
server.use-forward-headers=true

* Modify the instance security groups to include ingress https (a new security group was created).

* make webanno into a service (based on https://eur03.safelinks.protection.outlook.com/?url=https%3A%2F%2Fwebanno.github.io%2Fwebanno%2Freleases%2F3.4.7%2Fdocs%2Fadmin-guide.html%23_installing_webanno_as_a_service&amp;data=01%7C01%7Cangus.roberts%40kcl.ac.uk%7C84424f43954b4eb9b59308d6efe9d053%7C8370cf1416f34c16b83c724071654356%7C0&amp;sdata=nDmKnb38awvb1HqM1qYHD%2FwvOUgnHJCejWZJahobq7Y%3D&amp;reserved=0).
From now on, you should be able to start/stop it using:
sudo systemctl start|stop webanno
Log can be found at /var/log/webanno.log


After the above modifications you should be able to access the site directly (via the VPN) using https://eur03.safelinks.protection.outlook.com/?url=https%3A%2F%2F10.200.106.231%2F&amp;data=01%7C01%7Cangus.roberts%40kcl.ac.uk%7C84424f43954b4eb9b59308d6efe9d053%7C8370cf1416f34c16b83c724071654356%7C0&amp;sdata=5KvPqjCAxCePXHdaoE%2FbitAMTxks23l0nVTM1GbzsAk%3D&amp;reserved=0 (you will get a warning about self signed certificate, which is expected),
or via https://eur03.safelinks.protection.outlook.com/?url=https%3A%2F%2Fannotate.rosalind.kcl.ac.uk&amp;data=01%7C01%7Cangus.roberts%40kcl.ac.uk%7C84424f43954b4eb9b59308d6efe9d053%7C8370cf1416f34c16b83c724071654356%7C0&amp;sdata=CLBzUy%2FGsOGqOefrp%2Bcz2KyggCux76scri%2B%2FCsgvW20%3D&amp;reserved=0.

Note that webanno takes a while to start serving content after it is started. Possibly this is a  tomcat related problem.

