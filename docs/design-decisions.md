# CampusFlow — Design Decisions

## 1. Project Overview

CampusFlow is a command-line helpdesk application written in Python.

It helps a school manage support tickets submitted by students or staff.
Each ticket contains information such as its title, category, urgency,
number of affected users, priority, status, and assigned staff member.

The application allows users to create tickets, view tickets, assign
tickets to staff, update ticket statuses, view the work queue, and
generate reports.

## 2. Why I Used Python

I chose Python because its syntax is readable and easy to understand.

Python also provides built-in modules such as `json`, `pathlib`, and
`unittest`. These modules allow me to save data, manage file paths,
and test the application without installing external packages.

## 3. Why I Separated the Code into Modules

I separated the application into different files so that each file
has a specific responsibility.

- `tickets.py`: Creates tickets, validates ticket information,
  calculates priorities, and retrieves tickets.
- `workflow.py`: Assigns tickets, manages status changes, and creates
  the work queue.
- `storage.py`: Saves tickets to a JSON file and loads them when
  the application starts.
- `reports.py`: Generates summaries of ticket statuses and priorities.
- `main.py`: Provides the command-line menu and connects the different
  parts of the application.

This structure makes the code easier to read, test, maintain, and debug.

## 4. Ticket Identification

Each ticket receives a unique ID, such as `T001`, `T002`, or `T003`.

The ID helps users identify and retrieve individual tickets.

The application generates IDs based on the existing tickets so that
new tickets do not reuse an existing ID.

## 5. Ticket Priority

Ticket priority is calculated automatically using urgency and the
number of affected users.

The priority rules are:

- Critical: Urgency is high and at least 10 users are affected.
- High: Urgency is high, or at least 10 users are affected.
- Medium: Urgency is medium, or at least 3 users are affected.
- Low: None of the higher-priority rules apply.

These rules help the helpdesk identify which tickets need attention first.

## 6. Ticket Status and Workflow

Tickets move through the following workflow:

`open → in_progress → resolved`

A ticket must be assigned to a staff member before work can begin.

A ticket cannot skip directly from `open` to `resolved`.

Resolved tickets cannot be changed normally. They must first be reopened
before further work is performed.

These rules help prevent invalid workflow changes.

## 7. Work Queue Ordering

The work queue displays unresolved tickets in priority order:

1. Critical
2. High
3. Medium
4. Low

Tickets with the same priority are ordered by their numeric ticket ID.

Resolved tickets are excluded from the work queue because they no
longer require active work.

## 8. Data Storage

I used JSON to store ticket information in a file.

JSON is readable by humans and can be handled using Python's built-in
`json` module.

The application loads saved tickets when it starts and saves changes
so that ticket information can be used again later.

If the saved JSON file is malformed, the application reports an error
instead of silently treating the corrupted file as valid data.

## 9. Input Validation

The application validates important ticket information before
accepting it.

For example:

- Ticket titles cannot be blank.
- Categories must be Network, Hardware, Software, or Other.
- Urgency must be low, medium, or high.
- The number of affected users must be a positive integer.
- Boolean values are not accepted as affected-user counts.

Validation helps prevent incorrect information from entering the system.

## 10. Automated Testing

I used Python's `unittest` module to test the application's behaviour.

The tests cover ticket creation, priority calculation, workflow rules,
data storage, and report generation.

Automated tests help identify problems and make it safer to change
the application in the future.

## 11. Limitations and Possible Improvements

Possible future improvements include:

- Adding user authentication.
- Supporting multiple staff accounts.
- Creating a graphical user interface.
- Adding ticket search and filtering.
- Recording a history of ticket changes.
- Improving report presentation.

These improvements could make CampusFlow more useful for a real
school helpdesk.