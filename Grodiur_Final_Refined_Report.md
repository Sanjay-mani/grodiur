# PROJECT REPORT
## GRODIUR – Online Grocery Shopping System Using Django Framework

---

### **COLLEGE DETAILS**
**College Name:** ASC Degree College, Bangalore  
**Department:** Bachelor of Computer Applications (BCA)  
**Batch:** 2023-2026  
**Semester:** Sixth Semester  

### **STUDENT DETAILS**
**Name:** SANJAY.M  
**Register Number:** U03AQ23S0011  

### **GUIDE DETAILS**
**Guide Name:** JAYANTH L  

---

## **CERTIFICATE**

This is to certify that the project entitled **"GRODIUR – Online Grocery Shopping System Using Django Framework"** is a bonafide work carried out by **SANJAY.M (Reg No: U03AQ23S0011)**, a student of **ASC Degree College, Bangalore**, in partial fulfillment of the requirements for the award of the degree of **Bachelor of Computer Applications (BCA)** by **Bangalore University** during the academic year 2023-2026.

<br><br><br>

**____________________**  
**Signature of the Guide**  

<br><br>

**____________________**  
**Head of the Department**  

<br><br>

**____________________**  
**External Examiner**  

---

## **DECLARATION**

I, **SANJAY.M**, hereby declare that the project work entitled **"GRODIUR – Online Grocery Shopping System Using Django Framework"** submitted to the Department of Computer Applications, ASC Degree College, Bangalore, is a record of independent work carried out by me under the guidance of **JAYANTH L**.

I also declare that this project has not been submitted previously to any other university or institution for the award of any degree or diploma.

<br><br><br>

**Place:** Bangalore  
**Date:**  

<br><br>

**____________________**  
**SANJAY.M**  
**(Reg No: U03AQ23S0011)**

---

## **ACKNOWLEDGEMENT**

I would like to express my deep sense of gratitude to my project guide, **JAYANTH L**, for his valuable guidance and support throughout the development of this project.

I am also thankful to the **Head of the Department** and the **Principal of ASC Degree College** for providing me with the necessary facilities and a conducive environment to complete this project.

Finally, I would like to thank my family and friends for their constant encouragement and moral support during the course of this work.

<br><br><br>

**____________________**  
**SANJAY.M**

---

## **TABLE OF CONTENTS**

1. **ABSTRACT**
2. **INTRODUCTION**
    * 2.1 Overview
    * 2.2 Objectives
    * 2.3 Scope of the Project
    * 2.4 Existing System vs Proposed System
3. **LITERATURE SURVEY**
    * 3.1 Study of Existing Systems
    * 3.2 Feasibility Study
4. **SYSTEM SPECIFICATION**
    * 4.1 Hardware Requirements
    * 4.2 Software Requirements
5. **TECHNOLOGIES USED**
6. **SYSTEM DESIGN**
    * 6.1 Data Flow Diagrams (DFD)
    * 6.2 Entity Relationship Diagram (ERD)
    * 6.3 UML Diagrams
    * 6.4 Database Schema
7. **MODULE DESCRIPTION**
    * 7.1 Authentication & Profile
    * 7.2 Product Management
    * 7.3 Shopping Cart & Coupons
    * 7.4 Order Processing & Payments
    * 7.5 Customer Support Chatbot
8. **TESTING**
    * 8.1 Test Plan
    * 8.2 Test Cases
9. **CONCLUSION AND FUTURE SCOPE**
10. **BIBLIOGRAPHY**
11. **APPENDIX - VIVA QUESTIONS**

---

## **1. ABSTRACT**

The **GRODIUR** project is a web-based application designed to provide a convenient and efficient platform for online grocery shopping. Developed using the **Django** framework, the system allows users to browse various grocery items, add them to a virtual shopping cart, and place orders securely. 

The primary goal of this project is to simplify the grocery shopping process for local consumers by providing a user-friendly interface and reliable backend processing. Key features include a secure login system with **OTP verification (Twilio)**, social authentication via Google, a dynamic cart with coupon logic, and an integrated **Razorpay** payment gateway for digital transactions. Additionally, a **Rule-Based Customer Support Chatbot** is implemented to assist users with common queries such as order tracking and product availability.

The system utilizes **SQLite** as the database for storing user, product, and order information. The frontend is built using **HTML, CSS, JavaScript, and Bootstrap**, ensuring a responsive design that works across different devices. The project demonstrates a practical implementation of the **MVT (Model-View-Template)** architecture, focusing on security, performance, and user experience.

---

## **2. INTRODUCTION**

