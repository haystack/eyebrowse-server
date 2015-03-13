eyebrowse-server
===========

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

The project [eyebrowse-server](https://github.com/haystack/eyebrowse-server)
aims to build a server that can receive the data from users' installs of
eyebrowse.

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

The `make install` command has two arguments for setting up the envirnoment
```bash
make install debug=[true|false] env=[prod|dev]
```
The default options are `debug=true` and `env=dev`.

Common problems:

1. `DoesNotExist at /admin/ Site matching query does not exist.`
  
For dev:
  ```python
   from django.contrib.sites.models import Site
   Site.objects.create(name='localhost:8000', domain='http://localhost:8000')
  ```
  [Reference](http://stackoverflow.com/questions/11476210/getting-site-matching-query-does-not-exist-error-after-creating-django-admin)
=======
[![Join the chat at https://gitter.im/haystack/eyebrowse-server](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/haystack/eyebrowse-server?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

Eyebrowse allows users to automatically track and selectively publish their use of the Web in real-time. Currently, there is no simple way for the end-user to keep track of the vast time spent browsing the Web. Since there is no clear picture of how users access the Web as a whole, the Eyebrowse Project aims to allow public logging of Web usage through client-side services. Eyebrowse gives control to the user, while providing data for public use.

The concept of Eyebrowse is to gather browsing history from participating users. Depending on the particular distribution, it may either be used in a context where the data goes into a public repository, or it may be used in a context where the data is shared in a controlled way (such as among a group of users, but not publicly). 

The project [eyebrowse-server](https://github.com/haystack/eyebrowse-server) aims to build a server that can receive the data from users' installs of eyebrowse.

## Contact Info

+ [@eyebrowse_proj](https://twitter.com/eyebrowse_proj)
+ [eyebrowse@csail.mit.edu](mailto:eyebrowse@csail.mit.edu)
+ [Haystack Group Homepage](http://haystack.csail.mit.edu/)


## Authors

**Amy Zhang**
+ [axz@mit.edu](mailto:axz@mit.edu)
+ [@amyxzh](https://twitter.com/amyxzh)

**Josh Blum**
+ [joshblum@mit.edu](mailto:joshblum@mit.edu)
+ [@blumua](https://twitter.com/blumua)


**Scott Greenwald**
+ [swgreen@mit.edu](mailto:swgreen@mit.edu)
+ [@swgreen_mit](https://twitter.com/swgreen_mit)

**Jason Hu**
+ [mjhu@mit.edu](mailto:mjhu@mit.edu)


Copyright (c) 2015

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
