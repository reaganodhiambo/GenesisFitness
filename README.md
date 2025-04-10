# **Customer Management System for Genesis Fitness**

## **Project Details**
- **Developer**: Loise Muthambei  
- **Reg. Number**: E35/2360/2021  
- **Supervisor**: Dr. Erick Araka  
- **Academic Year**: 2024/2025  
- **System Title**: Customer Management System for Genesis Fitness  

---

## **Overview**

This project is a **Customer Management System** tailored for Genesis Fitness. It is designed to optimize customer interactions, manage memberships, and improve operational efficiency. The system leverages **Django** for backend development, **Bootstrap** for frontend design, and **MySQL** for database management. It offers an intuitive interface for administrators and users, ensuring a smooth experience.

---

## **Technology Stack**
- **Backend**: Django  
- **Frontend**: Bootstrap  
- **Database**: MySQL  

---

## **Setup Guide**

### **Prerequisites**
Ensure the following are installed on your system:
- **Python** (version 3.10 or higher)

---

### **Backend Configuration**

1. **Navigate to the backend directory**:

2. **Create and activate a virtual environment** (optional but recommended):
    ```python
    python -m venv venv
    source venv/bin/activate
    ```
3. **Install dependencies**:
    ```python
    pip install -r requirements.txt
    ```
4. **Apply database migrations**:
    ```python
    python manage.py migrate
    ```
5. **Set up a superuser** for admin access:
    ```python
    python manage.py createsuperuser
    ```
6. **Start the development server**:
    ```python
    python manage.py runserver
    ```

---

## **System Access**

With the server running, access the system via your browser at:
    ```python
    http://localhost:8000
    ```

To access the admin interface, use:
    ```python
    http://localhost:8000/admin
    ```