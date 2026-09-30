# BrightPath

> A cloud-hosted education management platform built as the final capstone project for the **Cloud & DevOps Programme (CSDO8)**.

BrightPath is a multi-tier web application designed to support common education management workflows such as user authentication, course management, student enrolment, attendance tracking, grading, and role-based access control.

The project demonstrates the integration of **application development, containerisation, cloud deployment, CI/CD, security, monitoring, and performance testing** using Microsoft Azure and modern DevOps practices.

---

# Project Scope

BrightPath was developed as an educational capstone project.

The project focuses on demonstrating:

**application development + cloud architecture + containerisation + DevOps + security + monitoring + scalability concepts**

rather than implementing every feature expected from a commercial learning management system.

---

# Team Project

BrightPath was developed as part of the **CSDO8 Cloud & DevOps Final Capstone Project**.

Project responsibilities were divided across areas including:

- frontend development;
- backend development;
- database development;
- cloud infrastructure;
- application security;
- deployment;
- CI/CD;
- testing and monitoring.

---

## Project Overview

BrightPath was developed as a team capstone project to demonstrate how a traditional web application can be designed, containerised, deployed, secured, monitored, and tested in a cloud environment.

The application follows a separated frontend, backend, and database architecture.

```text
User
 │
 ▼
Frontend Web Application
 │
 │ HTTPS / REST API
 ▼
Backend API
 │
 ▼
Azure SQL Database
```

The deployed environment expands this architecture with containerisation, CI/CD, monitoring, and Azure cloud services.

```text
                        GitHub
                           │
                           ▼
                    GitHub Actions
                           │
                    Build Containers
                           │
                           ▼
                Azure Container Registry
                    ┌──────┴──────┐
                    │             │
                    ▼             ▼
             Frontend App    Backend App
                Service        Service
                    │             │
                    └──────┬──────┘
                           │
                           ▼
                   Azure SQL Database

                Monitoring / Telemetry
                           │
                           ▼
                Application Insights
```

---

# Key Features

BrightPath provides role-based functionality for different users within an education platform.

### Authentication and Authorisation

- User login and logout
- Session-based authentication
- Role-based access control
- Protected routes
- Authorisation for:
  - Students
  - Teachers
  - Administrators
  - Super Administrators

### Course Management

- Create courses
- Retrieve course information
- Update course details
- Assign teachers
- Assign classrooms
- Manage course status
- Validate teacher and classroom availability

### Student Enrolment

- Enrol students into courses
- Track enrolment status
- Prevent duplicate enrolments
- Associate students with courses using relational database records

### Attendance Management

- Record student attendance
- Perform bulk attendance submission
- Validate enrolments before attendance creation
- Prevent duplicate attendance records

### Grade Management

- Record student assessment results
- Associate grades with student enrolments
- Store assessment scores and feedback
- Support teacher-managed grading workflows

---

# Technology Stack

| Area                | Technology                                 |
| ------------------- | ------------------------------------------ |
| Frontend            | HTML / Web Frontend                        |
| Backend             | Python, Flask                              |
| API                 | REST                                       |
| Validation          | Pydantic                                   |
| ORM                 | SQLAlchemy / Flask-SQLAlchemy              |
| Database            | Microsoft Azure SQL                        |
| Database Driver     | pyODBC / ODBC Driver 18                    |
| Authentication      | Flask Session Authentication               |
| Application Server  | Gunicorn                                   |
| Containerisation    | Docker                                     |
| Container Registry  | Azure Container Registry                   |
| Cloud Hosting       | Azure App Service                          |
| CI/CD               | GitHub Actions                             |
| Monitoring          | Azure Application Insights / Azure Monitor |
| Performance Testing | Azure Load Testing                         |
| Version Control     | Git / GitHub                               |

---

# Cloud Architecture

The production-oriented BrightPath architecture uses Microsoft Azure services to separate application hosting, container storage, database services, monitoring, and deployment automation.

### Application Layer

The frontend and backend are deployed independently using separate **Azure App Services**.

This separation allows both application components to:

- be deployed independently;
- scale independently;
- use separate configuration settings;
- maintain clear application boundaries;
- use different runtime configurations if required.

The backend App Service hosts the Flask API using **Gunicorn** as the production WSGI server.

---

### Container Layer

Both application components are packaged as Docker container images.

