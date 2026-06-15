# A Project Report On
**GRODIUR – AI Powered Online Grocery Shopping System Using Django Framework**

Submitted in partial fulfillment for the award of the Degree of
**BACHELOR OF COMPUTER APPLICATIONS (BCA)**
Bangalore University

**Submitted By:**
Name: SANJAY.M
Register Number: U03AQ23S0011

**Under the Guidance of:**
Guide Name: JAYANTH L

**Sixth Semester**
**ASC Degree College, Bangalore**

---

## 1. ABSTRACT

The advent of e-commerce has fundamentally transformed how consumers interact with retail markets, bringing unparalleled convenience to their fingertips. "GRODIUR" is a comprehensive, scalable, and responsive online grocery shopping system designed to streamline the grocery purchasing process. Built on the robust Django framework, this project addresses the limitations of traditional grocery shopping—such as time consumption, limited stock visibility, and geographic constraints—by providing a seamless digital storefront.

The primary problem this application solves is the inefficiency in local grocery supply chains and the lack of accessible, user-friendly digital grocery platforms that cater to both modern aesthetic standards and rigorous functional requirements. Grodiur bridges this gap by offering a fully integrated platform featuring secure user authentication (including Twilio-based OTP and Google OAuth), intuitive product management, dynamic cart operations, and an integrated Razorpay checkout system for secure financial transactions.

Technologically, the platform utilizes Python and Django for the backend, coupled with SQLite for robust data management during the initial phases. The frontend is powered by HTML5, CSS3, JavaScript, and Bootstrap 5, ensuring a highly responsive and modern user interface. Furthermore, Grodiur incorporates a rule-based intelligent chatbot assistant designed to handle order tracking, product search, and refund inquiries instantly, significantly reducing the overhead on customer support.

Key features include a dynamic product availability system, a comprehensive review and rating module, an intelligent cart with coupon logic, and a fully customized administrative panel for inventory and order management. The system is designed following the Model-View-Template (MVT) architecture, ensuring high maintainability and security against common web vulnerabilities like CSRF and XSS. Ultimately, Grodiur stands as a technically proficient, secure, and commercially viable e-commerce solution tailored for modern grocery retail.

**Keywords:** E-commerce, Django Framework, Python, Online Grocery, Razorpay Integration, Chatbot, Web Development, MVT Architecture.

---

## 2. INTRODUCTION

### 2.1 Introduction of the Project
The modern retail landscape is rapidly shifting towards digital platforms, driven by consumer demand for convenience, speed, and variety. Grodiur is an advanced online grocery shopping application developed to meet these growing demands. It provides users with a comprehensive digital supermarket experience from the comfort of their homes. Built using Python's Django framework, Grodiur is not just a digital catalog but a fully functional e-commerce ecosystem capable of handling complex business logic, from secure multi-factor authentication to payment processing and order lifecycle management.

### 2.2 Objectives of the Project
The primary objectives of the Grodiur project are to:
- Develop a secure, scalable, and user-friendly online grocery platform.
- Implement a robust authentication system utilizing traditional email, social logins (Google OAuth), and secure mobile OTP verification.
- Create a seamless shopping experience with dynamic cart management, coupon applications, and tax/delivery fee calculations.
- Integrate a reliable payment gateway (Razorpay) to facilitate secure digital transactions.
- Provide an interactive customer support experience through an integrated rule-based chatbot capable of tracking orders and answering FAQs.
- Equip store administrators with a powerful, customized dashboard to manage inventory, track orders, and monitor user engagement.

### 2.3 Scope of the Project
The scope of Grodiur encompasses the full lifecycle of an e-commerce transaction. It covers user registration and profile management, catalog browsing with search and filter capabilities, shopping cart operations, secure checkout, and post-purchase activities like order tracking and product reviewing. The system is designed to be accessible across various devices, ensuring a responsive mobile-first approach. Future scalability is built into the architecture, allowing for easy migration to enterprise databases like PostgreSQL and integration with advanced machine learning algorithms.

