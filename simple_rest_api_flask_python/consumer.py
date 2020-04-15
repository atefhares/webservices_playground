import requests

BASE_URL = "http://localhost:5000/"


def show_books():
    r = requests.get(BASE_URL + "books")
    print("response.TXT: ", r.text)


def create_book(params):
    r = requests.post(BASE_URL + "books", data=params)
    print("response.TXT: ", r.text)


def update_book(id, params):
    r = requests.put(BASE_URL + "books/" + str(id), data=params)
    print("response.TXT: ", r.text)


def delete_book(id):
    r = requests.delete(BASE_URL + "books/" + str(id))
    print("response.TXT: ", r.text)


print("=" * 30)
print("creating books:\n")
create_book({"t": "book1", "a": "Atef", "c": "science"})
create_book({"t": "book2", "a": "Atef", "c": "science"})
create_book({"t": "book3", "a": "Atef", "c": "science"})
create_book({"t": "book4", "a": "Atef", "c": "science"})
create_book({"t": "book5", "a": "Atef", "c": "science"})

print("=" * 30)
print("All books:\n")
show_books()

print("=" * 30)
print("updating book with id 3:\n")
update_book(3, {"t": "book103", "a": "NoName", "c": "SCIENCE"})

print("=" * 30)
print("deleting book with id 5:\n")
delete_book(5)

print("=" * 30)
print("All books:\n")
show_books()
