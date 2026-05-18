# Chapter 34: The Allure of Pies and Donuts

It is easy for us as teachers, writers, or speakers to discuss data visualization best practices, but we also realize there will be times when you will not have complete control over design decisions. There may be situations where you cannot avoid using pie and donut charts. A client request or a demand from the Director of All Things Circular may force decisions to be made about a visualization that are not best practice. It is our hope that this chapter will help you in these situations.

## Background

Pie charts, donut charts, and bubble charts typically are not good choices for visualizing data. There are occasional exceptions, but be very cautious in your use of these charts. Some examples follow.

Pie charts may be useful on a map to show a part-to-whole relationship within a geographic region. This is because there is no easy way to present multiple bar charts on a map where there is no common baseline for making comparisons.

![Figure 34.1: Pie charts on a map showing closed and open complaints](figure/Pic34.1_Piechart_on_map.png)

**Figure 34.1:** Pie charts on a map showing closed (blue) and open (orange) complaints.

As discussed in Chapter 1, the two best encoding methods for making precise quantitative comparisons are:

1. Using length or height from a common baseline for the comparison, such as a bar chart.
2. Using position to make the comparison, such as a dot plot.

When trying to show precise quantitative comparisons, using angles, arcs, area, or size of circles is not as good as using length or position to encode data.

Using size of a circle for precise comparisons can be especially difficult, but using size as secondary encoding in a scatterplot to show additional context to the data might be useful. For example, Figure 34.2 visualizes the comparison of fertility rate versus life expectancy at birth by country as a scatterplot. The size of a circle encodes population by country, a secondary metric that is not critical to the analysis, and color encodes the continent.

![Figure 34.2: Scatterplot showing life expectancy at birth versus fertility rate by country](figure/Pic34.2_ScatterPlot.png)

**Figure 34.2:** Scatterplot showing life expectancy at birth versus fertility rate by country.

Source: A re-creation of Hans Rosling's Gapminder. Free material from www.gapminder.org adapted by Jeffrey Shaffer using Tableau.

The primary purpose of this visualization is to compare fertility rate and life expectancy, not to show population. This secondary metric is less important. It is not critical to the analysis to make a precise comparison of the population among countries, yet it provides additional context to the overall story. It is also easy to see the most populated countries in the world, China and India, which are the large red circles.

## The Client or Boss Requires a Pie Chart

Say the boss or client wants a pie chart and the data has lots of categories. The first thing to consider is the type of data that is being displayed. The purpose of a pie chart is to show a part-to-whole relationship. The primary problem when reading a pie chart is comparing slices to one another. Try to minimize this in the design. Avoid dividing the pie or donut chart into many slices. As the slices in the chart increase, the data becomes more difficult to interpret.

Consider the example in Figure 34.3, which shows a pie chart with too many slices. There are 17 categories showing a percentage of total sales. Each category is a slice representing a different color. Even though the pie chart is ordered, making comparisons among the categories is very difficult and requires our eyes to go back and forth from the legend to the chart.

![Figure 34.3: Pie chart with 17 categories](figure/Pic34.3_Piechart_17categories.png)

**Figure 34.3:** Pie chart with 17 categories.

Now consider Figure 34.4. The same data is visualized in a pie chart but with a few major changes. First, there is only a single slice with a label, the category that is highlighted: phones. Instead of 17 categorical colors, there are only two: the highlighted category in blue and all of the others in gray. A bar chart has been added in place of the color legend. Now users can make a precise comparison using the bar chart and, if interactive, the user can select a bar to highlight any category in the pie chart.

Figure 34.4 meets the requirement of using a pie chart, but at the same time, it offers readers an alternative that utilizes the strength of the visual system: the precision that the bar chart offers. Notice that this solution provides an additional piece of information that was not immediately present in the other charts: the comparison of 85.6 percent versus 14.4 percent, which is now clearly indicated and is not easily seen in Figure 34.3.

![Figure 34.4: Pie chart with a single category highlighted and a companion bar chart](figure/Pic34.4_PieChart_SingleCategory_Comparison_BarChart.png)

**Figure 34.4:** Pie chart with a single category highlighted and a companion bar chart.

## The Client or Boss Requires a Donut Chart

Donut charts often are used as alternatives to pie charts to show a part-to-whole relationship. They also are used frequently as a key performance indicator (KPI). For example, Figure 34.5 shows that the North sales region has reached 64 percent of the target goal.

![Figure 34.5: Donut chart showing a KPI that has reached 64 percent of goal](figure/Pic34.5_DonutChart_KPI.png)

**Figure 34.5:** Donut chart showing a KPI that has reached 64 percent of goal.

