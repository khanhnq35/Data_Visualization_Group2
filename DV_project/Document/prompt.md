You are a senior data visualization engineer, Dash/Plotly developer, and academic report assistant.

Your task is to inspect an existing dashboard project and produce a Markdown improvement plan. Do not modify the dashboard implementation. Only create a new Markdown file.

## Project context

The project is a Dash + Plotly + pandas dashboard about FIFA World Cup and international football.

Main storyline:

> The World Cup has become larger and more global over time, but championship success is still concentrated among a small group of elite national teams; modern match-level data still shows many upsets and competitive surprises.

Expected dashboard pages may include:

1. Overview
2. Dominance
3. Upsets & Competitiveness
4. Tournament Detail

Expected visualizations may include:

* KPI cards: number of World Cups, teams, matches, goals, number of champion teams.
* Line chart: teams / matches / goals by year.
* Line chart: average goals per game by year.
* Champion timeline.
* Bar chart: number of titles by champion.
* Heatmap or stacked bar: top 4 by continent.
* Ranked table: team, appearances, best position, goals for, points.
* Scatter plot: FIFA rank gap vs goal difference.
* Bar chart: biggest upsets by rank gap.
* Stacked bar: result by neutral location.
* Tournament Detail page: year dropdown, ranking table, goals for, goals against, goals for vs goals against scatter plot, highlight cards for top 4.

However, do not assume these charts exist. You must verify them from the actual project files.

## Inputs

Project root:`DV_project/`  

Course knowledge documents:

`DV_project/Document/`

The course documents cover the following chapters:

1. Chapter 1: Overview of data visualization
2. Chapter 2: Visual models and encoding
3. Chapter 3: Graphical perception
4. Chapter 4: Visualization for multi-dimensional data
5. Chapter 5: Visualization for graphs
6. Chapter 6: Principles of figure design
7. Chapter 7: Map visualization
8. Chapter 8: Interactive visualization
9. Chapter 9: Storytelling with data

If the documents are organized as separate files, read all relevant files under `<DOCUMENT_PATH>`. If they are combined into one file, read that file and extract chapter-level knowledge.

## Main objective

Create a Markdown file named:

`dashboard_visualization_improvement_plan.md`

Place it at the project root unless the project has a better docs/report folder. If a better folder exists, place it there and clearly mention the output path.

The Markdown file must analyze the current dashboard and propose concrete visualization improvements based on the 9 course chapters.

## Important constraints

* Do not implement any dashboard changes.
* Do not rewrite source code.
* Do not modify existing files except creating the new Markdown plan.
* Inspect the actual project files before writing the plan.
* Base your assessment on verified code, data files, page layouts, callbacks, and Plotly figures.
* If a chart is mentioned in the project description but not found in code, mark it as “Not found in current implementation”.
* If something cannot be verified, write “Need more information” instead of guessing.
* Every recommendation must connect to a specific dashboard page, chart, component, or file.
* Every recommendation must reference at least one relevant course chapter.
* Prefer practical, implementable recommendations over generic theory.
* Write the final Markdown in Vietnamese.

## What to inspect

Inspect the project structure and identify:

1. App entry point:

   * `app.py`, `main.py`, or equivalent.
2. Page files:

   * files under `pages/`, `src/pages/`, or similar.
3. Chart/component files:

   * Plotly figures, Dash components, KPI cards, tables, filters.
4. Data loading / preprocessing:

   * CSV paths, pandas transformations, derived fields.
5. Callbacks:

   * filters, dropdowns, click interactions, hover/detail panels.
6. Styling:

   * CSS files under `assets/`, theme constants, layout styles.
7. Existing report/storytelling documents:

   * README, markdown files, project notes, dashboard story plan, if available.

When referencing implementation details in the Markdown file, include:

* file path
* function/component name if available
* chart/component id if available
* data fields used if available

Example:

`pages/overview.py -> create_overview_layout() -> overview-growth-line-chart`

## Required Markdown structure

The output file must use the following structure.

# Dashboard Visualization Improvement Plan

## 1. Project Context

Summarize:

* Dashboard topic.
* Main storyline.
* Tools used.
* Main pages found in the codebase.
* Data sources found in the project.
* Current improvement objective.

Clearly distinguish between:

* information verified from project files
* information inferred from project description
* information not found or not verified

## 2. Project Structure and Evidence

Create a table:

| Area | File / Path | What was found | Notes |
| ---- | ----------- | -------------- | ----- |

Cover:

* app entry point
* page files
* chart files
* callback files
* data files
* style/theme files
* existing documentation

## 3. Current Dashboard Inventory

Create a table listing all charts/components found in the current implementation.