### 2.4 Limitations of Existing Systems
Many existing local grocery platforms suffer from several limitations:
- **Poor User Interface:** Cluttered, non-responsive designs that frustrate mobile users.
- **Lack of Real-time Tracking:** Inability for users to instantly check their order status without calling customer service.
- **Insecure Authentication:** Reliance on basic passwords without multi-factor or OTP verification, leading to compromised accounts.
- **Limited Payment Options:** Lack of integrated digital payments, forcing reliance solely on Cash on Delivery.
- **Scalability Issues:** Tightly coupled architectures that break under heavy user load during peak hours.

### 2.5 Proposed System
Grodiur overcomes these limitations by proposing a modern, decoupled, and secure architecture. The proposed system features a sleek, responsive frontend built with Bootstrap 5. It incorporates a sophisticated OTP system via Twilio to ensure user authenticity. The integration of Razorpay allows for seamless UPI, Card, and Netbanking transactions. Furthermore, the inclusion of a dedicated conversational chatbot allows users to instantly query their order status by simply pasting their Order ID, providing an immediate, automated customer service experience.

### 2.6 Statement of Problem and Methodology (SDLC Model)
**Problem Statement:** To design and implement an efficient, secure, and highly available web-based grocery shopping application that resolves the friction in traditional and sub-par digital grocery shopping experiences.

**Methodology:** The project was developed adhering to the Agile Software Development Life Cycle (SDLC) model. This iterative approach allowed for continuous integration and continuous delivery (CI/CD). The phases included:
- **Requirement Gathering:** Analyzing market needs and defining the technical stack (Django, SQLite, Bootstrap).
- **System Design:** Creating Entity-Relationship diagrams, Data Flow Diagrams, and structuring the Django MVT architecture.
- **Implementation:** Coding the models, views, and templates. Dividing the project into manageable apps (accounts, products, cart, orders, etc.).
- **Testing:** Conducting unit testing on core functions (e.g., cart total calculations) and integration testing for payment gateways.
- **Deployment:** Configuring the application for production using Gunicorn, Whitenoise for static files, and hosting on platforms like PythonAnywhere.

---

## 3. LITERATURE SURVEY

### Existing Systems and Comparison
Platforms like BigBasket, Blinkit, and Amazon Fresh dominate the online grocery market. While highly capable, these platforms are resource-heavy and complex. Grodiur aims to provide a lightweight, highly efficient alternative that can be easily adopted by mid-sized grocery retailers. Unlike basic open-source templates, Grodiur integrates a localized OTP authentication system and an in-built customer service chatbot, features usually reserved for enterprise-level applications.

### Feasibility Study
Before development, a thorough feasibility study was conducted to ensure the project's viability.

**Technical Feasibility:**
The project is technically feasible as it utilizes Python and Django, which are open-source and highly supported. The required hardware is standard, and cloud hosting platforms like PythonAnywhere or Render provide the necessary infrastructure to deploy the application without significant upfront server costs.

**Operational Feasibility:**
Operationally, Grodiur is designed with intuitive user interfaces. The admin panel is customized to be user-friendly, allowing store managers with minimal technical knowledge to update product catalogs, manage inventory, and process orders efficiently. The automated chatbot further reduces operational overhead by handling basic customer inquiries.

**Economic Feasibility:**
As the project utilizes open-source technologies (Python, Django, SQLite, Bootstrap), the development cost is minimal. The only recurring costs in a production environment would be server hosting, Twilio API credits for SMS OTPs, and payment gateway transaction fees. This makes the system highly economically viable for small to medium businesses.

**Legal Feasibility:**
The system complies with standard data protection norms by utilizing secure password hashing (PBKDF2), secure session management, and adhering to CORS and CSRF protection policies mandated by modern web standards. Razorpay handles payment processing, ensuring PCI-DSS compliance.

**Schedule Feasibility:**
By utilizing Django's rapid development capabilities and built-in administrative interface, the project timeline was significantly reduced, allowing for the completion of the entire software lifecycle within the stipulated final year academic semester.

---

## 4. SOFTWARE SPECIFICATION
The software stack for Grodiur was carefully selected to ensure security, rapid development, and high performance.
- **IDE (Integrated Development Environment):** Visual Studio Code (VS Code)
- **Backend Language:** Python 3.x
- **Web Framework:** Django 5.x
- **Frontend Technologies:** HTML5, CSS3, JavaScript (ES6)
- **Frontend Framework/Library:** Bootstrap 5, crispy-bootstrap5
- **Database:** SQLite (Development & Initial Production)
- **Authentication Libraries:** django-allauth, djangorestframework-simplejwt
- **Payment Gateway:** Razorpay API
- **SMS/OTP Gateway:** Twilio API
- **Server/Deployment:** Gunicorn, Whitenoise, PythonAnywhere / Render

