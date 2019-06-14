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


* modify the default apache2 ssl configuration (/etc/apache2/sites-available/default-ssl.conf) to include the following block (based on https://webanno.github.io/webanno/releases/3.4.7/docs/admin-guide.html#_running_the_standalone_behind_httpd):


                ProxyPreserveHost On
                ProxyPass / ajp://localhost:18009/ timeout=1200
                ProxyPassReverse / http://localhost/

* enable the default ssl site:

                sudo a2ensite default-ssl

* modify the /srv/webanno/settings.properties file (based on https://webanno.github.io/webanno/releases/3.4.7/docs/admin-guide.html#_running_the_standalone_behind_httpd) to include the following lines:

               tomcat.ajp.port=18009
               server.use-forward-headers=true

* Modify the instance security groups to include ingress https (a new security group was created).

* make webanno into a service (based on https://webanno.github.io/webanno/releases/3.4.7/docs/admin-guide.html#_installing_webanno_as_a_service). From now on, you should be able to start/stop it using:

               sudo systemctl start|stop webanno

Log can be found at /var/log/webanno.log


After the above modifications you should be able to access the site directly (via the VPN) using the VM's IP (you will get a warning about self signed certificate, which is expected), or via https://annotate.rosalind.kcl.ac.uk.

Note that webanno takes a while to start serving content after it is started. Possibly this is a  tomcat related problem.

