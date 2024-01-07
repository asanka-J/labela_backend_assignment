**Label A Backend Assignment**

**Project Overview**

Backend solution for a company specialised in car parts wants to modernise their company, and start selling their parts online. 

**Running the Project**

*Clone the Repository*

- git clone https://github.com/asanka-J/labela_backend_assignment.git
- cd labela_backend_assignment

*Build and Run Docker Compose*

- sudo docker-compose up -d --build

*Applying Initial Configurations and Running Migrations*

- docker-compose exec web python manage.py init_project
- init_project creates accounts for the backend admin and a guest user. You can use the following credentials to test the application

-- Admin Account:

    Username: admin Password: demo@123
-- Guest Account:

    Username: demo_guest Password: demo@123
Feel free to log in using these credentials to test the functionality and access various features of the application.


*Accessing the Application*

Open your web browser and navigate to http://127.0.0.1:8000

**Testing**

To run the provided test cases for the API endpoints, execute:

- python manage.py test api

**Planned Next Steps**

- **Cart Ownership Transition:** Implement logic for transitioning cart ownership upon guest registration.
- **Configuration Setup:** Establish separate configurations for production, development, and local environments.
- **User Registration and Authentication:** Implement user registration and authentication functionalities.
- **Frontend Integration:** Integrate the backend API with the frontend developed by the agency.

**Sample API Postman Collection**

Find a collection of sample API requests in `sample_api_collection.json` file within the repository. Use Postman to import and explore these sample requests.

**Bonus Points Achieved**

- RESTful API implementation
- Utilization of Django ORM
- Docker setup included for PostgreSQL
 