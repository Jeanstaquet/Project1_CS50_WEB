import os, csv

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

# Database engine object from SQLAlchemy that manages connections to the database
# set DATABASE_URL in terminal "export DATABASE_URL={Your Heroku URI}"
engine = create_engine(os.getenv("DATABASE_URL"))

# create a 'scoped session' that ensures different users' interactions
# with the database are kept separate
db = scoped_session(sessionmaker(bind=engine))

# Read and write data from books.csv to the books table on Heroku database
def main():
    db.execute("CREATE TABLE books ( \
        isbn VARCHAR PRIMARY KEY, \
        title VARCHAR NOT NULL, \
        author VARCHAR NOT NULL, \
        year INTEGER NOT NULL)")
    with open("books.csv") as file:
        reader = csv.reader(file, delimiter=',')
        next(reader, None)
        for isbn, title, author, year in reader:
            db.execute("INSERT INTO books (isbn, title, author, year) \
                VALUES (:isbn, :title, :author, :year)",\
                {"isbn": isbn, "title": title, "author": author, "year": year})
            print(f"Added book {isbn} titled {title} by {author} from {year} into the database.")

        db.commit()

if __name__ == "__main__":
    main()
