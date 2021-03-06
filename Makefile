USR=http
GRP=http


install:
	install -v -m 755 -g $(GRP) -o $(USR) -d $(DESTDIR)/var/www/lide/backend
	cp -rv lide $(DESTDIR)/var/www/lide/backend
	cp -rv contact $(DESTDIR)/var/www/lide/backend
	cp -rv lide_api $(DESTDIR)/var/www/lide/backend
	cp -rv offers $(DESTDIR)/var/www/lide/backend
	cp -rv pages $(DESTDIR)/var/www/lide/backend
	cp -rv posts $(DESTDIR)/var/www/lide/backend
	cp -rv settings $(DESTDIR)/var/www/lide/backend
	install -v -m 755 -g $(GRP) -o $(USR) manage.py /var/www/lide/backend/manage.py
	install -v -m 755 -g $(GRP) -o $(USR) requirements.txt /var/www/lide/backend/requirements.txt
	install -v -m 655 lide.service -D $(DESTDIR)/usr/lib/systemd/system/lide.service
	install -v -m 655 lide.socket -D $(DESTDIR)/usr/lib/systemd/system/lide.socket


uninstall:
	rm -rf $(DESTDIR)/var/www/lide/backend