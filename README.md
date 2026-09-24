# FastAPI College Event and Lost & Found API

## 1. Project Description
This repository contains two RESTful APIs built with FastAPI and SQLModel:
- **Task 1 (Lost & Found System):** Allows college students to report lost or found items on campus, update their status, and query items by category or status.
- **Task 2 (Campus Event Seat Reservation API):** Manages college events (workshops, hackathons, seminars) and allows students to reserve seats dynamically. It actively checks event capacities and prevents overbooking or booking for closed events.

## 2. Technologies Used
- **Python 3**
- **FastAPI** (Web Framework)
- **SQLModel** (ORM and Data Validation)
- **Pydantic** (Data Validation and Settings Management)
- **SQLite** (Database)
- **Uvicorn** (ASGI Server)

## 3. Installation Steps
1. Clone the repository to your local machine:
   ```bash
   git clone <your-github-repo-url>
   cd <repository-folder>
   ```
2. Create and activate a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 4. Command to Run the FastAPI Application
To run **Task 1** (Lost & Found API):
```bash
uvicorn task_1.main:app --reload
```

To run **Task 2** (Event Reservation API):
```bash
uvicorn task_2.main:app --reload
```

## 5. Swagger UI URL
Once the server is running, you can access the interactive API documentation (Swagger UI) at:
- **http://127.0.0.1:8000/docs**

## 6. Brief Description of Available Endpoints

### Task 1: Lost & Found
- `POST /items`: Create a new lost/found item report.
- `GET /items`: List all reported items.
- `GET /items/{item_id}`: Retrieve a specific item by its ID.
- `PUT /items/{item_id}`: Update the details/status of an item.
- `DELETE /items/{item_id}`: Delete an item report.
- `GET /items/status/{status}`: Filter items by their status (Lost, Found, Returned).
- `GET /items/category/{category}`: Filter items by their category.

### Task 2: Campus Event Reservation
- `POST /events`: Create a new event.
- `GET /events`: Return a list of all events.
- `GET /events/{event_id}`: Get details of a specific event.
- `PUT /events/{event_id}`: Update an event's information.
- `DELETE /events/{event_id}`: Delete an event and its reservations.
- `POST /events/{event_id}/reserve`: Make a reservation (if open and seats remain).
- `GET /events/{event_id}/reservations`: View all reservations for a given event.
- `GET /events/{event_id}/availability`: View the event's capacity, booked, and remaining seats.
- `DELETE /reservations/{reservation_id}`: Cancel a specific reservation.