| Page | Chart / Component | File / Function / ID | Data fields used | Current chart type | Current purpose | Role in story | Verification status |
| ---- | ----------------- | -------------------- | ---------------- | ------------------ | --------------- | ------------- | ------------------- |

Use “Verified from code”, “Inferred”, or “Not found” in the verification status column.

## 4. Overall Assessment

Evaluate the current dashboard according to:

* Story clarity
* Chart choice
* Visual encoding
* Layout and visual hierarchy
* Color usage
* Interaction design
* Accessibility and readability
* Suitability for report/demo

Write three subsections:

### 4.1 Strengths

List 5–8 concrete strengths. Each strength must mention the relevant page/chart/component.

### 4.2 Limitations

List 5–8 concrete limitations. Each limitation must mention the relevant page/chart/component.

### 4.3 Most urgent improvement areas

Create a prioritized table:

| Priority | Issue | Affected page/chart | Related chapter | Why it matters |
| -------- | ----- | ------------------- | --------------- | -------------- |

## 5. Chart-by-Chart Analysis and Recommendations

For each chart/component found in the project, write a subsection using this format:

### [Page name] — [Chart / Component name]

#### Current role

Explain what question this chart/component currently answers.

#### Evidence from code

Include:

* file path
* function/component name
* chart id if available
* key data fields
* chart type

#### Strengths

List concrete strengths.

#### Limitations

List concrete limitations.

#### Recommended changes

Create a table:

| Recommendation | Based on chapter | Why it helps | Implementation suggestion | Affected files/components | Priority | Difficulty |
| -------------- | ---------------- | ------------ | ------------------------- | ------------------------- | -------- | ---------- |

Priority must be one of:

* High
* Medium
* Low

Difficulty must be one of:

* Low
* Medium
* High

Implementation suggestions must be practical and specific. Examples:

* Add annotation at 1998 to mark the expansion to 32 teams.
* Use one highlight color for selected champion and muted gray for non-selected teams.
* Replace a pie chart with a horizontal bar chart if there are too many categories.
* Add opacity to scatter points to reduce overplotting.
* Add hover fields: date, teams, score, rank gap, tournament.
* Add a reset filter button.
* Move the insight card closer to the chart it explains.
* Use an insight-oriented chart title instead of a generic title.
* Add a caption explaining that international match data only covers the modern period if applicable.

At minimum, analyze the following if they exist:

1. KPI cards
2. Overview growth line chart
3. Average goals per game line chart
4. Champion timeline
5. Champion count bar chart
6. Top 4 by continent heatmap or stacked bar
7. Ranked team table
8. Rank gap vs goal difference scatter plot
9. Biggest upsets bar chart
10. Result by neutral location chart
11. Tournament Detail ranking table
12. Goals for / goals against charts
13. Goals for vs goals against scatter plot
14. Highlight cards for selected tournament or top 4

If any of these are not found, add a short subsection:

### [Expected chart name] — Not found in current implementation

Explain whether it should be added, skipped, or replaced.

## 6. Chapter-Based Application Plan

This section must align with the course report requirement.

For each chapter, use the following structure:

### Chapter X: [Chapter title]

#### Techniques / principles applied

List the relevant course concepts from the chapter.

#### How applied in the current dashboard

Explain how the current dashboard already applies these concepts. Mention specific pages/charts.

#### Gaps or issues

Explain what is missing or weak.

#### Recommended improvements

List concrete improvements mapped to specific pages/charts.

#### Notes / adjustments

If the chapter is not directly applicable, explain why.

You must cover all 9 chapters:

### Chapter 1: Overview of data visualization

Cover:

* why this dataset/topic is suitable
* role of visualization in the problem
* exploratory vs explanatory visualization
* types of visualization used

### Chapter 2: Visual models and encoding

Cover:

* nominal, ordinal, quantitative variables
* visual marks: point, line, bar, area, text
* visual channels: position, length, color, size, shape
* encoding rationale for key variables

### Chapter 3: Graphical perception

Cover:

* pre-attentive processing
* magnitude estimation
* multiple visual encodings
* Gestalt grouping principles
* layout grouping and visual hierarchy

### Chapter 4: Visualization for multi-dimensional data

Cover:

* amounts
* distributions
* proportions
* relationships
* trends
* uncertainty
* coordinate systems and axes

### Chapter 5: Visualization for graphs

Cover:

* whether the project contains graph-like data
* possible node/edge representation if relevant
* whether a network graph should be added or avoided
* graph visualization risks

If graph visualization is not appropriate, explain why.

### Chapter 6: Principles of figure design

Cover:

