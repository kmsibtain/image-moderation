# image-moderation
# Image Moderation API

## 1. Introduction
This project implements an Image Moderation API using FastAPI for the backend and React for the frontend. Its purpose is to automatically detect and block harmful, illegal, or otherwise unwanted imagery such as graphic violence, hate symbols, explicit nudity, self-harm depictions, or extremist propaganda from being served to end users.

## 2. Objectives Met
* **Secure, well-structured REST API in FastAPI:** Designed with clear routing, models, and services.
* **Authentication/Authorization:** Implemented using bearer tokens with admin-only access for certain endpoints.
* **MongoDB Data Modeling and Usage Tracking:** Utilizes MongoDB for storing tokens and recording API usage per token.
* **Docker Containerization:** Both backend and frontend are containerized using Docker, managed by `docker-compose.yml`.
* **Minimal Frontend UI:** A React application to interact with the API, allowing token management and image uploads.
* **Best Practices:** Follows good project structure, includes documentation, and aims for clean code.

## 3. Technical Stack
* **Backend:** Python 3.9, FastAPI, Uvicorn, PyMongo, Pillow.
* **Frontend:** React, HTML, CSS, JavaScript.
* **Database:** MongoDB.
* **Containerization:** Docker, Docker Compose.


## 4. API Endpoints

### 4.1 Authentication Endpoints (Admin-Only)

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

### 4.2 Moderation Endpoint

* **`POST /moderate`**
    * **Description:** Analyzes an uploaded image and returns a content-safety report.
    * **Authentication:** Any valid bearer token in `Authorization: Bearer <token>` header.
    * **Request Body:** `multipart/form-data` with a `file` field containing the image.
    * **Response:** JSON object containing filename, content type, and a `moderation_report` with categories (e.g., violence, nudity) and their detection status/confidence.


## 5. Setup Instructions

### Prerequisites
* Docker Desktop (includes Docker and Docker Compose)
* Git

### Steps

1.  **Clone the repository:**
    ```bash
    git clone "https://github.com/kmsibtain/image-moderation"
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

3.  **Build and Run with Docker Compose:** 
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

