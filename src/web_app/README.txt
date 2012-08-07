HTTPSpy web_app
---------------

Pasos para instalar:

$sudo cpan cpan App::cpanminus
$sudo cpanm DBI
$sudo cpanm DBD::SQLite
$sudo cpanm YAML::Tiny
$sudo cpanm Mojolicious

Para correr:

$morbo informes

Nota:
	Por defecto levanta la base de datos log.db que esta en el directorio de la
	web_app. Para cambiar la base utilizar la variable de entorno INFORMES_DB.
    Los informes definidos son para utilizar con la base generada por el plugin SQLiteStatic.
