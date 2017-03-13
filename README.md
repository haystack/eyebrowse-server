eyebrowse-server
===========
[![Join the chat at https://gitter.im/haystack/eyebrowse-server](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/haystack/eyebrowse-server?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Eyebrowse allows users to automatically track and selectively publish their use
of the Web in real-time. Currently, there is no simple way for the end-user to
keep track of the vast time spent browsing the Web. Since there is no clear
picture of how users access the Web as a whole, the Eyebrowse Project aims to
allow public logging of Web usage through client-side services. Eyebrowse gives
control to the user, while providing data for public use.

The concept of Eyebrowse is to gather browsing history from participating
users. Depending on the particular distribution, it may either be used in a
context where the data goes into a public repository, or it may be used in a
context where the data is shared in a controlled way (such as among a group of
users, but not publicly).

## Get running in 5 minutes

First, check out the `eyebrowse-server`:

```bash
git clone git@github.com:haystack/eyebrowse-server.git
cd eyebrowse-server
```
The application requires some configuration variables for the database and a few
other django-related things. We've provided `config_template.py` for you to
add the required values, so use your favorite editor and fill that puppy out:

```vim
vim config_template.py
```
Next, you can install the python requirements and setup the config file you make.

Note: If you're setting up a dev with MYSQL, this might be helpful to get
started:

```mysql
$ sudo mysql
> CREATE USER 'admin'@'localhost' IDENTIFIED BY 'somepassword';
> CREATE DATABASE eyebrowse;
> USE eyebrowse;
> GRANT ALL PRIVILEGES ON eyebrowse.* TO 'admin'@'localhost';
```

Where the corresponding dictionary in `config_template.py` would read:
```python
MYSQL_LOCAL = {
    'NAME': 'eyebrowse',
    'USER': 'admin',
    'PASSWORD': 'somepassword',
    'HOST': 'localhost',
}
```

Note: You need to use `sudo` if you are not working in a
[virtualenv](http://docs.python-guide.org/en/latest/dev/virtualenvs/).

```bash
make install
make run
```

The `make install` command has two arguments for setting up the environment
```bash
make install debug=[true|false] env=[prod|dev]
```
The default options are `debug=true` and `env=dev`.

There are several cron tasks that eyebrowse uses. If you want to install them, run
```
python manage.py installtasks
```
Most of them are not important for development purposes. The one exception 
would be the script for updating the popular feeds which should be run to
populate them initially. Run the following at the python command line (with
your eyebrowse virtual environment enabled):
```
from scripts.cron_tasks.populate_popular_history import *
populate_popular_history()
```


### Common problems:

1. `DoesNotExist at /admin/ Site matching query does not exist.`

For dev [(stackoverflow reference)](http://stackoverflow.com/questions/11476210/getting-site-matching-query-does-not-exist-error-after-creating-django-admin):
  ```python
   from django.contrib.sites.models import Site
   Site.objects.create(name='localhost:8000', domain='http://localhost:8000')
  ```
=======

### Setting up HTTPS for your server 

To set up HTTPS, you need to configure a SSL certificate onto the Apache server.

1. Generate a key and certificate-signing request: http://tig.csail.mit.edu/wiki/TIG/HowToRequestAServerCertificate. Place the key and .csr file in a directory such as `/home/[username]`.

2. Email help@csail.mit.edu to request a certificate.

3. Upon certificate approval, download the received certificate file and place it in `/etc/ssl/certs`.

4. Place the private key in `/etc/ssl/private`, and secure its permissions using `chmod 640 [key file name]` and `chown root [key file name]`.

5. Modify Apache config files found in `/etc/apache2`
 + There are two VirtualHost config blocks, one for 443 (HTTPS) and one for 80 (HTTP)
 + In `httpd.conf`, inside the VirtualHost config for 443, set the following:
 
 ```
 <VirtualHost __default__:443>
    SSLEngine on
    SSLCertificateFile /path/to/your_domain_name.crt
    SSLCertificateKeyFile /path/to/your_private.key
 </VirtualHost>
 ```
6. Test the Apache config before restarting. Run the following command:
```
apachectl configtest
```

7. Restart Apache.
```
apachectl stop
apachectl start
```

## Contact Info

+ [@eyebrowse_proj](https://twitter.com/eyebrowse_proj)
+ [eyebrowse@csail.mit.edu](mailto:eyebrowse@csail.mit.edu)
+ [Haystack Group Homepage](http://haystack.csail.mit.edu/)