```text
Source Code
     │
     ▼
GitHub Actions
     │
     ▼
Docker Build
     │
     ▼
Azure Container Registry
     │
     ├─────────────► Frontend App Service
     │
     └─────────────► Backend App Service
```

Azure Container Registry acts as the private container registry used by the deployed App Services.

---

### Database Layer

Application data is stored in **Microsoft Azure SQL Database**.

The backend communicates with Azure SQL through SQLAlchemy and the Microsoft ODBC Driver.

The application uses internal relational database identifiers while exposing separate business identifiers through the API where appropriate.

Examples include:

```text
course_id       → Internal database primary key
course_id_bus   → Business-facing course identifier

student_id      → Internal database primary key
student_id_bus  → Business-facing student identifier
```

This separates database implementation details from identifiers exposed to application users.

---

# Backend Architecture

The Flask backend follows a layered application structure.

```text
backend/
│
├── app/
│   ├── routes/
│   ├── services/
│   ├── schemas/
│   ├── utils/
│   ├── exceptions/
│   └── __init__.py
│
├── config.py
├── extensions.py
├── requirements.txt
└── run.py
```

The application separates responsibilities between different layers.

```text
HTTP Request
     │
     ▼
Route
     │
     ▼
Pydantic Validation
     │
     ▼
Service Layer
     │
     ▼
SQLAlchemy ORM
     │
     ▼
Azure SQL Database
```

### Routes

Routes handle:

- HTTP requests;
- authentication checks;
- authorisation checks;
- request validation;
- response formatting.

### Service Layer

The service layer contains application business logic such as:

- course validation;
- enrolment processing;
- attendance processing;
- grading;
- database queries;
- business rule enforcement.

### Schemas

Pydantic models provide request validation before data reaches the service layer.

This helps enforce predictable API input and reduces invalid data entering application logic.

---

# Database Design

BrightPath uses a relational database model containing entities including:

- Users
- Students
- Teachers
- Administrators
- Courses
- Classrooms
- Enrolments
- Attendance
- Grades

Relationships are represented using internal foreign keys.

---

# API Design

The backend API uses versioned REST endpoints.

Role-based decorators protect restricted endpoints.

Example:

```python
@login_required
@role_required("TEACHER")
```

This ensures users must both authenticate and possess the appropriate application role before accessing protected functionality.

---

# Containerisation

The backend application is packaged using Docker.

The backend image contains:

- Python runtime
- Flask application
- application dependencies
- Microsoft ODBC Driver
- Gunicorn
- Azure SQL connectivity dependencies

Gunicorn worker and thread settings were evaluated through load testing to identify a suitable concurrency configuration for the deployed App Service tier.

---

# CI/CD Pipeline

GitHub Actions provides automated container build and deployment workflows.

The CI/CD pipeline follows the general process:

```text
Developer Push
      │
      ▼
    GitHub
      │
      ▼
GitHub Actions
      │
      ├── Validate Application
      │
      ├── Build Container Image
      │
      ├── Tag Container Image
      │
      └── Push Image
      │
      ▼
Azure Container Registry
      │
      ▼
Azure App Service
```

Container images can be tagged using the Git commit SHA, providing traceability between deployed containers and source code revisions.

````

This provides a clear link between:

```text
Source Commit
     │
     ▼
Container Image
     │
     ▼
Deployment
````

---

# Configuration and Secrets

Application configuration is separated from source code using environment variables.

Sensitive information such as database credentials is **not committed into the repository**.

---

# Security

Security controls implemented within the project include:

### HTTPS

Azure App Service provides HTTPS access for the deployed application.

### Authentication

Users authenticate through the backend application.

### Role-Based Access Control

Application permissions are enforced using role-based decorators.

### Secret Management

Credentials and environment-specific configuration are kept outside the source repository.

### Database Isolation

The backend application provides the application-facing interface to the database rather than exposing database operations directly to frontend users.

### Input Validation

Pydantic schemas validate incoming API payloads before business logic is executed.

### Database Constraints

Database constraints and application validation help prevent:

- duplicate enrolments;
- invalid relationships;
- duplicate attendance records;
- invalid foreign-key references.

---

# Monitoring and Observability

Azure monitoring services are used to observe application behaviour after deployment.

Monitoring includes infrastructure-level metrics such as:

- CPU utilisation;
- memory utilisation;
- HTTP request behaviour;
- application response performance;
- App Service metrics.

Application-level telemetry can additionally be collected using **Application Insights** and OpenTelemetry instrumentation.

This provides visibility across two monitoring layers:

```text
Platform Monitoring
Azure App Service
       │
       ├── CPU
       ├── Memory
       ├── Requests
       └── Platform Metrics

