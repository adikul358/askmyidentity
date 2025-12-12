# Marketplace Platform

## Requirements

- Use Django, Django REST Framework (DRF), and JWT authentication.
- Each vendor should have:
    - Vendor information (store name, contact, domain/subdomain)
    - Products, Orders, and Customers, visible only to that vendor
- Implement role-based access:
    - Store Owner can manage all data (products, orders, users)
    - Staff can manage only orders and products assigned to them
    - Customer can view and place orders
- JWT tokens must include vendor ID and role for authorization.
- APIs required for:
    - Authentication (register/login)
    - CRUD for Products and Orders
    - Order placement and listing (vendor-specific)

## Installation

1. Setup Environment
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
2. Install Requirements
    ```
    pip install -r requirements.txt
    ```
2. Run Server
    ```
    pip install -r requirements.txt
    ```

## Cloud Deployment

The app has been deployed on GCP Cloud Run using Cloud SQL DB.

Public URL: https://askmyidentity-720236446091.europe-west1.run.app


## API

<img width="2526" height="1744" alt="Screenshot 2025-12-12 at 23 29 09" src="https://github.com/user-attachments/assets/fd1a7c46-dbad-4970-b1b2-69ff53e27182" />

<img width="2526" height="1744" alt="Screenshot 2025-12-12 at 23 29 01" src="https://github.com/user-attachments/assets/fad668e1-1f9f-483b-ab21-9b8e7b104eb4" />

## Entity Structure
<img width="747" height="755" alt="entity-diagram drawio" src="https://github.com/user-attachments/assets/040a870d-bfc4-443e-987b-ce06527bdf9d" />

