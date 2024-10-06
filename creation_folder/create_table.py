from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from bson import ObjectId
import random
import string

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['library_management']

# Define collections
collections = ['Users', 'Racks', 'Books', 'Requests', 'Issues', 'Reservations', 'Fines', 'BookRack']

# Drop collections if they exist (optional, for a clean slate)
for collection in collections:
    db.drop_collection(collection)

# Generate a random ID of specified length
def generate_random_id(length=8):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

# Create a BookID based on format: ED_RACK_SHELF
def create_book_id(edition, rack_id, shelf_column):
    return f'{edition:02d}_{rack_id:02d}_{shelf_column:02d}'

# Create collections and insert dummy data
def create_and_insert_data():
    # Users Collection
    users = db['Users']
    user_ids = [str(ObjectId()), str(ObjectId())]  # Generate two user IDs
    users.insert_many([
        {
            '_id': user_ids[0],  # Use generated ObjectId
            'Name': 'John Doe',
            'Email': 'john.doe@example.com',
            'Phone': '1234567890',
            'MembershipType': 'Student',
            'JoinDate': '2024-09-13',
            'username': 'johndoe',
            'password': generate_password_hash('password123')  # Hashed password
        },
        {
            '_id': user_ids[1],  # Use generated ObjectId
            'Name': 'Jane Smith',
            'Email': 'jane.smith@example.com',
            'Phone': '0987654321',
            'MembershipType': 'Faculty',
            'JoinDate': '2024-09-14',
            'username': 'janesmith',
            'password': generate_password_hash('password456')
        }
    ])

    # Racks Collection
    racks = db['Racks']
    rack_ids = ['01', '02']  # Custom Rack IDs with two digits
    racks_data = [
        {
            '_id': rack_ids[0],
            'LocationDescription': 'Aisle 1, Shelf 1',
            'FloorNumber': 1,
            'Section': 'Science'
        },
        {
            '_id': rack_ids[1],
            'LocationDescription': 'Aisle 2, Shelf 3',
            'FloorNumber': 2,
            'Section': 'Arts'
        }
    ]
    racks.insert_many(racks_data)

    # Books Collection
    books = db['Books']
    books_data = [
        {
            'Title': 'Introduction to Algorithms',
            'Author': 'Thomas H. Cormen',
            'ISBN': '9780262033848',
            'Publisher': 'MIT Press',
            'Year': 2021,
            'Genre': 'Education',
            'Type': 'Physical',
            'CopiesAvailable': 5,
            'FilePath': '',
            'Summary': 'An introduction to algorithms for computer science students.',
            'RackID': rack_ids[0],  # Use a predefined RackID
            'BookID': create_book_id(1, 1, 1)  # Edition 1, Rack 01, Shelf 01
        },
        {
            'Title': 'The Art of Computer Programming',
            'Author': 'Donald E. Knuth',
            'ISBN': '9780321751041',
            'Publisher': 'Addison-Wesley',
            'Year': 2011,
            'Genre': 'Education',
            'Type': 'eBook',
            'CopiesAvailable': 0,
            'FilePath': '/path/to/ebook.pdf',
            'Summary': 'A comprehensive overview of algorithms and programming.',
            'RackID': rack_ids[1],  # Use a predefined RackID
            'BookID': create_book_id(2, 2, 3)  # Edition 2, Rack 02, Shelf 03
        }
    ]
    books.insert_many(books_data)

    # Requests Collection
    requests = db['Requests']
    requests.insert_many([
        {
            'UserID': user_ids[0],  # Use the predefined user ID
            'BookID': books_data[0]['BookID'],  # Use the predefined book ID
            'RequestDate': '2024-09-13',
            'Status': 'Requested'
        }
    ])

    # Issues Collection
    issues = db['Issues']
    issues.insert_many([
        {
            'UserID': user_ids[0],  # Use the predefined user ID
            'BookID': books_data[0]['BookID'],  # Use the predefined book ID
            'IssueDate': '2024-09-13',
            'DueDate': '2024-10-13',
            'ReturnDate': ''
        }
    ])

    # Reservations Collection
    reservations = db['Reservations']
    reservations.insert_many([
        {
            'UserID': user_ids[1],  # Use the predefined user ID
            'BookID': books_data[1]['BookID'],  # Use the predefined book ID
            'ReservationDate': '2024-09-13',
            'Status': 'Pending'
        }
    ])

    # Fines Collection
    fines = db['Fines']
    fines.insert_many([
        {
            'UserID': user_ids[1],  # Use the predefined user ID
            'BookID': books_data[1]['BookID'],  # Use the predefined book ID
            'FineAmount': 10.00,
            'PaymentStatus': 'Unpaid'
        }
    ])

    # BookRack Collection
    bookrack = db['BookRack']
    bookrack.insert_many([
        {
            'BookID': books_data[0]['BookID'],  # Use the predefined book ID
            'RackID': racks_data[0]['_id']  # Use the predefined rack ID
        },
        {
            'BookID': books_data[1]['BookID'],  # Use the predefined book ID
            'RackID': racks_data[1]['_id']  # Use the predefined rack ID
        }
    ])

if __name__ == '__main__':
    create_and_insert_data()
    print("Collections created and data inserted successfully!")
