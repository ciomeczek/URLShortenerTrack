# Starting server
```
python -m flask run
```

# Installing requirements
```
pip install -r requirements.txt
```

# Example .env
```
FLASK_ENV=build
FLASK_APP=server
SECRET_KEY=secret
```

# Setting up database
```
touch db.sqlite3;

sqlite3 db.sqlite3 "
    CREATE TABLE url (
        url_id INTEGER PRIMARY KEY,
        url TEXT NOT NULL,
        shortened_url TEXT NOT NULL,
        tracker_url TEXT NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE visit (
        visit_id INTEGER PRIMARY KEY,
        url_id INTEGER NOT NULL,
        ip VARCHAR(15) NOT NULL,
        user_agent VARCHAR(255) NOT NULL,
        created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (url_id)  REFERENCES url (url_id) ON DELETE CASCADE
    );
";
```
