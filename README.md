# amavisd-new

Forked version of amavisd-new with ClearOS changes applied

* git clone git+ssh://git@github.com/clearos/amavisd-new.git
* cd amavisd-new
* git checkout epel7
* git remote add upstream git://pkgs.fedoraproject.org/amavisd-new.git
* git pull upstream epel7
* git checkout clear7
* git merge --no-commit epel7
* git commit
