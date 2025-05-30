# Receipt Processor

This project is a web service that calculates reward points for receipts according to a set of business rules. It’s built in Python using Flask and is designed to match the provided API specification for the take-home assessment.

The service allows you to submit a receipt and receive a unique ID in return. You can then use this ID to retrieve the number of points awarded for that receipt. All data is stored in memory.

When a receipt is submitted, the app checks that all required fields are present and correctly formatted. It then calculates points based on the rules described in the assessment, stores the result in memory with a randomly generated ID, and returns that ID to you. When you ask for the points for a specific ID, the app looks up the points and returns them.

You can run the service either locally with Python or inside a Docker container.

Two example receipts are provided in the Example folder. To test, submit one of these receipts to the service’s POST endpoint, then use the returned ID to check the points with the GET endpoint.

## Project structure

- `app.py` – Main application file containing the Flask web service and business logic.
- `requirements.txt` – List of Python dependencies needed to run the app.
- `Dockerfile` – Instructions for building a Docker image of the service.
- `README.md` – This file, describing the project and how to use it.
- `api.yml` – OpenAPI specification for the API endpoints and request/response formats.
- `Example/` – Folder containing sample receipt JSON files for testing.

## How to Run

1. Clone the repository
   git clone https://github.com/AbhinavS-30/receipt-processor.git
   cd receipt-processor

2. Create Virtual Environment
   python -m venv venv
   venv\Scripts\activate

3. Install dependencies
   pip install -r requirements.txt

4. Start the server
   python app.py

The app will run on http://localhost:8080.

## Testing API

You can use Postman to test the endpoints.
Here’s how to test with the provided screenshots:

Example-1: morning-receipt.json

- POST /receipts/process
![WhatsApp Image 2025-05-30 at 14 25 40_711affed](https://github.com/user-attachments/assets/0eac0be6-abff-4a60-a343-755fd446b3d9)

- GET /receipts/4789cd01-910d-4c4e-b5d6-d88cf47d8946/points
![WhatsApp Image 2025-05-30 at 14 27 17_5440e216](https://github.com/user-attachments/assets/bb5563d0-0e2e-4b66-9090-9c8679ee327f)

Example-2: simple-receipt.json

- POST /receipts/process
![WhatsApp Image 2025-05-30 at 14 28 53_51a20649](https://github.com/user-attachments/assets/1113991a-24eb-4025-b059-7225dbeb5aa6)

- GET /receipts/39679973-6813-47bc-b89a-39c951551f17/points
![WhatsApp Image 2025-05-30 at 14 30 27_3e6d25cb](https://github.com/user-attachments/assets/46addf7c-52f8-45ef-bb69-a4d114876b7a)


If you have any questions or run into any issues, please feel free to reach out to me at abhinav.302001@gmail.com.
