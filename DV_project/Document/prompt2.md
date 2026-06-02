You are a senior Dash/Plotly engineer and technical project planner.

Your task is to read the existing dashboard improvement plan and convert it into a clear implementation task plan divided into phases.

Do not implement any code changes yet. Only create a task plan.

## Inputs

Project root:

Visualization improvement plan:

Optional course/report documents, if needed:

## Objective

Create a Markdown task plan named:

`dashboard_improvement_tasks.md`

Place it in the project root, or in a docs/report folder if the project already has one.

The task plan must break down the improvement work into practical phases and implementation tasks that a coding agent can execute later.

## Important constraints

* Do not modify dashboard source code.
* Do not implement the tasks.
* Do not create new features beyond the scope of the improvement plan.
* Prioritize P0 and P1 items first.
* Treat P2 as “should improve if time allows”.
* Treat P3 / bonus items as optional only.
* Do not make map visualization, network graph, animation, or small multiples part of the required implementation unless the plan explicitly marks them as required.
* Each task must be small enough to implement and review independently.
* Each task must include affected files/components when possible.
* Each task must include acceptance criteria.
* Each task must include testing/check steps.
* If the plan is ambiguous, write the assumption clearly instead of guessing.

## What to inspect before creating tasks

Read:

1. Plan in document folder 
2. Project structure under DV_project
3. Existing page files, if available:

   * `pages/overview.py`
   * `pages/dominance.py`
   * `pages/upsets.py`
   * `pages/tournament.py`
4. Shared files, if available:

   * `src/theme.py`
   * `src/components.py`
   * `src/data.py`
   * `assets/styles.css`
   * `app.py`

Use the implementation details from the plan and verify file names/components against the actual project if possible.

## Required output structure

Create the file:

# Dashboard Improvement Implementation Tasks

## 1. Planning Summary

Summarize:

* project goal
* main dashboard story
* implementation objective
* priority strategy
* what is in scope
* what is out of scope

Clearly state:

* P0 = must fix before final submission
* P1 = important quality/storytelling improvements
* P2 = useful if time allows
* P3 = optional / bonus

## 2. Phase Overview

Create a table:

| Phase | Name | Goal | Priority level | Main files affected | Expected outcome |
| ----- | ---- | ---- | -------------- | ------------------- | ---------------- |

Use this phase structure unless the actual plan strongly suggests a better one:

### Phase 0 — Baseline verification and safety checks

Goal: confirm the current app runs before making changes.

### Phase 1 — Accessibility and shared visual style fixes

Goal: fix CVD-safe colors, shared palette, and styling issues that affect multiple pages.

### Phase 2 — Storytelling titles and insight cards

Goal: replace descriptive titles with action titles and add page-level insight cards.

### Phase 3 — Overview page improvements

Goal: improve expansion story with annotations, timeline fixes, and better hover/context.

### Phase 4 — Dominance page improvements

Goal: improve elite dominance story, continent encoding, chart titles, and table readability.

### Phase 5 — Upsets page improvements

Goal: improve scatter readability, upset colors, legend labels, top upset chart, and detail panel.

### Phase 6 — Tournament Detail page improvements

Goal: improve goals charts, GF vs GA scatter reference line, sorting, and 2022 storytelling.

### Phase 7 — Interaction and usability polish

Goal: add/reset filters, improve tooltip content, no-data guidance, and interaction clarity.

### Phase 8 — Final QA, screenshots, and report alignment

Goal: verify the dashboard, capture screenshots, and ensure every improvement supports the report.

### Phase 9 — Optional / bonus enhancements

Goal: list optional P3 ideas such as choropleth map, small multiples, animation, or index chart.

## 3. Detailed Tasks by Phase

For each phase, create tasks using this format:

### Phase X — [Phase name]

#### Task X.Y — [Task title]

**Priority:** P0 / P1 / P2 / P3
**Type:** Bugfix / Refactor / Visualization improvement / Storytelling / Accessibility / Interaction / QA
**Related plan item:** quote or summarize the relevant recommendation from `<PLAN_PATH>`
**Affected files/components:**

* file path
* function name, component id, or chart id if available

**Goal:**
Explain what this task should achieve.

**Implementation steps:**

1. Step 1
2. Step 2
3. Step 3

**Acceptance criteria:**

* Criterion 1
* Criterion 2
* Criterion 3

**Test/check steps:**

* Command to run if relevant, for example `python app.py`
* Manual check steps in the browser
* Visual check expectations
* Data consistency checks if relevant

**Notes / risks:**

* Mention edge cases, possible callback issues, layout risks, or ambiguity.

## 4. Dependency Map

Create a dependency table:

| Task | Depends on | Reason |
| ---- | ---------- | ------ |

Examples:

* Insight cards depend on reusable component/CSS task.
* Tournament chart updates depend on CVD palette fix.
* QA depends on all implementation phases.
* Screenshots depend on final visual state.

## 6. Suggested Execution Order

Create a numbered execution order from safest/highest-impact to lowest-impact.

Example:

1. Baseline run and screenshots.
2. Shared color fixes.
3. Action titles.
4. Insight card component.
5. Page-specific improvements.
6. Interaction polish.
7. QA and screenshots.
8. Optional features.

## 7. Risk and Rollback Plan

Create a table:

| Risk | Where it may happen | Mitigation | Rollback |
| ---- | ------------------- | ---------- | -------- |

Cover:

* callback breakage
* Plotly layout issues
* color changes reducing contrast
* annotations overlapping data
* reset filter callback complexity
* optional features expanding scope too much

## 8. Definition of Done

The implementation plan is complete when:

* All P0 tasks are clearly defined.
* All P1 tasks are clearly defined.
* P2 tasks are separated from required tasks.
* P3 tasks are clearly marked optional.
* Every task has affected files/components.
* Every task has acceptance criteria.
* Every task has test/check steps.
* Final QA and screen
shot tasks are included.
* No implementation was performed.

## Output requirements

* Write the Markdown in Vietnamese.
* Keep task titles clear and actionable.
* Use checkboxes where helpful.
* Use tables for phase overview, dependencies, and risk plan.
* Be specific enough that another coding agent can implement the tasks without rereading the whole improvement plan.
* Do not modify existing dashboard source code.
* Save the final file as:

`dashboard_improvement_tasks.md`
