import matplotlib.pyplot as plt
# plt.figure()

# ####
# # plt.xlabel("Human")
# # plt.ylabel("Amounts")
# # plt.title("Human Amounts")
# # # "o" - dots
# # # lines = plt.plot([1,2,3,4],[3,5,9,25], "o")
# # lines = plt.plot(['Men','Woman','Children','Old'],[3,5,9,25], "o")
# # plt.setp(lines, color="#FF5566")

# ####
# plt.axis([0,6,0,20]) # 0,6 x-range  0, 20 y-range
# plt.plot([1,2,3,4],[3,5,9,25])

# plt.show()

# ####
# figure = plt.figure()
# axes = figure.add_subplot()
# axes.set_title("A test line graph")
# axes.set_xlabel("Numbers")
# axes.set_ylabel("Occurances")
# axes.plot([1,2,3,4],[3,5,9,25])

# #### 2 lines in a graph
# # figure = plt.figure()
# # ax1 = figure.add_subplot(1, 2, 1) # 1 row 2 column in column 1
# # ax2 = figure.add_subplot(1, 2, 2) # 1 row 2 column in column 2

# figure, (ax1, ax2) = plt.subplots(1, 2)

# ax1.plot([1,2,3,4],[3,5,9,25])
# ax2.plot([1,2,3,4],[5,7,11,20])
# plt.show()

# ####
option_votes = [63,28,8]
option_names = [
    "Flask",
    "Django",
    "It depends"
]
figure = plt.figure()
ax1 = figure.add_subplot(1, 1, 1)

ax1.pie(
    option_votes,
    labels=option_names,
    explode=[0.1, 0, 0],
    autopct="%1.1f%%"
)
plt.show()
