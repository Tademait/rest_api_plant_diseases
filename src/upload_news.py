import database

if __name__ == "__main__":
    db = database.Database()
    print("Upload news to the database")
    title = input("News title: ")
    body = input("News body: ")
    res = db.add_news(title=title, body=body)
    if res:
        print("News uploaded successfully")
    else:
        print("News upload failed")