EATANDRATE
Progetto Linguaggi Dinamici
AUTHORS: Simone Richetti (mat. 88664), Daniele Toschi (mat. 88607)

DESCRIZIONE:
Applicazione web dinamica creata con Django per gestire le recensioni di attività.
Features:
	- Sistema di registrazione e autenticazione utenti e proprietari attività
	- Sistema di creazione e modifica delle attività
	- Sistema di caricamento di immagini delle attività
	- Sistema di recensione delle attività e valutazione delle recensioni
	- Sistema di notifica e risposta
	- Sistema di ricerca per nome, luogo e tipologia

PREREQUISITI:
Sono necessari:
	- Python3.X
	- Connessione internet per l'importazione dei CDN Bootstrap
	- DBMS sqlite3
	- virtualenv (facoltativo ma consigliato)
	- Visual C++ 14.0 o sup. (solo per Windows, richiesto per installazione
		package wordcloud)
	
INSTALLAZIONE:
Per creare ambiente virtuale (saltare il seguente blocco di istruzioni se non lo si
vuole fare):
	$ cd my_project_folder
	$ virtualenv [-p /path/to/python3 | --python=python3] env
	(Unix)$ source env/bin/activate
	(Windows)$ env\bin\activate.bat
	
Per installare le dipendenze entrare nella directory del progetto e utilizzare:
	$ pip install -r requirements.txt

Il database fornito nel progetto contiene già entità di prova. Per crearne uno
nuovo caricando il dump fornito utilizzare:
	$ cd eatandrate/
	$ sqlite3
	>>.open db.sqlite3
	>>.read dump_db.sql
	>>.exit

UTILIZZO:
Per far partire il server, posizionarsi nella cartella eatandrate/ e utilizzare:
	$ python manage.py runserver

Aprire quindi un qualsiasi browser e digitare nella barra degli indirizzi "127.0.0.1:8000"

TEST:
Per eseguire i test, entrare nella directory eatandrate/ e digitare:
	$ python manage.py test [attivita | recensioni]

CREDENZIALI ROOT:
	USER: root
	PWD: progettold

La password di qualsiasi utente è uguale a quella di root