As a single KPI indicator, this donut chart certainly is easier to understand than the pie chart example with 17 categories in Figure 34.3. The reason is that this donut chart does not require the reader to compare one category to another. It is simply an actual value coming full circle back to 100 percent of target.

However, although a single value is easy enough to see, consider what happens when four regions are being compared, as in Figure 34.6.

Try comparing the North versus East regions and then the South versus West regions. This comparison is much harder than interpreting a single KPI donut chart, and we think users will find themselves relying on the labels inside of the donuts.

![Figure 34.6: KPI donut chart showing four regions](figure/Pic34.6_DonutChart_KPI_4Region.png)

**Figure 34.6:** KPI donut chart showing four regions.

Also, it is important to note that this type of KPI visualization is useful only when the goal has an upper bound of 100 percent, as, for example, the number of seats in a sports arena, the capacity of a storage facility, or the number of cars on a lot. These things have an upper bound limit, which makes the goal fixed at 100 percent. A sales target, however, might not have an upper bound limit. It is possible that the sales team could sell at a higher price than expected, regardless of quantity, and achieve 106 percent of goal. A KPI donut is difficult to use if it is important to show that performance over the goal.

Throughout the book, we have discussed better chart types for this type of comparison, for example, a bullet chart with a bar chart showing the actual result and a target line showing the goal. These chart types do not have the same limitation as donut charts, and it will be easier to compare 106 percent of goal to 110 percent of goal.

Another alternative is a progress bar. Progress bars are very common, and often you probably do not even realize when they are being used. For example, Time Warner Cable uses a beautifully designed progress bar to show what time a TV show starts, when it ends, and how far into the show it is at any particular moment. The design also features a blue and gray color scheme, very similar to the color scheme being used in our examples. Figure 34.7 shows the data from the KPI donut chart as a progress bar.

**Figure 34.7:** Progress bars showing the KPI for four regions. Notice how easy it is to compare one region to another region. *(No corresponding image file was present in `figure/`.)*

## Where's My Donut?

Despite your efforts to present the data in the best way, you have hit a roadblock with a boss or client. Although the boss or client agrees that a bar chart with a target line or a progress bar might make the comparison easier, too many bar charts are "boring." The boss or client says something like "It needs more visual impact" or "Make it pop more." The person probably cannot define this in any further detail either but insists on donut charts.

If you find yourself in this situation, try:

1. Taking a deep breath.
2. Doing a quick YouTube search for "needs more cowbell."
3. Read on.

The next examples propose alternatives that may help you in these situations.

Note that we are not recommending these charts as best practice data visualization methods. We assume that if you have read this far, you have no choice but to give in to the requirements of the client or boss. We propose that you accommodate the poor choice by redundantly encoding the information in a better way.

## May I Have a Dozen Donuts?

Figure 34.8 shows an example where multiple donut charts are used for a comparison of defects. It is not actually a full dozen. As discussed previously, a series of donut charts makes it really hard to compare one chart to the next. This specific example is also problematic because all of the values are very low, so seeing the differences in the data is very difficult.

![Figure 34.8: Series of donut charts showing defect rates for different categories or time periods](figure/Pic34.6_Series_DonutChart_DefectRate.png)

**Figure 34.8:** Series of donut charts showing defect rates for different categories or time periods.

By adding a bar chart, the small differences in the defect rate can be seen. This is because the bar chart uses length from a common baseline, which allows for a very precise comparison that donut charts do not.

![Figure 34.9: The same series of donut charts but with a bar chart on top](figure/Pic34.7_Same_DonutChart_with_BarChart_Ontop.png)

**Figure 34.9:** The same series of donut charts but with a bar chart on top.

In Figure 34.10, the defect rate is plotted underneath the donut chart. This technique is similar to the one used in Figure 34.9, but a dot is used to represent each defect. Notice how easy it is to see the difference between 2 percent and 3 percent in both Figures 34.9 and 34.10. It is much easier to see this small difference using the bar chart or dots than trying to decipher and compare tiny segments of donut charts.

![Figure 34.10: The same series of donut charts plotted with individual dots showing the defects](figure/Pic34.8_Same_Donutchart_with_dots.png)

**Figure 34.10:** The same series of donut charts plotted with individual dots showing the defects.

## Conclusion

It is our hope that showing a few of these examples illustrates how accommodations can be made. Yes, there may be instances where you are forced to make bad design decisions; the boss or client just wants a dozen donuts. By offering small accommodations for these choices, you can help readers better understand the data and still meet the boss or client's demands.

And maybe if you are lucky, after a month or so, the boss or client will see that it is the bars or dots that are making the comparison easy, and you will get the all-clear to delete the donuts.
