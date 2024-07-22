# FootballManager 2024

FootballManager 2024 is a web-based football management game built with Django where users can register, select their team, choose
players, and compete in a tournament against computer-controlled teams. The game includes user vs. user functionality
for future expansion.
</br>
note: pc-platform.
## Table of Contents

- [Installation](#installation)
- [Features](#features)
- [Usage](#usage)
- [Views](#views)
    - [User Registration](#user-registration)
    - [Team Selection](#team-selection)
    - [Player Selection](#player-selection)
    - [Tournament Simulation](#tournament-simulation)
    - [User vs. User Match](#user-vs-user-match)
- [Models](#models)
- [Simulation Logic](#simulation-logic)
- [Future Enhancements](#future-enhancements)
- [Admin Page and Version Control](#Admin-Page-and-Version-Control)
- [Packages to be installed and os](#Packages-to-be-installed-and-os )


## Installation

1. Clone the repository:

  
(https://github.com/NotL3d/footballManager.git)

## Features

- User registration and authentication
- Team selection
- Player selection with positional constraints
- Tournament simulation with user vs. computer matches
- Display of match results and tournament progression

## Usage

1. Register an account and log in.
2. Select a team to manage.
3. Choose 11 players for your team, adhering to positional constraints.
4. Simulate a match against a computer-controlled team.
5. View the results and progress through the tournament.

## Views

### User Registration

- **URL**: `/register/`
- **Description**: Register a new user account.
- **Template**: `register.html`

### Team Selection

- **URL**: `/select_team/`
- **Description**: Select a team to manage.
- **Template**: `select_team.html`

### Player Selection

- **URL**: `/select_players/`
- **Description**: Choose 11 players for your team.
- **Template**: `select_players.html`

### Tournament Simulation

- **URL**: `/simulate_tournament/`
- **Description**: Simulate matches against computer teams and progress through the tournament.
- **Template**: `tournament_result.html`

### User vs. User Match

- **URL**: `/select_opponent/` and `/simulate_user_vs_user/<opponent_id>/`
- **Description**: Select an opponent and simulate a match between user teams (future enhancement).
- **Template**: `select_opponent.html`, `match_result.html`

## Models

### CustomUserModel

- Extends `AbstractUser`
- Additional fields: `gender`, `birth_day`, `wins`, `losses`

### Team

- Stores team information

### ChoseTeamModel

- Stores the user’s chosen team

### Player

- Stores player information, including attributes and team

### SelectedPlayer

- Stores the players selected by the user for their team

## Simulation Logic

### simulate_game

A function to simulate the outcome of a match between two teams based on player attributes and positional correctness.

### get_random_computer_team

A function to randomly select a computer-controlled team from the database.

### simulate_tournament

A function to simulate a tournament, where the user’s team competes against computer-controlled teams. The tournament
progresses in rounds until a winner is determined.

## Future Enhancements

- Implement user vs. user matches.
- Add more detailed player statistics and history.
- Create a more interactive and dynamic user interface.
## Admin Page and Version Control

The Django admin interface is used to manage the models in FootballManager 2024. This includes creating, updating, and deleting players, teams, and user data.

### Accessing the Admin Page

1. Make sure you have created a superuser as described in the [Installation](#installation) section.
2. Navigate to the admin page at `/admin/` and log in with your superuser credentials.

### Managing Models in the Admin Page

#### Players

- **Create Player**: Add new players to the database.
- **Edit Player**: Update player attributes, including name, position, and team.
- **Delete Player**: Remove players from the database.

#### Teams

- **Create Team**: Add new teams to the database.
- **Edit Team**: Update team information.
- **Delete Team**: Remove teams from the database.

#### Users

- **Edit User**: Update user details, including wins and losses.
- **Delete User**: Remove users from the database.





## Packages to be installed and os

- asgiref              3.8.1
- asgiref              3.8.1
- diff-match-patch     20230430
- Django               5.0.7
- django-import-export 4.1.1
- pip                  23.2.1
- python-dotenv        1.0.1
- sqlparse             0.5.0
- tablib               3.5.0
- tzdata               2024.1
-python version       3.12.0
- OS VERSION (WINDOWS 10 Education)    10.0.190045  

