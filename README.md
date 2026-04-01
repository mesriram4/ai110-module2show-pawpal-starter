# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info *
- Let a user add/edit tasks (duration + priority at minimum) *
- Generate a daily schedule/plan based on constraints and priorities *
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started 

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.


### Smarter Scheduling 

+ Some updates have been made to increase the scheduling efficiency of this app: For starters, the program now creates a list of tasks assigned based on pet, completion status, priority, and time slot (if provided), otherwise automatically assigned. 
+ In main.py, the program includes several examples of an owner, pets, and tasks being assigned based on tasks assigned to pet, priority, and time slot if assigned. Main.py allows for users to add additional tasks other than the examples included in main.py, and the program returns a list of tasks based on the filters and sorting criteria previously described. 
+ All additional features were linked with features within app.py. Data inputted is saved through st.session(); both pawpal_system and app.py are linked. 