### Server issues: intermittent expired certificates

The GIN server experienced intermittent expired certificates. When loading the GIN page, in 4 out of 10 instances an expired certificate would be served, while in the other cases a valid certificate was used.

Running curl on "gin.g-node.org" and "web.gin.g-node.org" showed intermittent (~ 4 out of 10) certificate issues for both:

    curl -H 'Cache-Control:no-cache' -I https://gin.g-node.org

    curl: (60) SSL certificate problem: certificate has expired
    More details here: https://curl.haxx.se/docs/sslcerts.html
    
    curl failed to verify the legitimacy of the server and therefore could not
    establish a secure connection to it. To learn more about this situation and
    how to fix it, please visit the web page mentioned above.


    curl -I https://web.gin.g-node.org

    curl: (60) SSL certificate problem: certificate has expired
    More details here: https://curl.haxx.se/docs/sslcerts.html
    
    curl failed to verify the legitimacy of the server and therefore could not
    establish a secure connection to it. To learn more about this situation and
    how to fix it, please visit the web page mentioned above.

Since "web.gin.g-node.org" is a forward to gin.g-node.org and successfully curling it retrieved only the "forward" header and not the gin page header, the issue was most likely to lie with the apache and not with the "downstream" haproxy or the gin server itself. 

Another very useful tool was the Qualis SSL lab page, checking the certificate via the page [https://www.ssllabs.com/ssltest/index.html](https://www.ssllabs.com/ssltest/index.html). It immediately showed, that two certificates were being served, one of them expired.


The letsentcrypt certificates in `/etc/letsencrypt/archive` showed, that all certificates had been correctly renewed every 3 months and that the live certificates in `/etc/letsencrypt/live` were pointing to the newest certificate that was intermittently being served as the valid certificate.

In the past, manually creating a new certificate via `certbot` had shown, that it spools up an apache against which the new certificate is being tested. When the process was done, this apache was not always shut down properly and `systemctl stop apache2.service` had to be run twice until all apache instances had been shut off.
This lead to the suspicion, that the automated certificate renewal could have left an apache running that was still serving the expired certificate while the "proper" apache was serving the renewed certificate.

Investigating the apache processes showed the following

- output of `systemctl status apache2.service`:

         apache2.service - The Apache HTTP Server
           Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset: e
           Active: active (running) since Thu 2022-01-06 06:11:20 CET; 2 months 21 days a
             Docs: https://httpd.apache.org/docs/2.4/
          Process: 392822 ExecReload=/usr/sbin/apachectl graceful (code=exited, status=0/
         Main PID: 1148000 (apache2)
            Tasks: 82 (limit: 309169)
           Memory: 100.6M
           CGroup: /system.slice/apache2.service
                   ├─ 392833 /usr/sbin/apache2 -k start
                   ├─ 392872 /usr/sbin/apache2 -k start
                   ├─ 916937 /usr/sbin/apache2 -k start
                   └─1148000 /usr/sbin/apache2 -k start

- `htop` showed, that there was one main process (1148000) with three subprocesses 
    - the process 1148000 was owned by `root`
    - the sub-processes 916937, 392833, 392872 where owned by `www-data`

- restarting the service (`systemctl restart apache2.service`)
- output of `systemctl status apache2.service`:

        apache2.service - The Apache HTTP Server
           Loaded: loaded (/lib/systemd/system/apache2.service; enabled; vendor preset: e
           Active: active (running) since Tue 2022-03-29 14:16:30 CEST; 9s ago
             Docs: https://httpd.apache.org/docs/2.4/
          Process: 852265 ExecStart=/usr/sbin/apachectl start (code=exited, status=0/SUCC
         Main PID: 852277 (apache2)
            Tasks: 55 (limit: 309169)
           Memory: 25.9M
           CGroup: /system.slice/apache2.service
                   ├─852277 /usr/sbin/apache2 -k start
                   ├─852278 /usr/sbin/apache2 -k start
                   └─852279 /usr/sbin/apache2 -k start

- `htop` showed, that there was one main process (852277) with two subprocesses
    - the process 852277 was owned by `root`
    - the sub-processes 852278, 852279 were owned by `www-data`

- restarting the service did solve the issue, the expired certificate was no longer served.


## Checking certificate expiration dates

There are a couple of ways how to check certificate expiration dates

- directly on the server
  ```bash
  sudo openssl x509 -dates -noout -in /path/to/certificate/cert.pem
  ```

- using curl
  ```bash
  curl -vI [domain]
  ```

- using an off-site service like [https://www.ssllabs.com/ssltest/index.html](https://www.ssllabs.com/ssltest/index.html)
