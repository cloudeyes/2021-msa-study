## Preface

- Managing Complexity, Solving Business Problems
- Why Python?
- TDD, DDD, and Event-Driven Architecture
- Who Should Read This Book
- A Brief Overview of What You’ll Learn
    - Part I, Building an Architecture to Support Domain Modeling
    - Part II, Event-Driven Architecture
    - Addtional Content
- Example Code and Coding Along
- License
- Conventions Used in This Book
- O’Reilly Online Learning
- How to Contact O’Reilly
- Acknowledgments

## Introduction

- Why Do Our Designs Go Wrong?
- Encapsulation and Abstractions
- Layering
- The Dependency Inversion Principle
- A Place for All Our Business Logic: The Domain Model

## I. Building an Architecture to Support Domain Modeling

### 1. Domain Modeling

- What Is a Domain Model?
- Exploring the Domain Language
- Unit Testing Domain Models
    - Dataclasses Are Great for Value Objects
    - Value Objects and Entities
- Not Everything Has to Be an Object: A Domain Service Function
    - Python’s Magic Methods Let Us Use Our Models with Idiomatic Python
    - Exceptions Can Express Domain Concepts Too

### 2. Repository Pattern

- Persisting Our Domain Model
- Some Pseudocode: What Are We Going to Need?
- Applying the DIP to Data Access
- Reminder: Our Model
    - The “Normal” ORM Way: Model Depends on ORM
    - Inverting the Dependency: ORM Depends on Model
- Introducing the Repository Pattern
    - The Repository in the Abstract
    - What Is the Trade-Off?
- Building a Fake Repository for Tests Is Now Trivial!
- What Is a Port and What Is an Adapter, in Python?
- Wrap-Up

### 3. A Brief Interlude: On Coupling and Abstractions

- Abstracting State Aids Testability
- Choosing the Right Abstraction(s)
- Implementing Our Chosen Abstractions
    - Testing Edge to Edge with Fakes and Dependency Injection
    - Why Not Just Patch It Out?
- Wrap-Up

### 4. Our First Use Case: Flask API and Service Layer

- Connecting Our Application to the Real World
- A First End-to-End Test
- The Straightforward Implementation
- Error Conditions That Require Database Checks
- Introducing a Service Layer, and Using FakeRepository to Unit Test It
    - A Typical Service Function
- Why Is Everything Called a Service?
- Putting Things in Folders to See Where It All Belongs
- Wrap-Up
    - The DIP in Action

### 5. TDD in High Gear and Low Gear

- How Is Our Test Pyramid Looking?
- Should Domain Layer Tests Move to the Service Layer?
- On Deciding What Kind of Tests to Write
- High and Low Gear
- Fully Decoupling the Service-Layer Tests from the Domain
    - Mitigation: Keep All Domain Dependencies in Fixture Functions
    - Adding a Missing Service
- Carrying the Improvement Through to the E2E Tests
- Wrap-Up

### 6. Unit of Work Pattern

- The Unit of Work Collaborates with the Repository
- Test-Driving a UoW with Integration Tests
- Unit of Work and Its Context Manager
    - The Real Unit of Work Uses SQLAlchemy Sessions
    - Fake Unit of Work for Testing
- Using the UoW in the Service Layer
- Explicit Tests for Commit/Rollback Behavior
- Explicit Versus Implicit Commits
- Examples: Using UoW to Group Multiple Operations into an Atomic Unit
    - Example 1: Reallocate
    - Example 2: Change Batch Quantity
- Tidying Up the Integration Tests
- Wrap-Up

### 7. Aggregates and Consistency Boundaries

- Why Not Just Run Everything in a Spreadsheet?
- Invariants, Constraints, and Consistency
    - Invariants, Concurrency, and Locks
- What Is an Aggregate?
- Choosing an Aggregate
- One Aggregate = One Repository
- What About Performance?
- Optimistic Concurrency with Version Numbers
    - Implementation Options for Version Numbers
- Testing for Our Data Integrity Rules
    - Enforcing Concurrency Rules by Using Database Transaction Isolation Levels
    - Pessimistic Concurrency Control Example: SELECT FOR UPDATE
- Wrap-Up
- Part I Recap

## II. Event-Driven Architecture

### 8. Events and the Message Bus

- Avoiding Making a Mess
    - First, Let’s Avoid Making a Mess of Our Web Controllers
    - And Let’s Not Make a Mess of Our Model Either
    - Or the Service Layer!