* proportional ink
* handling overlap
* color palette and accessibility
* multi-panel figures
* titles, captions, and tables
* data-context balance
* avoiding unnecessary 3D charts

### Chapter 7: Map visualization

Cover:

* whether map data exists
* possible fields: host country, champion country, team country, continent
* whether choropleth/symbol map is useful
* map limitations and risks

If map visualization is not appropriate, explain why.

### Chapter 8: Interactive visualization

Cover:

* filtering
* zooming
* selection
* view transformation
* animation
* Dash and Plotly tools/libraries
* interaction quality and callback design

### Chapter 9: Storytelling with data

Cover:

* story structure
* narrative style
* explanatory vs exploratory flow
* interaction and exploration in the story
* titles, subtitles, annotations, insight cards

## 7. Proposed Revised Dashboard Structure

Propose an improved dashboard structure.

Create a table:

| Page | Main question | Main visual | Supporting visuals | Interactions | Key insight | Related chapters |
| ---- | ------------- | ----------- | ------------------ | ------------ | ----------- | ---------------- |

Include the four core pages if they exist or are planned:

1. Overview
2. Dominance
3. Upsets & Competitiveness
4. Tournament Detail

If map or graph visualization is recommended, mark it as optional or bonus unless it is clearly necessary.

## 8. Visual Style Guide

Propose a concrete visual style guide for the dashboard.

Cover:

* background
* card style
* font
* spacing
* color palette
* highlight color usage
* axis style
* gridline style
* legend placement
* tooltip style
* title format
* caption format
* annotation style
* table style

Make the style guide practical for Dash + Plotly.

## 9. Interaction Design Plan

Create a table:

| Page | Interaction | Purpose | Implementation idea | Affected files/components | Priority |
| ---- | ----------- | ------- | ------------------- | ------------------------- | -------- |

Cover the interactions that exist or should be added:

* year range filter
* team filter
* continent filter
* tournament filter
* dropdown for World Cup year
* hover tooltip
* click detail or selection
* reset filters
* zoom/pan where useful
* animation only if justified

Also mention interactions that should not be added because they would make the dashboard too complex.

## 10. Storytelling Improvement Plan

Propose:

* dashboard title
* dashboard subtitle
* narrative flow
* page titles
* page subtitles
* insight card text
* chart annotation text
* final conclusion message

Create a table:

| Story act | Page | Evidence/chart | Message to communicate | Suggested title/annotation |
| --------- | ---- | -------------- | ---------------------- | -------------------------- |

The story should follow this general flow:

1. The World Cup expanded over time.
2. Expansion did not make championship success evenly distributed.
3. Modern match-level data still shows upsets and uncertainty.
4. A selected tournament, especially 2022 if available, provides a concrete case study.

## 11. Prioritized Action Plan

Create three subsections:

### 11.1 Must fix before final submission

Tasks required for a stronger dashboard/report.

### 11.2 Should improve if time allows

Useful improvements that are not strictly required.

### 11.3 Optional / bonus

Advanced ideas such as maps, network graphs, animation, or advanced interactions.

Each task must use this format:

| Task | Related page/chart | Based on chapter | Expected impact | Difficulty | Suggested implementation location |
| ---- | ------------------ | ---------------- | --------------- | ---------- | --------------------------------- |

## 12. Report Writing Support

Write a concise outline for the report section:

“Technique application / Áp dụng kỹ thuật”

Use this format:

### Chapter X: [Chapter title]

#### Techniques / principles applied

* ...

#### How applied in the dashboard

* ...

#### Notes / adjustments

* ...

The content should be detailed enough for the student to expand into the final report.

## 13. Final Dashboard Checklist

Create a final checklist covering:

* chart choice
* encoding correctness
* color consistency
* accessibility
* proportional ink
* overlap handling
* layout hierarchy
* interaction quality
* storytelling clarity
* report alignment
* screenshot readiness
* demo readiness

## Output requirements

* Write the Markdown file in Vietnamese.
* Use clear headings and tables.
* Be specific and practical.
* Reference actual files/components from the project whenever possible.
* Do not make unsupported claims.
* If something is missing, explicitly state that it was not found.
* The final output must be saved as:

`dashboard_visualization_improvement_plan.md`

## Acceptance criteria

The task is complete only if:

1. The project files were inspected.
2. The course documents under `<DOCUMENT_PATH>` were read.
3. A new Markdown file was created.
4. The Markdown file includes chart-by-chart analysis.
5. The Markdown file includes chapter-by-chapter application for all 9 chapters.
6. Recommendations are tied to specific charts/pages/components.
7. Each major recommendation references relevant course chapters.
8. The file includes prioritized implementation tasks.
9. No existing dashboard code was modified.