### **2.1 Overview**
In the current digital era, the demand for online services has increased significantly. Grocery shopping, being an essential daily activity, has seen a shift from traditional physical stores to digital platforms. **GRODIUR** is a web application developed to bridge the gap between local grocery retailers and customers by providing a structured and secure online marketplace.

### **2.2 Objectives**
* To develop a functional online platform for grocery shopping.
* To implement a secure authentication system using Django's built-in auth and mobile OTP.
* To provide an easy-to-use shopping cart and checkout process.
* To integrate a reliable payment gateway for online transactions.
* To provide an automated support system using a rule-based chatbot.
* To allow administrators to manage products, categories, and orders effectively.

### **2.3 Scope of the Project**
The scope of this project includes the development of both the customer-facing website and the administrative backend. Customers can register, verify their accounts, browse products, manage their cart, and track orders. Administrators can add/update products, manage stock availability, and process customer orders. The project is designed to be hosted on platforms like **PythonAnywhere** for public access.

### **2.4 Existing System vs Proposed System**
* **Existing System:** Many local stores still rely on manual billing or basic phone-based orders. Customers often face issues like lack of price transparency, time consumption, and manual tracking of orders.
* **Proposed System:** **GRODIUR** offers a transparent, automated, and secure alternative. It provides real-time stock visibility, automated price calculations, digital payment options, and instant order tracking through a rule-based chatbot.

---

## **3. LITERATURE SURVEY**

### **3.1 Study of Existing Systems**
Online grocery giants like BigBasket and Amazon Fresh have set high standards for digital retail. However, for small to medium-scale retailers, these systems can be overly complex or expensive to integrate. Our research focused on creating a balanced system that provides essential e-commerce features (Cart, Payments, Tracking) without the overhead of enterprise-level complexity. We analyzed various Django-based e-commerce patterns to implement a robust order lifecycle.

### **3.2 Feasibility Study**
* **Technical Feasibility:** Python and Django are well-documented and widely supported. Hosting on PythonAnywhere is a cost-effective solution for students and small projects.
* **Operational Feasibility:** The system is designed to be intuitive for users with basic internet knowledge. The admin panel is straightforward for store owners.
* **Economic Feasibility:** Using open-source technologies like Django and SQLite keeps the development cost at a minimum.

---

## **4. SYSTEM SPECIFICATION**

### **4.1 Hardware Requirements**
* **Processor:** Dual Core 2.0 GHz or higher.
* **RAM:** 4 GB minimum.
* **Hard Disk:** 20 GB of free space.
* **Internet Connection:** Required for API calls (Razorpay, Twilio, Google OAuth).

### **4.2 Software Requirements**
* **Operating System:** Windows 10/11 or Linux.
* **Web Browser:** Chrome, Firefox, or Safari.
* **Languages:** Python 3.10+, HTML5, CSS3, JavaScript.
* **Framework:** Django 5.x.
* **Database:** SQLite3.
* **Tools:** VS Code, Git, PythonAnywhere.

---

## **5. TECHNOLOGIES USED**

* **Django:** A high-level Python web framework that encourages rapid development and clean design. It follows the MVT architecture.
* **Bootstrap 5:** A popular CSS framework used for building responsive and mobile-first websites.
* **SQLite:** A lightweight, disk-based database that doesn't require a separate server process.
* **Razorpay:** A payment gateway that allows businesses to accept, process, and disburse payments.
* **Twilio:** Used for sending SMS-based OTPs to verify user phone numbers.
* **WhiteNoise:** Allows Django to serve its own static files in production environments.

---

## **6. SYSTEM DESIGN**

### **6.1 Data Flow Diagrams (DFD)**
* **Level 0 (Context Diagram):** Shows the overall system where the User and Admin interact with the Grocery System.
* **Level 1 DFD:** Breaks down the system into modules like Login, Product Browsing, Cart Management, and Order Processing.
* **Level 2 DFD:** Provides detailed flow of data within the Order and Payment modules.

### **6.2 Entity Relationship Diagram (ERD)**
The ER diagram for **GRODIUR** includes the following key entities:
* **User:** Stores basic information and links to a UserProfile.
* **Product:** Contains details like name, price, stock, and image.
* **Category:** Groups products together.
* **Cart:** Links a User to their selected CartItems.
* **Order:** Stores the final purchase details and payment status.
* **Review:** Stores user feedback for specific products.

### **6.3 UML Diagrams**
* **Use Case Diagram:** Defines the interactions between the Customer (browse, buy, track) and the Admin (manage products, view orders).
* **Sequence Diagram:** Illustrates the step-by-step process of placing an order, from adding to cart to payment verification.
* **Class Diagram:** Shows the structure of the system by illustrating the classes (Models) and their relationships.

