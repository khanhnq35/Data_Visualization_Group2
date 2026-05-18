# Chapter 18: Server Process Monitoring

A server-monitoring dashboard highlighting delayed and failed processes for any given day.

- Dashboard designer: Mark Jackson (<http://ugamarkj.blogspot.com>)
- Organization: Piedmont Healthcare

![Server process monitoring dashboard overview](figure/dashboard_overview.png)

## Scenario

### Big Picture

You are a business intelligence manager. Your employees rely on your business intelligence service being online with the latest data when they arrive at work in the morning. You need to know if something went wrong with the overnight processes before everyone gets to work.

What you need is a dashboard you can look at each morning that shows you what, if anything, is holding up your server. If anything is going wrong, you can jump directly to that process and take corrective action. Also, you can delve into that process's recent history to see if it has been consistently problematic. If it has, you need to do more research and decide on a course of action to fix the process.

To determine what to do next, you might ask the following questions:

- Did our server processes succeed today?
- Which processes failed?
- Are the failing processes repeatedly failing?
- Which processes are taking longer than usual?

### Specifics

- You manage a server and need to respond quickly if processes fail. If these processes are going to cause problems for the users, those problems need to be identified and addressed quickly.
- You need an email each morning with a summary report of overnight processes. If a high number fail or if some key processes fail, you need to click the email to go to the live dashboard and drill into the details.
- For any given failed process, you need extra contextual details to help you diagnose and fix the problem. Was this failure caused by a problem earlier in the process chain? Is this process consistently failing?

### Related Scenarios

- You are a manufacturer and need to track the production schedule's progress towards completion.
- You are an event manager and need to track that tasks begin correctly and run to time.

## How People Use the Dashboard

As an administrator responsible for keeping your enterprise's systems up and running, you need to know if things are going wrong. A static image of the dashboard is emailed to Mark Jackson, the dashboard designer, each morning.

The bar chart at the top shows percentage of failures for each of the last 14 days. The most recent is at the far right, highlighted in the overview dashboard. Comparing last night to the last two weeks allows Mark to easily see if last night was normal or an outlier. The average failure rate is shown as a dotted line.

Mark can see that 6.7 percent of processes failed overnight. That is a real problem, and significantly above the average failures for the previous 14 days. Some investigation is needed.

Mark can see all the processes that took place that day. Gray ones succeeded, and red ones failed. Reference lines on each Gantt bar show the scheduled start time (dotted line) and the average time the task has taken (solid line). The Epic Radiant Orders task is the clear problem on this day.

### Figure 18.1: The tool tip adds extra detail about the failure

![The tool tip adds extra detail about the failure](figure/fig18.1_The_tool_tip.png)

If Mark wants to investigate any task in detail, he can hover over it to see a tool tip for extra contextual information.

Now Mark can see details about the Epic Radiant Orders task. Not only did the task fail, it took nearly seven hours to fail. On average, it takes around two hours to complete.

From here, he has two options. The tool tip has a URL link in it: he can click the link in the tool tip to go and see the task on the server itself. His other option is to click on the Gantt bar, which reveals a new view at the bottom of the dashboard showing detail for the task.

### Figure 18.2: Detail view for a specific task

![Detail view for the Epic Radiant Orders task](figure/fig18.2_Detail_view.png)

In Figure 18.2, Mark can see that the Epic Radiant Orders task has been failing consistently recently. Whatever preventive medicine he has been applying has not yet succeeded.

The detail view shows the performance of a single task over the previous month. Clearly, the Epic Radiant Orders task needs some investigation. It has failed seven times in the last month.

Throughout this process, Mark has gone from receiving an email with a daily alert to being able to see the overview for the day. From there, he can drill down into detail where he needs to explore further and finally go straight to any server processes that need investigation.

## Why This Works

### Labels on the Gantt Bar

Mark could have put the header labeling each task at the left-hand edge of the chart, in a header area. Instead, he chose to label the Gantt bar itself. On first glance, this makes the view look busy: there is an awful lot of text butting up against the bar.

When you look at Figure 18.3, though, you can see why he did it. When he sees a red, failing task, its name is right there, where his eyes are. He does not need to do a careful look up to the left to find the name of the task.

### Figure 18.3: Label position comparison

![The top view shows labels next to Gantt bars; the lower view shows labels on the left](figure/fig18.3_Label_position_compare.png)

### Reference Lines

In addition to finding the failing processes quickly, Mark needs an indication of which other processes might be contributing to the failures. In this case, he uses reference lines to show schedules and durations.

In Figure 18.4, Mark can see that the Epic Radiant Orders task failed. The dotted vertical lines for each task show him when each task was due to start. Epic Radiant Orders was significantly delayed. It should start around 10:30 a.m. but did not start until around 5 p.m.

The solid vertical lines show the average duration of each task. In this case, Mark can see that the previous task, Epic ASAP Events, also finished later than normal. Did one delay cause the other? Mark knows he will have to investigate both of these.

### Figure 18.4: Scheduled tasks shown by Gantt bars

![Dotted lines indicate scheduled start time and solid lines indicate average task duration](figure/fig18.4_Dot_line.png)

### URL Actions

The tool tip contains a URL. Mark can find which details need further investigation and, with a single click, can go straight to the relevant information. This speed and directness is important to any dashboard because it puts users in the flow. Mark does not have to waste time finding the relevant next dashboard; the URL takes him there directly.

### Overview, Zoom and Filter, Details on Demand

One aspect of successful dashboards is to create an exploratory path through the data. Ben Shneiderman, Distinguished Professor in the Department of Computer Science at the University of Maryland and a pioneer of information visualization study, described his mantra of data visualization:

- Overview
- Zoom and filter
- Details on demand

The dashboard in Figure 18.5 demonstrates this flow. Starting at the top, Mark has an overview of the server performance for recent days (1). Clicking on a day allows him to filter down to a single-day view (2). He can then get details on demand by clicking on a task (3), to open the details on task summary view (4), or use the URL to go directly to the task on the server itself (5). The flow is top down and easy to follow.

### Figure 18.5: A dashboard with a great top-down flow

![A dashboard with a great top-down flow](figure/fig18.5_Dashboard_good_top_down_workflow.png)

The task summary view is not visible in the emailed report or when the report is first opened. That view appears only when it is clicked. This dashboard is a nice way of showing as much detail as possible in the initial view and bringing in contextual information only when it is needed.

## Author Commentary

### Andy

This is a simple dashboard. I think that works in its favor. Mark designed it to answer the three most important questions he has each day:

1. How many tasks failed?
2. Which ones were they?
3. Are the failures a trend or a one-off?

Bar chart. Gantt chart. Gantt chart. That is all it took, and the dashboard needed no other adornment.

In anticipation that follow-up questions will arise, the URL link lets Mark get to the next set of questions he might need to ask. The strategy of linking dashboards together allows you to keep each one from becoming cluttered. Attempting to answer too many questions in one dashboard reduces clarity.

There are several issues with text overlapping the vertical reference lines in the Gantt bar. That might have earned a few "ugly cats," but this dashboard got an exemption for an important reason: it is for his eyes only. Because the destined audience is himself, he has built something that works for him.

When designing a dashboard, how much spit and polish should you put on it? If it is just for you, then, really, what you put on your dashboard is between you and the computer screen. If it works for you, that is fine. However, if it is for consumption by an entire organization, you have to make the experience as smooth as possible. If Mark's dashboard was to be used by the entire organization, we might suggest workarounds to avoid the overlapping text.