---

## 5. HARDWARE SPECIFICATION
The hardware requirements for developing and running the application are relatively modest due to the optimized nature of the Django framework.
- **Processor:** Intel Core i3 / AMD Ryzen 3 or higher
- **RAM:** Minimum 4 GB (8 GB recommended)
- **Storage:** Minimum 256 GB SSD 
- **Operating System:** Windows 10/11, macOS, or Linux
- **Mobile Support:** The frontend is fully responsive and optimized for mobile browsers.
- **Internet Requirements:** A stable broadband connection is required for external API communications.

---

## 6. TECHNOLOGIES USED

**Python**
Python is a high-level, interpreted programming language known for its readability and concise syntax. In Grodiur, Python handles all backend logic, database modeling, and algorithmic processing.

**Django Framework**
Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. It follows the MVT (Model-View-Template) architecture. Django provides an integrated ORM (Object-Relational Mapping), which abstracts SQL queries, making database operations secure against SQL injection attacks.

**SQLite**
SQLite is a C-language library that implements a small, fast, self-contained, high-reliability SQL database engine. It is used as the primary database for Grodiur to store user profiles, product catalogs, cart details, and order histories.

**Bootstrap & Frontend Tech**
Bootstrap 5 provides a robust grid system and pre-styled components, ensuring Grodiur is aesthetically pleasing and mobile-responsive. HTML5 structures the web pages, CSS3 handles custom styling (like the Grodiur color palette and animations), and JavaScript manages dynamic client-side interactions, such as updating cart quantities asynchronously and handling the chatbot UI.

---

## 7. MODULE DESCRIPTION

The Grodiur application is highly modular, divided into specific Django apps. This separation of concerns ensures that the codebase is maintainable and scalable.

### 7.1 Authentication Module (accounts)
This module manages user identities. It extends the default Django User model using a `UserProfile` model to store additional information such as phone numbers, addresses, and profile pictures. It integrates `django-allauth` for Google OAuth integration, allowing users to sign in seamlessly using their Google accounts. Password validation and secure session handling are strictly enforced.

### 7.2 OTP Verification Module (otp_auth)
Security is paramount in e-commerce. The `otp_auth` module utilizes the Twilio API to send One-Time Passwords (OTPs) to users' mobile phones. It includes an `OTPVerification` model that tracks OTP generation, status (pending, verified, expired), attempts, and IP addresses to prevent abuse. This ensures that cash-on-delivery orders and account creations are authenticated by a real human.

### 7.3 Product Management Module (products)
This module handles the digital catalog. It includes models for `Category` and `Product`. The Product model stores critical data such as name, description, MRP price, selling price, stock availability, and images. The system is designed dynamically so that products marked as 'unavailable' are greyed out on the frontend rather than completely hidden, allowing users to know what Grodiur usually stocks.

### 7.4 Cart Module (cart)
The cart module is the core of the shopping experience. It comprises the `Cart` and `CartItem` models. It contains complex business logic to calculate the final checkout price dynamically. It seamlessly handles quantity updates and ensures that out-of-stock items cannot be added.

### 7.5 Order Module (orders)
Once a cart is checked out, the data is transferred to the order module. It generates a unique Order ID (e.g., GRO-2026-XXXX). It manages multiple payment states (Pending, Paid, Failed) and order statuses (Processing, Shipped, Delivered, Cancelled). It includes specialized logic for Cash on Delivery (COD) versus online payments via Razorpay. A robust signature verification system ensures Razorpay transactions are securely validated on the backend.

### 7.6 Review Module (reviews)
Customer feedback is crucial for online retail. The review module allows users to rate products (1 to 5 stars) and leave text comments. The system restricts reviews to users who have successfully purchased and received the product, ensuring high authenticity of product ratings.

