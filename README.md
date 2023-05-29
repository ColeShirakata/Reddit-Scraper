# Reddit Parser Flask App

This Flask app is designed to parse Reddit using PyLucene. It provides a web interface for searching and retrieving Reddit data.

## Prerequisites

Before running the app, ensure you have the following installed:

- Python 3.x
- Flask
- PyLucene
- Docker

## Installation

1. Clone the repository:


2. Change into the project directory:


3. Install the required dependencies using pip:


4. Set the environment variable for the Flask app:

- On Windows (Command Prompt):

  ```
  set FLASK_APP=main.py
  ```

- On macOS/Linux:

  ```
  export FLASK_APP=main.py
  ```
  
5. Pull the Docker image:

  ```
  docker pull coady/pylucene
  ```

## Usage

1. Run the pylucene file using Docker:

```
docker run -it --rm -v $(pwd):/app coady/pylucene python /app/search/search.py
```

2. Start the Flask development server:


The app will be accessible at http://localhost:5000.

3. Open your web browser and navigate to the provided URL.

4. Use the web interface to search and retrieve Reddit data.

## Contributing

Contributions are welcome! If you find any issues or want to add new features, please feel free to submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
