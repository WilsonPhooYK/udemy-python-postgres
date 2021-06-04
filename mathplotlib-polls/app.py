import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from data import polls

poll_titles = [poll[0] for poll in polls]
poll_men = [poll[1] for poll in polls]
poll_women = [poll[1] for poll in polls]

poll_x_coordinates = list(range(len(polls)))
poll_x2_coordinates = [index + len(polls) + 1 for index in range(len(polls))]

figure = plt.figure(figsize=(6,6), linewidth=5)
figure.subplots_adjust(bottom=0.35, wspace=0.3)
axes1 = figure.add_subplot(1, 2, 1)
plt.xticks(poll_x_coordinates, poll_titles, rotation=30, ha="right")

men_plot = axes1.bar(
    poll_x_coordinates,
    poll_men,
    # tick_label=poll_titles
    # label="Men"
)
women_plot = axes1.bar(
    poll_x_coordinates,
    poll_women,
    # tick_label=poll_titles, # latest label will show in the axes
    bottom=poll_men,
    # label="Women"
)
axes1.legend((men_plot, women_plot), ("Men", "Women"))

axes2 = figure.add_subplot(1, 2, 2)
men_plot_2 = axes2.bar(
    poll_x_coordinates,
    poll_men,
    # tick_label=poll_titles
    # label="Men"
    color=["#5c44fd", "#ff5566", "#5c44fd", "#ff5566", "#5c44fd", "#ff5566", "#5c44fd"]
)

# axes.legend()
# axes2.legend((men_plot,), ("Men",))

handles = [
    Patch(facecolor="#5c44fd", label="Tech"),
    Patch(facecolor="#ff5566", label="Clothing")
]
axes2.legend(handles=handles)

plt.xticks(poll_x_coordinates, poll_titles, rotation=30, ha="right")
# plt.show()
figure.savefig("graph.png", bbox_inches="tight", pad_inches=0.3, facecolor="#FFFFFF", edgecolor="#FF0000")