### 7.7 Chatbot Module (chatbot)
Grodiur features an intelligent rule-based chatbot designed to improve customer support. Built directly into the backend using regex and pattern matching, it analyzes user input to detect intents such as "Track Order", "Refunds", or "Product Search". For example, if a user inputs an Order ID, the system queries the SQLite database and securely returns the real-time status of that specific order.

### 7.8 Admin Module
Leveraging Django's powerful built-in admin panel, this module is highly customized. It allows store managers to oversee operations without needing SQL knowledge. Administrators can add new products, update inventory, manage promotional coupons, view detailed order invoices, and monitor registered users in a clean, professional interface.

---

## 8. DESIGN AND IMPLEMENTATION

### System Architecture (MVT Pattern)
Grodiur employs Django's Model-View-Template (MVT) architecture:
- **Model:** Defines the data structure and database schema (e.g., Product, Cart, Order models). Django's ORM translates these Python classes into SQLite tables.
- **View:** The business logic layer. Views receive HTTP requests, interact with the Models to fetch or save data, and pass the data to the Templates. For example, `cart_add` view updates the CartItem and redirects the user.
- **Template:** The presentation layer. HTML files mixed with Django Template Language (DTL) tags render the final web page dynamically based on the data provided by the View.

### Database Schema Explanation
The database is highly relational. The core relationships include:
- **User to UserProfile:** One-to-One relationship. Each user has exactly one profile containing extended details.
- **User to Address:** One-to-Many relationship. A user can have multiple saved delivery addresses.
- **Category to Product:** One-to-Many relationship. A category contains multiple products.
- **Cart to CartItem:** One-to-Many relationship. A cart contains various products with specific quantities.
- **CartItem to Product:** Many-to-One relationship. A specific cart item links to the main product database to fetch current pricing.
- **Order to OrderItem:** Similar to cart, but immutable. Once an order is placed, the prices are locked into OrderItem records to prevent future price changes from affecting historical order invoices.

### Workflow Explanation
The typical user workflow involves:
1. User lands on the homepage and browses categories.
2. User clicks on a product to view details and reviews.
3. User adds the product to the cart (prompts login if unauthenticated).
4. User signs in via Email, Phone (OTP), or Google OAuth.
5. User reviews the cart, applies a discount coupon, and proceeds to checkout.
6. User selects a delivery address and chooses Payment Method (Razorpay or COD).
7. Upon successful payment, the backend verifies the transaction and generates an Order ID.
8. User is redirected to the Order Success page and can track the order via the Chatbot.

---

## 9. TESTING

Testing ensures the system behaves as expected under various conditions and prevents bugs from reaching the production environment.

### Test Plan
The testing strategy involved Unit Testing for individual Python functions (like discount calculations), Integration Testing for external APIs (Razorpay, Twilio), and UI/Functional Testing to ensure the frontend behaves correctly across devices.

### Sample Test Cases

| Test Case ID | Module | Test Description | Expected Result | Actual Result | Status |
|---|---|---|---|---|---|
| TC01 | Authentication | User attempts to login with incorrect password. | System displays "Invalid credentials" error message. | System displayed error message. | Pass |
| TC02 | OTP Auth | User enters an expired OTP during phone verification. | System rejects OTP and prompts to request a new one. | System rejected expired OTP. | Pass |
| TC03 | Cart | User adds an out-of-stock product to the cart. | Add to cart button is disabled; action fails. | Button disabled, prevented addition. | Pass |
| TC04 | Cart | Order total falls below free delivery threshold. | Delivery fee of ₹40 is added to the final total. | ₹40 fee accurately calculated. | Pass |
| TC05 | Payment | Razorpay payment returns successful payload. | Order status updates to 'Paid' and cart clears. | Status updated, cart cleared securely. | Pass |
| TC06 | Chatbot | User inputs valid Order ID in chatbot window. | Chatbot returns accurate tracking timeline. | Chatbot displayed tracking UI. | Pass |

---

## 10. CONCLUSION AND FUTURE SCOPE

### Project Conclusion
The "GRODIUR" project successfully demonstrates the implementation of a full-fledged, production-ready e-commerce platform using the Django framework. It effectively solves the problem of digital grocery shopping by providing a fast, secure, and user-centric platform. The successful integration of multi-factor authentication, secure payment gateways, and an interactive customer support chatbot proves that mid-scale web applications can offer enterprise-level features while remaining maintainable and efficient.

