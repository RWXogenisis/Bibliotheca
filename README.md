# Bibliotheca-Library Management System

This Library Management System (LMS) allows users to manage, search, and visualize books stored on shelves. The system includes a user-friendly front-end interface for interacting with the library, a backend powered by Flask for handling requests, and MongoDB for data storage. Additionally, it utilizes Blender to render a 3D visualization of the library's shelves and books.

## Required Applications

- **Python 3.x**: For running the backend.
- **Blender**: For handling 3D visualizations. [Download here](https://www.blender.org/download/).
- **MongoDB**: To store data. You will need:
  - **MongoDB server** (`mongod`) running.
  - **MongoDB shell** (`mongosh`) for database interaction.

## Installation

### 1. Setup Backend
1. **Create and activate a virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### 2. Setup MongoDB
1. Start the MongoDB server:
    ```bash
    mongod
    ```

2. Use `mongosh` to create a database called `library_db` and populate it with initial data as required.

### 3. Blender Setup
Ensure Blender is installed. Use it to run the 3D visualization script (`test3.py`).

## Running the Application

### 1. Backend: Flask API
Run the Flask backend:
```bash
python app.py
```
This will start the API server, exposing endpoints for user authentication and library management.

### 2. Running the Blender Script
To visualize the library structure:
```bash
blender --python test3.py
```
This command will open Blender and execute the `test3.py` script, generating a 3D visualization of the library shelves and books.

## Frontend Interaction
The frontend allows users to:
- **Log in** for an account.
- **Search** for books by their ID.
- **View** detailed information about selected books and their shelf locations.
- **Request** new books to be added to the library.

![image](https://github.com/user-attachments/assets/bdf244c4-5801-4869-a3a7-98150c907168)

### In case the user forgets the password
#### Points to note:
- The user should already be registered
- They should have access to the email they have registered with

  The user will get the OTP on their registered email which they can use to reset the password

  ![image](https://github.com/user-attachments/assets/df6ce778-62b9-4127-9cb0-60b99f1d358f)

### Preview of the dashboard
![image](https://github.com/user-attachments/assets/5a102e79-156b-460c-9480-d40b9cc278fb)


### Preview of book when viewed
![image](https://github.com/user-attachments/assets/f3a56840-95b1-4d78-a72f-ce31736e8d53)


## Project Structure
```
library_management_system/
├── app.py              # Flask backend application
├── requirements.txt    # Python dependencies
├── test3.py            # Blender script for visualization
├── README.md           # Project documentation
```

## Schema diagram of mongoDB
![Schema Diagram](https://github.com/user-attachments/assets/2f1b80a9-e014-4c0b-8892-d3f9ffe152e8)

## Book highlighting feature
TO use the highlighting feature, download blender and add the exe file to the environemental path and run:
```bash
blender --python test3.py
```
![image](https://github.com/user-attachments/assets/39608f34-52e1-459d-a824-bb690d75404a)

The application will show the row, the shelf and the rack where the book may be present according to the ID of the book. The current format used is:
```
"row id"_"shelf id"_"rack id"
```

## Testing and Development
- Ensure all services (Flask and MongoDB) are running correctly.

## Troubleshooting
- If the Flask backend does not start, check the console for errors and ensure all dependencies are installed.
- Make sure MongoDB is running and accessible.
- If Blender does not render correctly, ensure the script path is correctly set and Blender is properly installed.
