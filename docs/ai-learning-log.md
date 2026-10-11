# CampusFlow — AI Learning Log

## 1. Introduction

I used AI as a learning assistant while developing CampusFlow.

My goal was not only to complete the project but also to understand
how the different parts of the application work.

I used AI to explain programming concepts, help me understand errors,
suggest possible solutions, and improve my understanding of testing
and code organization.

## 2. Understanding the Project Structure

### What I wanted to learn

I wanted to understand how to divide a Python project into smaller
files instead of placing all the code inside one large file.

### How AI helped

AI explained the purpose of separating ticket management, workflow,
storage, and reporting into different modules.

### What I learned

I learned that separating code by responsibility makes a project
easier to understand, test, maintain, and debug.

I also learned that Python files can import functions from other
files in the same project.

### How I applied the learning

I organized CampusFlow into modules so that each module handles
a particular part of the application.

## 3. Understanding Ticket Priority

### What I wanted to learn

I wanted to understand how ticket urgency and the number of affected
users could determine a ticket's priority.

### How AI helped

AI helped explain how to turn the priority rules into conditional
logic.

### What I learned

I learned that the order of conditions matters.

For example, a ticket with high urgency affecting at least 10 users
must be classified as critical before checking the less urgent rules.

### How I applied the learning

I used a priority-calculation function to determine whether each
ticket should be critical, high, medium, or low priority.

I also used tests to check different combinations of urgency and
affected users.

## 4. Understanding Ticket Workflow

### What I wanted to learn

I wanted to understand how to prevent tickets from moving through
invalid statuses.

### How AI helped

AI helped explain how conditional statements can check a ticket's
current status before allowing a status change.

### What I learned

I learned that an application should enforce its rules rather than
accept every action requested by a user.

For example, an unassigned ticket should not move into the
in-progress status.

### How I applied the learning

I implemented workflow checks to prevent invalid status changes
and require tickets to be assigned before work begins.

## 5. Understanding JSON Storage

### What I wanted to learn

I wanted ticket information to remain available after the program
was closed and started again.

### How AI helped

AI explained how JSON can represent Python data and how a program
can read from and write to a JSON file.

### What I learned

I learned the difference between data held in memory and data saved
in a file.

I also learned why malformed JSON should produce a clear error.

### How I applied the learning

I used Python's `json` module to save tickets and load them again.

I tested the storage functions to check that data could be saved,
loaded, and handled when the file contained invalid JSON.

## 6. Understanding Automated Testing

### What I wanted to learn

I wanted to check that the application followed its requirements
instead of relying only on manually running the program.

### How AI helped

AI helped me understand how unit tests can check individual
functions and expected behaviour.

### What I learned

I learned that tests can verify correct results and check that
invalid input or actions are rejected.

### How I applied the learning

I created tests for ticket creation, priority calculation, workflow
rules, JSON storage, and report generation.

I used Python's `unittest` framework to run the tests.

## 7. How I Checked AI Suggestions

I treated AI suggestions as material to understand and verify,
not as automatically correct answers.

I reviewed the suggested code, compared it with the project
requirements, and used tests to check important behaviour.

When an error occurred, I used the error message to help identify
which part of the code needed attention.

## 8. What I Learned Overall

Developing CampusFlow helped me understand how a Python application
can be divided into modules and how those modules work together.

I improved my understanding of functions, conditional statements,
input validation, file handling, exceptions, and automated testing.

I also learned that completing a project involves more than writing
code. The application must follow its requirements, handle errors,
and be tested properly.

## 9. What I Want to Improve

In future projects, I want to become more confident at designing
programs independently, debugging errors, writing tests, and
explaining why I chose a particular solution.

I also want to practise implementing features before asking AI for
help so that I can strengthen my problem-solving skills.