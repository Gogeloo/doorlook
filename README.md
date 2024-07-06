# Doorlook

Doorlook is a project designed to analyze companies and how they treat their employees. It consists of a backend built with FastAPI and a frontend built with React. The project utilizes web scraping and various AI tools to gather and analyze opinions about companies.

## Table of Contents

- [Doorlook](#doorlook)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Project Structure](#project-structure)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Running the Project](#running-the-project)
  - [Pre-commit Hooks](#pre-commit-hooks)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- Analyze companies based on various metrics.
- Evaluate employee treatment and satisfaction.
- Web scraping to gather opinions from various sources.
- AI tools for opinion analysis and sentiment detection.
- User-friendly interface for data visualization.
- RESTful API for backend services.

## Project Structure

The project scaffold could be found in [STRUCTURE](STRUCUTRE).

## Getting Started

### Prerequisites

- Python 3.12
- Node.js and npm
- Docker (optional, for containerization)

### Installation

1. **Clone the repository:**

   ```sh
   git clone https://github.com/Gogeloo/doorlook.git
   cd doorlook
   ```

2. **Backend setup:**

   Navigate to the backend directory and install dependencies using Poetry:

   ```sh
   cd backend
   poetry install
   ```

3. **Frontend setup:**

   Navigate to the frontend directory and install dependencies using npm:

   ```sh
   cd frontend
   npm install
   ```

### Running the Project

1. **Running the backend:**

   ```sh
   cd backend
   poetry run uvicorn app.main:app --reload
   ```

   The backend will be available at `http://localhost:8000`.

2. **Running the frontend:**

   ```sh
   cd frontend
   npm start
   ```

   The frontend will be available at `http://localhost:3000`.

3. **Using Docker:**

   Alternatively, you can use Docker to run both backend and frontend:

   ```sh
   docker-compose up --build
   ```

   This will start both services and make them available at their respective ports.

## Pre-commit Hooks

This project uses pre-commit hooks to ensure code quality. To install and update the hooks, run:

```sh
pre-commit install
```

## Usage

Navigate to http://localhost:3000 to access the frontend interface.
Use the available endpoints to interact with the backend API (e.g., http://localhost:8000/docs for the FastAPI documentation).

## Contributing

Contributions are welcome! Please follow these steps to contribute:

- Fork the repository.
- Create a new branch (`git checkout -b feature/your-feature`).
  - Please follow the [conventional commit messages](https://l.arvid.top/cc) format.
- Make your changes.
- Commit your changes (`git commit -am 'feat: add new feature'`).
  - Please follow the [conventional commit messages](https://l.arvid.top/cc) format.
- Push to the branch (`git push origin feature/your-feature`).
- Create a new Pull Request.

Please read the [CONTRIBUTING](CONTRIBUTING) for more details.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
