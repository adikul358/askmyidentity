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