- Single Responsibility Principle
- All Aboard the Message Bus!
    - The Model Records Events
    - Events Are Simple Dataclasses
    - The Model Raises Events
    - The Message Bus Maps Events to Handlers
- Option 1: The Service Layer Takes Events from the Model and Puts Them on the Message Bus
- Option 2: The Service Layer Raises Its Own Events
- Option 3: The UoW Publishes Events to the Message Bus
- Wrap-Up

### 9. Going to Town on the Message Bus

- A New Requirement Leads Us to a New Architecture
    - Imagining an Architecture Change: Everything Will Be an Event Handler
- Refactoring Service Functions to Message Handlers
    - The Message Bus Now Collects Events from the UoW
    - Our Tests Are All Written in Terms of Events Too
    - A Temporary Ugly Hack: The Message Bus Has to Return Results
    - Modifying Our API to Work with Events
- Implementing Our New Requirement
    - Our New Event
- Test-Driving a New Handler
    - Implementation
    - A New Method on the Domain Model
- Optionally: Unit Testing Event Handlers in Isolation with a Fake Message Bus
- Wrap-Up
    - What Have We Achieved?
    - Why Have We Achieved?

### 10. Commands and Command Handler

- Commands and Events
- Differences in Exception Handling
- Discussion: Events, Commands, and Error Handling
- Recovering from Errors Synchronously
- Wrap-Up

### 11. Event-Driven Architecture: Using Events to Integrate Microservices

- Distributed Ball of Mud, and Thinking in Nouns
- Error Handling in Distributed Systems
- The Alternative: Temporal Decoupling Using Asynchronous Messaging
- Using a Redis Pub/Sub Channel for Integration
- Test-Driving It All Using an End-to-End Test
    - Redis Is Another Thin Adapter Around Our Message Bus
    - Our New Outgoing Event
- Internal Versus External Events
- Wrap-Up

### 12. Command-Query Responsibility Segregation (CQRS)

- Domain Models Are for Writing
- Most Users Aren’t Going to Buy Your Furniture
- Post/Redirect/Get and CQS
- Hold On to Your Lunch, Folks
- Testing CQRS Views
- “Obvious” Alternative 1: Using the Existing Repository
- Your Domain Model Is Not Optimized for Read Operations
- “Obvious” Alternative 2: Using the ORM
- SELECT N+1 and Other Performance Considerations
- Time to Completely Jump the Shark
    - Updating a Read Model Table Using an Event Handler
- Changing Our Read Model Implementation Is Easy
- Wrap-Up

### 13. Dependency Injection (and Bootstrapping)

- Implicit Versus Explicit Dependencies
- Aren’t Explicit Dependencies Totally Weird and Java-y?
- Preparing Handlers: Manual DI with Closures and Partials
- An Alternative Using Classes
- A Bootstrap Script
- Message Bus Is Given Handlers at Runtime
- Using Bootstrap in Our Entrypoints
- Initializing DI in Our Tests
- Building an Adapter “Properly”: A Worked Example
    - Define the Abstract and Concrete Implementations
    - Make a Fake Version for Your Tests
    - Figure Out How to Integration Test the Real Thing
- Wrap-Up

### Epilogue

- What Now?
- How Do I Get There from Here?
- Separating Entangled Responsibilities
- Identifying Aggregates and Bounded Contexts
- An Event-Driven Approach to Go to Microservices via Strangler Pattern
- Convincing Your Stakeholders to Try Something New
- Questions Our Tech Reviewers Asked That We Couldn’t Work into Prose
- Footguns
- More Required Reading
- Wrap-Up

## A. Summary Diagram and Table

## B. A Template Project Structure
- Env Vars, 12-Factor, and Config, Inside and Outside Containers
- Config.py
- Docker-Compose and Containers Config
- Installing Your Source as a Package
- Dockerfile
- Tests
- Wrap-Up

## C. Swapping Out the Infrastructure: Do Everything with CSVs
- Implementing a Repository and Unit of Work for CSVs

## D. Repository and Unit of Work Patterns with Django
- Repository Pattern with Django
- Custom Methods on Django ORM Classes to Translate to/from Our Domain Model
- Unit of Work Pattern with Django
- API: Django Views Are Adapters
- Why Was This All So Hard?
- What to Do If You Already Have Django
- Steps Along the Way

## E. Validation
- What Is Validation, Anyway?
- Validating Syntax
- Postel’s Law and the Tolerant Reader Pattern
- Validating at the Edge
- Validating Semantics
- Validating Pragmatics

## Index
