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

