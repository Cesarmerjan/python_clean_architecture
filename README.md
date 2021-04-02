# Working in progress!

# Clean Architecture with Python

The purpose of this repository is to make a simple example of the implementation of a python project with Clean Architecture

## Important
If your application is a CRUD do not use this methodology
The application of this repository is a CRUD.
It could have been implemented with another architectural model like MVC.


Feel free to indicate improvements. The idea is to implement a repository that serves as an example of using Clean Architecture with Python.

## References
The main references of this application are:
Clean Architecture: A Craftsman's Guide to Software Structure and Design.
Robert C. Martin
Kevlin Henney

Architecture Patterns with Python: Enabling Test-Driven Development, Domain-Driven Design, and Event-Driven Microservices
Bob Gregory
Harry J.W.Percival

## Clean Architecture
### Diagram
![Alt text](images/clean_architecture_diagram.jpg?raw=true "Clean Architecture Diagram")
### Flow Chart
![Alt text](images/clean_architecture_flow_chart.png?raw=true "Clean Architecture Flow Chart.png")


# Project

## Functional Requirements
The user must be able to register, log in, log out and make comments.
Comments made should contain information about when it was made and by whom it was made.
Logged users must be able to edit or delete comments made by them previously.
Non-logged users can view comments.

## Business Rule
A user can only delete, edit or make comments when logged in.
A user can only delete or edit his own comment.


## Non-functional Requirements
The database must be implemented in Postgres.
The system must be installable.
It must be possible to interact with the system via API or via CLI.


## Usa Case Diagram
![Alt text](images/class_diagram.png?raw=true "Class Diagram")


## Class Diagram
![Alt text](images/use_case.png?raw=true "Use Case Diagram")


## ValueObjects
Comment

## Entities
User

## Layers Responsibility
### Domain
Responsible for representing the entities or object values of the system
### Use Case
#### Service
Responsible for the business rules
#### Interactor
Responsible for managing interaction with the business rules (service)
### Serializer
Responsible for defining the data structure of the request and the payload of the response
### Adapters (Port & Adapters)
Responsible for communication with external elements 
#### Drivers
Responsible for communication between the application and others "devices"
#### ORM
Responsible for mapping objects with database tables
#### Repository
Responsible for data access logic 
#### Unit of Work
Responsible for the atomicity (transactions, concurrency, commit and rollback)
#### Response
Responsible for defining the response structure of the application 
#### Controllers
Responsible for managing requests and responses flow
### Exceptions
Responsible for custom exceptions
### Utils
Responsible for support modules fo the system
### Views
Responsible for the user interface