### Advantages
- Highly secure architecture protecting against common web vulnerabilities.
- Automated customer service via the integrated chatbot reduces manual workload.
- Seamless checkout process with multiple payment options improves conversion rates.
- Responsive design ensures optimal performance across desktops, tablets, and mobile phones.

### Future Scope
While the current system is highly capable, future iterations could include:
- **AI Integration:** Replacing the rule-based chatbot with a Large Language Model (LLM) for natural conversational abilities.
- **Machine Learning:** Implementing a recommendation engine to suggest products based on user purchase history.
- **Mobile App:** Developing native Android and iOS applications using React Native connected to the existing Django REST Framework endpoints.
- **Delivery Agent App:** Creating a separate portal for delivery personnel to update real-time GPS tracking for orders.

---

## 11. BIBLIOGRAPHY
- Django Software Foundation. (2026). *Django Documentation.* Retrieved from https://docs.djangoproject.com/
- Python Software Foundation. (2026). *Python 3 Reference Manual.* Retrieved from https://docs.python.org/3/
- Bootstrap Team. (2026). *Bootstrap 5 Documentation.* Retrieved from https://getbootstrap.com/docs/5.0/
- Razorpay Software Pvt Ltd. (2026). *Razorpay Payment Gateway API Documentation.* Retrieved from https://razorpay.com/docs/
- Twilio Inc. (2026). *Twilio SMS API Documentation.* Retrieved from https://www.twilio.com/docs/sms
- Williams, S. (2020). *Django for Professionals: Production websites with Python & Django.* WelcomeToCode.

---

## APPENDIX A: VIVA & INTERVIEW QUESTIONS

**1. What is Django and why did you choose it for this project?**
**Answer:** Django is a high-level Python web framework that encourages rapid development and clean design. I chose it because it comes "batteries-included", meaning it has built-in features for authentication, database ORM, and an admin panel, which are essential for an e-commerce platform like Grodiur. It also provides excellent security against SQL injection and CSRF attacks.

**2. Explain the MVT Architecture.**
**Answer:** MVT stands for Model-View-Template. 
- **Model:** Manages the database schema and data logic.
- **View:** Contains the business logic, fetches data from the Model, and passes it to the Template.
- **Template:** Handles the presentation layer (HTML/CSS) to display data to the user.

**3. How did you handle payments in Grodiur?**
**Answer:** I integrated the Razorpay Payment Gateway. When a user checks out, a Razorpay order is created via the backend API. The frontend displays the checkout widget. Upon successful payment, Razorpay sends back a payment ID and signature, which my backend mathematically verifies using the secret key to ensure the transaction wasn't tampered with.

**4. How does the Chatbot work? Is it AI-based?**
**Answer:** The chatbot is currently a rule-based system, not a generative AI. It uses Python's regular expressions (regex) and pattern matching to detect specific intents like greetings, product searches, and order tracking. If an order ID is detected, it queries the database and securely returns the live status of that order.

**5. What is the role of SQLite? Why not MySQL or PostgreSQL?**
**Answer:** SQLite is used because it is lightweight, requires zero configuration, and is perfect for development. For enterprise-level scaling, Django's ORM allows seamless migration to PostgreSQL by simply changing the database settings, without altering any underlying queries.

**6. How is user authentication managed?**
**Answer:** User authentication is managed using Django's built-in auth system extended with `django-allauth` for Google OAuth integration. Additionally, I implemented a custom OTP module using the Twilio API to verify mobile numbers securely.

**7. Can you explain the flow of the OTP verification?**
**Answer:** When a user requests phone login, a Twilio API call sends a random 6-digit OTP to their phone. The OTP, along with a timestamp, is stored in the `OTPVerification` model with a "pending" status. The user has 5 minutes and 3 attempts to enter the correct OTP. Upon successful entry, the backend verifies the code, updates the status to "verified", logs the user in, and prevents the OTP from being reused.

**8. How do you handle out-of-stock items in the cart?**
**Answer:** In the `products` module, items are not removed but marked out-of-stock. In the `cart` module, validation checks the available quantity against the cart quantity. If stock is insufficient or 0, the "Add to Cart" button is disabled on the frontend, and backend views prevent insertion or checkout.

---
**End of Report**
