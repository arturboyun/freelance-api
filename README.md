# Freelance Platform API

This is the API for the Freelance Platform project. It is responsible for managing and providing data to the front-end application.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them.

-   Python 3.11^
-   Poetry 1.8^
-   Docker (optional)

### Installation

1. Clone the repository
    ```
    git clone https://github.com/yourusername/freelance-platform.git
    ```
2. Navigate into the project directory
    ```
    cd freelance-api
    ```
3. Install the dependencies
    ```
    poetry install
    ```
4. Enter to shell
    ```
    poetry shell
    ```
5. Start project with uvicorn
    ```
    uvicorn app.main:app --reload
    ```
6. Open your browser and go to `http://localhost:8000/docs` to see the Swagger API documentation.

### Running the project

#### Locally

1. Start the server
    ```
    npm start
    ```

#### Using Docker

1. Build the Docker image
    ```
    docker compose up --build
    ```
2. Run the Docker container
    ```
    docker run -p 8000:8000 freelance-platform
    ```

Now, you can access the API at `http://localhost:8000`.