Application Monitoring
Application Insights
       │
       ├── Requests
       ├── Dependencies
       ├── Exceptions
       └── Application Traces
```

---

# Performance and Load Testing

Azure Load Testing was used to evaluate the behaviour of the deployed backend under concurrent user load.

The tests investigated several aspects of application performance.

---

# Local Development

## Prerequisites

The following tools are required:

```text
Python 3.x
Docker
Git
ODBC Driver 18 for SQL Server
```

Create a Python virtual environment:

```bash
python -m venv .venv
```

Activate it:

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r backend/requirements.txt
```

Configure environment variables:

```bash
cp .env.example .env
```

Update the required values inside `.env`.

Run the backend:

```bash
python -m backend.run
```

---

# Deployment Workflow

The overall deployment workflow is:

```text
Local Development
       │
       ▼
Git Commit
       │
       ▼
GitHub Repository
       │
       ▼
GitHub Actions
       │
       ▼
Docker Build
       │
       ▼
Azure Container Registry
       │
       ▼
Azure App Service
       │
       ▼
Azure SQL Database
```

This provides a repeatable deployment process instead of manually copying application files to the production environment.

---

# Cloud & DevOps Concepts Demonstrated

The BrightPath project demonstrates practical implementation of several Cloud and DevOps concepts.

| Area                     | Implementation                       |
| ------------------------ | ------------------------------------ |
| Cloud Hosting            | Azure App Service                    |
| Managed Database         | Azure SQL Database                   |
| Containerisation         | Docker                               |
| Container Registry       | Azure Container Registry             |
| CI/CD                    | GitHub Actions                       |
| Infrastructure Security  | HTTPS, network/database restrictions |
| Application Security     | Authentication and RBAC              |
| Configuration Management | Environment variables                |
| Monitoring               | Azure Monitor / Application Insights |
| Performance Testing      | Azure Load Testing                   |
| Application Server       | Gunicorn                             |
| API Architecture         | Flask REST API                       |
| Validation               | Pydantic                             |
| ORM                      | SQLAlchemy                           |
| Version Control          | Git / GitHub                         |

---

# Key Learning Outcomes

Through the development of BrightPath, the project team gained practical experience in:

- designing a multi-tier cloud application;
- separating frontend, backend, and database responsibilities;
- building REST APIs with Flask;
- implementing relational database models;
- implementing authentication and role-based access control;
- validating API requests with Pydantic;
- containerising applications with Docker;
- configuring production Python applications with Gunicorn;
- storing container images in Azure Container Registry;
- deploying containers through Azure App Service;
- connecting cloud applications to Azure SQL;
- managing environment-specific configuration securely;
- implementing automated CI/CD pipelines with GitHub Actions;
- monitoring cloud-hosted applications;
- conducting load and performance tests;
- analysing latency, throughput, CPU, memory, and concurrency;
- investigating horizontal scaling behaviour.

---

# Production Improvements

The capstone implementation provides the foundation for a larger production architecture.

Potential future improvements include:

- Azure Key Vault for centralised secret management;
- Managed Identity for Azure service authentication;
- private endpoints for platform services;
- Virtual Network integration;
- Azure Private DNS Zones;
- Web Application Firewall protection;
- Azure Front Door or Application Gateway;
- autoscaling policies;
- automated database migrations;
- expanded automated unit and integration testing;
- structured application logging;
- distributed tracing;
- alerting and operational dashboards;
- Infrastructure as Code using Terraform or Bicep;
- deployment environments for development, staging, and production.

---

# Conclusion

BrightPath demonstrates the progression of an application from source code to a cloud-hosted, containerised system with automated deployment and operational monitoring.

The project brings together the complete application lifecycle:

```text
Design
  │
  ▼
Develop
  │
  ▼
Validate
  │
  ▼
Containerise
  │
  ▼
Build
  │
  ▼
Deploy
  │
  ▼
Secure
  │
  ▼
Monitor
  │
  ▼
Load Test
  │
  ▼
Scale
```

The result is a practical demonstration of how application development and Cloud & DevOps practices can be combined to deliver and operate a modern web application on Microsoft Azure.
