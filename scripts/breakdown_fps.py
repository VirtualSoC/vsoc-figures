import os
import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import warnings
import statistics
import logging

# GLOBAL CONSTANTS

PATH_TO_FIGURES = "../figs/"
FIGSIZE=(11, 7)
LEGEND_FONTSIZE = 27
LABEL_FONTSIZE = 45
hatches = ['xx', '\\\\', '//', '--', '++', '||', 'o', 'O', '.', '*']
width = 0.35  # the width of the bars
line_width = 1.5
colors = ['#7F449B', '#009D72', '#E5A023', "#21130d"]
# colors_dark = ['#f0f0f0', '#d0d0d0', '#b0b0b0', '#909090', '#21130d']
colors_dark = ['#ffffff', '#c0c0c0', '#808080', '#404040', '#000000']

font = {'family': 'Arial',
        'weight' : 'normal',
        'size'   : 40}
matplotlib.rcParams['pdf.fonttype']=42
matplotlib.rcParams['ps.fonttype']=42
bar_common_args = {"linewidth": line_width, "zorder": 3}
bar1_args = {"edgecolor": 'black', "facecolor":colors_dark[0]}
bar2_args = {"edgecolor": 'black', "facecolor":colors_dark[1]}
bar3_args = {"edgecolor": 'black', "facecolor":colors_dark[2]}
bar4_args = {"edgecolor": 'black', "facecolor":colors_dark[3]}
bar5_args = {"edgecolor": 'black', "facecolor":colors_dark[4]}

# envsetup

plt.rc('font', **font)
plt.rcParams.update({'legend.handlelength': 1.3, 'legend.borderpad': 0.25, "legend.labelspacing": 0.25, "legend.handletextpad": 0.5})
plt.rcParams['hatch.linewidth'] = line_width
pd.set_option("display.max_colwidth", 5000)
pd.set_option("display.max_columns", 10000)
pd.set_option("display.max_rows", 100)
os.makedirs(PATH_TO_FIGURES, exist_ok=True)
warnings.filterwarnings('ignore')

# refresh the fonts just installed
matplotlib.font_manager._load_fontmanager(try_read_cache=False)

error_config = {
    'elinewidth': 2,
    'ecolor': 'red',
    'capsize': 3,
    'linestyle': '-'   
}

app_id = ['vSoC','Fence-off','Prefetch-off']

input_file = "data/fps_breakdown.csv"
df = pd.read_csv(input_file)

simulators = ['vSoC', 'Fence-off', 'Prefetch-off']
fps = [[],[],[],[],[]]
errors = [[],[],[],[],[]]
software_types = df['Type'].unique()

for i in range(0,5):
    software_type = software_types[i]
    filtered_data = df[df['Type'] == software_type]

    for simulator in simulators:
        values = filtered_data[simulator].values
        values_filtered = [x for x in values if x != -1]
        if len(values_filtered) > 0:
            avg = np.mean(values_filtered)
            err = statistics.stdev(values_filtered) if len(values_filtered) > 1 else 0
        else:
            avg = 0
            err = 0
        fps[i].append(avg)
        errors[i].append(err)

print(fps)
print(errors)
sum1 = [0]*3
sum2 = [0]*3

for j in range(0,3):
    for i in range(0, 5):
        sum1[j] += fps[i][j]
        if i < 2:
            sum2[j] += fps[i][j]
    sum1[j]/=5
    sum2[j]/=2
print(sum1,sum2)

emulators=['vsoc','fence-off', 'write-invalidate']
app_keywords=['4k','360','cam','ar','cloud']
app_name=['UHD Video','360° Video','Camera','AR','Livestream']


f, ax = plt.subplots(figsize=FIGSIZE)

x = np.arange(len(app_id))  # the label locations
rects1 = ax.bar(x - width*4/5 , fps[0], label=app_id[0], width=width*2/5, **bar_common_args, **bar1_args, yerr= errors[0], error_kw=error_config)
rects2 = ax.bar(x - width*2/5 , fps[1], label=app_id[1], width=width*2/5, **bar_common_args, **bar2_args, yerr= errors[1], error_kw=error_config)
rects3 = ax.bar(x - 0.0, fps[2], label=app_id[2], width=width*2/5, **bar_common_args, **bar3_args, yerr= errors[2], error_kw=error_config)
rects4 = ax.bar(x + width*2/5 , fps[3], label=app_id[2], width=width*2/5, **bar_common_args, **bar4_args, yerr= errors[3], error_kw=error_config)
rects5 = ax.bar(x + 4*width/5 , fps[4], label=app_id[2], width=width*2/5, **bar_common_args, **bar5_args, yerr= errors[4], error_kw=error_config)


# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('FPS', size = LABEL_FONTSIZE)
ax.set_xticks(x, app_id)
ax.set_ylim((0.00, 100.0))

circ1 = mpatches.Patch(label=app_name[0], **bar_common_args, **bar1_args)
circ2 = mpatches.Patch(label=app_name[1], **bar_common_args, **bar2_args)
circ3 = mpatches.Patch(label=app_name[2], **bar_common_args, **bar3_args)
circ4 = mpatches.Patch(label=app_name[3], **bar_common_args, **bar4_args)
circ5 = mpatches.Patch(label=app_name[4], **bar_common_args, **bar5_args)
l2 = ax.legend(handles = [circ1, circ2, circ3, circ4, circ5], loc = 'upper right', bbox_to_anchor=(1.005, 1.005), fontsize=LEGEND_FONTSIZE, edgecolor = 'black', framealpha=1.0, fancybox = False, ncol=2)
plt.show()

f.savefig(PATH_TO_FIGURES + "breakdown_fps.pdf", format = "pdf", bbox_inches = 'tight')