### **6.4 Database Schema**
The database is structured to ensure data integrity. Relationships are maintained using Foreign Keys. For example, a `CartItem` refers to a `Product` and a `Cart`. An `OrderItem` refers to an `Order` and a `Product`.

---

## **7. MODULE DESCRIPTION**

### **7.1 Authentication & Profile**
This module handles user registration, login, and profile management. It uses Django's `auth` system and a custom `UserProfile` model. It supports:
* Traditional Email/Password login.
* **OTP Verification** via Twilio for mobile security.
* **Google OAuth** via `django-allauth`.

### **7.2 Product Management**
Managed primarily through the Django Admin panel. Products can be categorized and marked as "Available" or "Unavailable". The frontend dynamically renders products and greys out items that are out of stock.

### **7.3 Shopping Cart & Coupons**
Allows users to add multiple items and update quantities. The cart calculates MRP totals, discounts, and delivery fees. A coupon system is implemented to allow users to apply discount codes during checkout.

### **7.4 Order Processing & Payments**
When a user clicks "Checkout", an order is created with a "Pending" status. 
* **Razorpay Integration:** Facilitates online payments. The system verifies the payment signature on the backend before marking an order as "Paid".
* **Order History:** Users can view their previous orders and download invoices.

### **7.5 Rule-Based Customer Support Chatbot**
An integrated support tool that uses **regex and keyword matching** to respond to user queries. 
* It can track orders if a valid Order ID is provided.
* It answers FAQs about delivery, refunds, and search for products.
* It provides a simple conversational interface for common user issues.

---

## **8. TESTING**

### **8.1 Test Plan**
Testing was conducted to ensure all modules work correctly under different scenarios. We focused on Unit Testing, Integration Testing, and User Interface (UI) Testing.

### **8.2 Test Cases**

| Test ID | Module | Scenario | Expected Result | Result |
| :--- | :--- | :--- | :--- | :--- |
| T01 | Auth | Login with wrong password | Error message: "Invalid credentials" | Pass |
| T02 | OTP | Entering expired OTP | Error message: "OTP expired" | Pass |
| T03 | Cart | Add out-of-stock item | Button disabled or error shown | Pass |
| T04 | Payment | Successful Razorpay payment | Order status changed to "Paid" | Pass |
| T05 | Chatbot | Ask to track valid Order ID | Returns current order status | Pass |
| T06 | Coupons | Apply invalid coupon code | Error: "Coupon not found" | Pass |

---

## **9. CONCLUSION AND FUTURE SCOPE**

### **9.1 Conclusion**
The **GRODIUR** online grocery system successfully provides a practical solution for modern retail. By using Django, we built a secure and functional platform that handles everything from user authentication to complex order flows. The project meets all the requirements of a final-year BCA project, focusing on real-world usability and technical accuracy.

### **9.2 Future Scope**
* **Mobile Application:** Developing an Android/iOS app using React Native or Flutter.
* **Real-time Chat:** Upgrading the rule-based chatbot to a live chat system with human support.
* **Multiple Sellers:** Extending the system to allow multiple grocery vendors to list their products.
* **Notification System:** Implementing email and browser-based push notifications for order updates.

---

## **10. BIBLIOGRAPHY**

1.  **Django Documentation:** https://docs.djangoproject.com/en/stable/
2.  **Bootstrap Framework:** https://getbootstrap.com/
3.  **Python Official Docs:** https://docs.python.org/3/
4.  **Razorpay API Reference:** https://razorpay.com/docs/
5.  **Twilio API Docs:** https://www.twilio.com/docs/
6.  **"Two Scoops of Django"** by Audrey Roy Greenfeld and Daniel Roy Greenfeld.

---

## **11. APPENDIX - VIVA QUESTIONS**

**Q1: What is MVT in Django?**  
**A:** MVT stands for Model-View-Template. The Model handles data, the View handles business logic and requests, and the Template handles the presentation (HTML).

**Q2: How did you implement OTP?**  
**A:** We used the Twilio API to send a 6-digit random code to the user's mobile number. The code is stored in the database with an expiration time and verified when the user enters it.

**Q3: How is the chatbot implemented?**  
**A:** It is a **rule-based chatbot** that uses Python's `re` (regular expression) module. It looks for specific patterns (like Order IDs) or keywords (like "track", "refund") and returns predefined responses or fetches data from the database.

**Q4: Is SQLite suitable for production?**  
**A:** For small to medium projects with low traffic, SQLite is fine. For larger applications with many concurrent users, we would upgrade to PostgreSQL or MySQL.

**Q5: How does Razorpay verify payments?**  
**A:** After a payment, Razorpay returns a `payment_id`, `order_id`, and `signature`. We use our secret key to verify the signature on the backend to ensure the payment is authentic.

---
**End of Project Report**
