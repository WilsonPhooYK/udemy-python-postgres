import matplotlib.pyplot as plt
from database import OptionSpread

def create_pie_chart(options: list[OptionSpread]):
    figure = plt.figure()
    axes = figure.add_subplot(1,1,1)
    
    
    axes.pie(
        [option[1] for option in options],
        labels=[option[0] for option in options],
        autopct="%1.1f%%"
    )
    
    return figure

def create_bar_chart(options: list[OptionSpread]):
    figure = plt.figure(figsize=(10, 10)) # 100px * 100px
    figure.subplots_adjust(bottom=0.35)
    axes = figure.add_subplot(1,1,1)
    axes.set_title("Polls to their vote counts")
    axes.set_ylabel("Vote Count")
    
    axes.bar(
        range(len(options)), # [0, 1]
        [option[1] for option in options], # Value
        tick_label=[option[0] for option in options]
    )
    plt.xticks(rotation=30, ha="right")
    # axes.set_xticks(range(len(options)))
    # axes.set_xticklabels([option[0] for option in options], rotation=30)
    
    return figure