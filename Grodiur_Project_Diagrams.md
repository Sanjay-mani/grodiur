# GRODIUR - Project Diagrams (BCA Final Year)

This document contains professional, academic-style diagrams generated for the **GRODIUR – Online Grocery Shopping System** project. 

---

## 1. DFD Level 0 (Context Diagram)

```mermaid
graph TD
    %% Styling
    classDef entity fill:#fff,stroke:#000,stroke-width:2px;
    classDef process fill:#fff,stroke:#000,stroke-width:3px;

    C((Customer / User)):::entity
    A((Admin)):::entity
    S[1.0 GRODIUR Grocery System]:::process

    %% Customer Flows
    C -- "Registration / Login" --> S
    C -- "Browse & Search Products" --> S
    C -- "Add to Cart" --> S
    C -- "Place Orders" --> S
    C -- "Online Payment" --> S
    
    S -- "Order Confirmation" --> C
    S -- "Product Information" --> C
    S -- "Payment Status" --> C

    %% Admin Flows
    A -- "Manage Products & Inventory" --> S
    A -- "Update Order Status" --> S
    A -- "View User Details" --> S
    
    S -- "Update Confirmation" --> A
    S -- "System Reports" --> A
```

---

## 2. DFD Level 1 (Functional Decomposition)

```mermaid
graph TD
    %% Styling
    classDef entity fill:#fff,stroke:#000,stroke-width:2px;
    classDef process fill:#fff,stroke:#000,stroke-width:2px;
    classDef store fill:#fff,stroke:#000,stroke-width:1px;

    U((Customer)):::entity
    AD((Admin)):::entity
    
    D1[[Data Store: SQLite DB]]:::store

    subgraph "Main Process Modules"
        P1(1.0 Auth & OTP Verification):::process
        P2(2.0 Product Management):::process
        P3(3.0 Cart & Coupon System):::process
        P4(4.0 Order Processing):::process
        P5(5.0 Payment Gateway):::process
        P6(6.0 Rule-Based Chatbot):::process
    end

    %% Flows
    U -- "Credentials / OTP" --> P1
    P1 -- "User Data" --> D1
    
    U -- "Search / Browse" --> P2
    P2 -- "Fetch Products" --> D1
    
    U -- "Add Items" --> P3
    P3 -- "Cart Data" --> D1
    
    U -- "Checkout" --> P4
    P4 -- "Create Order" --> D1
    
    P4 -- "Initiate Payment" --> P5
    P5 -- "Verify Signature" --> D1
    
    U -- "Support Queries" --> P6
    P6 -- "Fetch Order Status" --> D1

    AD -- "Inventory Update" --> P2
    AD -- "Order Status Change" --> P4
```

---

## 3. Entity Relationship (ER) Diagram

```mermaid
erDiagram
    USER ||--|| USER_PROFILE : "has"
    USER ||--o{ ADDRESS : "manages"
    USER ||--o{ ORDER : "places"
    USER ||--o{ REVIEW : "writes"
    USER ||--|| CART : "owns"

    CATEGORY ||--o{ PRODUCT : "contains"
    PRODUCT ||--o{ CART_ITEM : "included_in"
    PRODUCT ||--o{ ORDER_ITEM : "sold_in"
    PRODUCT ||--o{ REVIEW : "rated_by"

    CART ||--o{ CART_ITEM : "holds"
    ORDER ||--o{ ORDER_ITEM : "contains"

    USER {
        int user_id PK
        string username
        string email
        string password
    }

    PRODUCT {
        int product_id PK
        string name
        decimal price
        int stock_qty
        string image
    }

    ORDER {
        int order_id PK
        string order_number
        decimal total_amount
        string status
        datetime created_at
    }

    OTP_VERIFICATION {
        string identifier
        string otp
        string status
        datetime expires_at
    }
```

---

## 4. UML Use Case Diagram

```mermaid
graph LR
    %% Styling
    classDef actor fill:#fff,stroke:#000,stroke-width:2px;
    classDef usecase fill:#fff,stroke:#000,stroke-width:1px;

    Customer((Customer)):::actor
    Admin((Admin)):::actor

    subgraph "GRODIUR System Use Cases"
        UC1(Register / Login):::usecase
        UC2(Verify Mobile OTP):::usecase
        UC3(Browse & Search Products):::usecase
        UC4(Manage Cart):::usecase
        UC5(Apply Coupon):::usecase
        UC6(Checkout & Payment):::usecase
        UC7(Track Order Status):::usecase
        UC8(Submit Review):::usecase
        UC9(Chat with Bot):::usecase
        
        UC10(Add / Update Products):::usecase
        UC11(Manage Orders):::usecase
        UC12(View Users & Reviews):::usecase
        UC13(Inventory Control):::usecase
    end

    Customer --> UC1
    Customer --> UC2
    Customer --> UC3
    Customer --> UC4
    Customer --> UC6
    Customer --> UC7
    Customer --> UC8
    Customer --> UC9

    Admin --> UC1
    Admin --> UC10
    Admin --> UC11
    Admin --> UC12
    Admin --> UC13
```

---

## 5. UML Class Diagram

```mermaid
classDiagram
    class User {
        +int id
        +string username
        +string email
        +login()
        +logout()
    }

    class Product {
        +int id
        +string name
        +decimal selling_price
        +decimal mrp_price
        +int stock
        +boolean is_available
    }

    class Cart {
        +int id
        +get_total()
        +apply_coupon()
    }

    class CartItem {
        +int id
        +int quantity
        +get_subtotal()
    }

    class Order {
        +int id
        +string order_id
        +string status
        +string payment_status
        +generate_invoice()
    }

    class Review {
        +int id
        +int rating
        +string comment
    }

    User "1" -- "1" Cart : owns
    Cart "1" -- "*" CartItem : contains
    Product "1" -- "*" CartItem : defines
    User "1" -- "*" Order : places
    Order "1" -- "*" Review : rated_in
```

---

## 6. System Architecture Diagram

```mermaid
graph TD
    %% Styling
    classDef layer fill:#fff,stroke:#000,stroke-width:2px;
    classDef component fill:#fff,stroke:#000,stroke-width:1px;

    subgraph "Client Side"
        Browser[User Web Browser]
        UI[HTML5 / CSS3 / Bootstrap 5 / JS]
    end

    subgraph "Server Side (Django Framework)"
        URL[URL Dispatcher]:::component
        Views[Django Views - Business Logic]:::layer
        Models[Django Models - ORM]:::layer
        Templates[Django Templates - UI Engine]:::component
    end

    subgraph "Data Layer"
        DB[(SQLite Database)]:::layer
    end

    subgraph "External Integrations"
        Twilio[Twilio API - SMS OTP]
        Razorpay[Razorpay - Payments]
        Google[Google OAuth - Social Login]
    end

    Browser <--> UI
    UI <--> URL
    URL <--> Views
    Views <--> Templates
    Views <--> Models
    Models <--> DB

    Views -- "Request OTP" --> Twilio
    Views -- "Process Payment" --> Razorpay
    Views -- "Auth Request" --> Google
```
