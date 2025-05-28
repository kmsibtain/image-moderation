# image-moderation
# Image Moderation API

## 1. Introduction
This project implements an Image Moderation API using FastAPI for the backend and React for the frontend. Its purpose is to automatically detect and block harmful, illegal, or otherwise unwanted imagery such as graphic violence, hate symbols, explicit nudity, self-harm depictions, or extremist propaganda from being served to end users. [cite: 1]

## 2. Objectives Met
* **Secure, well-structured REST API in FastAPI:** Designed with clear routing, models, and services. [cite: 2]
* **Authentication/Authorization:** Implemented using bearer tokens with admin-only access for certain endpoints. [cite: 3]
* **MongoDB Data Modeling and Usage Tracking:** Utilizes MongoDB for storing tokens and recording API usage per token. [cite: 3]
* **Docker Containerization:** Both backend and frontend are containerized using Docker, managed by `docker-compose.yml`. [cite: 4, 7]
* **Minimal Frontend UI:** A React application to interact with the API, allowing token management and image uploads. [cite: 4, 12, 13]
* **Best Practices:** Follows good project structure, includes documentation, and aims for clean code. [cite: 5, 17]

## 3. Technical Stack
* **Backend:** Python 3.9, FastAPI, Uvicorn, PyMongo, Pillow. [cite: 6]
* **Frontend:** React, HTML, CSS, JavaScript. [cite: 6]
* **Database:** MongoDB. [cite: 6]
* **Containerization:** Docker, Docker Compose. [cite: 7]

## 4. Setup Instructions

### Prerequisites
* Docker Desktop (includes Docker and Docker Compose)
* Git

### Steps

1.  **Clone the repository:**
    ```bash
    git clone <your-private-git-repo-url>
    cd image-moderation-api
    ```

2.  **Create `.env` file:**
    Copy the `.env.example` file to `.env` in the root directory. This file will contain environment variables for your application.
    ```bash
    cp .env.example .env
    ```
    The `.env` file should look like this (you can modify `MONGO_URI` if your MongoDB setup is different):
    ```
    # Backend Environment Variables
    MONGO_URI=mongodb://mongodb:27017/image_moderation
    ```

3.  **Build and Run with Docker Compose:** [cite: 15]
    From the `image-moderation-api` root directory, run:
    ```bash
    docker-compose up --build
    ```
    This command will:
    * Build the backend Docker image based on `backend/Dockerfile.backend`.
    * Build the frontend Docker image based on `frontend/Dockerfile.frontend`.
    * Start a MongoDB container.
    * Start the backend FastAPI container, connected to MongoDB.
    * Start the frontend Nginx server, serving the React application and configured to communicate with the backend.

### Accessing the Application

* **Frontend UI:** Open your web browser and navigate to `http://localhost`.
* **Backend API Documentation (Swagger UI):** Open your web browser and navigate to `http://localhost:7000/docs`.

## 5. API Endpoints

### 5.1 Authentication Endpoints (Admin-Only) [cite: 9]

* **`POST /auth/tokens`**
    * **Description:** Creates a new bearer token.
    * **Requires:** Admin token in `Authorization: Bearer <token>` header.
    * **Query Parameter:** `is_admin` (boolean, default: `false`) - set to `true` to generate an admin token.
    * **Response:** JSON object containing the new token, `is_admin` status, and `created_at` timestamp.

* **`GET /auth/tokens`**
    * **Description:** Retrieves a list of all issued bearer tokens.
    * **Requires:** Admin token in `Authorization: Bearer <token>` header.
    * **Response:** JSON array of token objects.

* **`DELETE /auth/tokens/{token}`**
    * **Description:** Deletes a specific bearer token.
    * **Requires:** Admin token in `Authorization: Bearer <token>` header.
    * **Path Parameter:** `{token}` - the string value of the token to delete.
    * **Response:** 204 No Content on success.

### 5.2 Moderation Endpoint

* **`POST /moderate`**
    * **Description:** Analyzes an uploaded image and returns a content-safety report. [cite: 9]
    * **Authentication:** Any valid bearer token in `Authorization: Bearer <token>` header. [cite: 10]
    * **Request Body:** `multipart/form-data` with a `file` field containing the image.
    * **Response:** JSON object containing filename, content type, and a `moderation_report` with categories (e.g., violence, nudity) and their detection status/confidence.

## 6. Git Workflow [cite: 8, 16]
This project follows a GitHub Flow-like workflow:
1.  **`main` branch:** This branch is considered production-ready and stable.
2.  **Feature Branches:** For every new feature or bug fix, a new branch is created from `main` (e.g., `feature/implement-auth`, `fix/cors-issue`).
3.  **Commits:** Changes are committed frequently and with meaningful commit messages on feature branches.
4.  **Pull Requests (PRs):** Once a feature is complete and tested, a Pull Request is opened to merge the feature branch back into `main`.
5.  **Code Review & CI Hooks:** PRs are reviewed by peers. CI hooks (e.g., linting with `flake8` for Python, `ESLint` for JavaScript; type-checking with `mypy` for Python) are integrated into the CI/CD pipeline (though not explicitly implemented in this repo's CI config, the intention is to use them).

## 7. Future Improvements
* Implement a more robust token management system (e.g., JWTs with proper expiration and refresh tokens).
* Integrate with a real third-party image moderation API (e.g., Google Cloud Vision, Azure AI Vision, Clarifai).
* Add comprehensive unit and integration tests for both backend and frontend. [cite: 17]
* Improve frontend UI/UX and add more detailed error messages.
* Implement rate limiting on the backend API.
* Containerize frontend build step separately for production builds.

## 8. Contact
For any questions or issues, please contact [Your Name/Email].
