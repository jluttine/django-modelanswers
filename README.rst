Django site - Model answers
===========================

Model answer wiki for exercise problems.

See the documentation in ``doc/`` folder or at
http://django-modelanswers.readthedocs.org/.

Deploying
---------

For development, you can use ``runserver``.

For deploying, you should have Apache and ``mod_wsgi`` installed. On
Ubuntu::

   sudo aptitude install apache2 libapache2-mod-wsgi

In ``/etc/apache2/httpd.conf``, add, for instance::

   Alias /media/ /path/to/django-modelanswers/modelanswers/media/
   Alias /static/ /path/to/django-modelanswers/modelanswers/sitestatic/

   <Directory /path/to/django-modelanswers/modelanswers/sitestatic>
   Order deny,allow
   Allow from all
   </Directory>

   <Directory /path/to/django-modelanswers/modelanswers/media>
   Order deny,allow
   Allow from all
   </Directory>

   WSGIScriptAlias / /path/to/django-modelanswers/modelanswers/wsgi.py
   WSGIPythonPath /path/to/django-modelanswers

   <Directory /path/to/django-modelanswers/modelanswers>
   <Files wsgi.py>
   Order allow,deny
   Allow from all
   </Files>
   </Directory>


Check that your ``django-modelanswers`` folder, sub-folders and all
parent folders have read-access for Apache.  Also, Apache must have
write-access to the database.  If using Sqlite3, also the parent
directory of the database must be writeable, therefore::

   chgrp www-data modelanswers/modelanswers.sqlite
   chmod g+w modelanswers/modelanswers.sqlite
   chgrp www-data modelanswers


License and copyright
---------------------

The application in ``diff_match_patch`` is licensed under Apache
License 2.0.

For everything else applies the copyright and AGPLv3 license
conditions as described below.

Copyright (C) 2011,2012 Jaakko Luttinen jaakko.luttinen@iki.fi

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public
License along with this program.  If not, see
<http://www.gnu.org/licenses/>.

