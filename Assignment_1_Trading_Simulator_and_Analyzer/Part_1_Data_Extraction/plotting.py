import matplotlib.pyplot as plt

def plot_graph_2(time_dict, size_dict, sym):

    # subsequent values are excluded as the time taken are very high
    del time_dict[".h5"]
    del time_dict[".xlsx"]
    del time_dict[".sql"]
    del time_dict[".html"]
    del time_dict[".md"]

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8.84, 12.48))

    # Plotting for time
    keys_time = list(time_dict.keys())
    values_time = list(time_dict.values())

    bar_width = 0.35
    index_time = range(len(keys_time))
    ax1.bar(index_time, values_time, bar_width, label = "time", color = "green")

    ax1.set_xlabel('File Types')
    ax1.set_ylabel('Time (in milliseconds)')
    ax1.set_title('Comparison of File Types - Time')
    ax1.set_xticks(index_time)
    ax1.set_xticklabels(keys_time)
    ax1.legend()

    # Plotting for size
    keys_size = list(size_dict.keys())
    values_size = list(size_dict.values())

    index_size = range(len(keys_size))
    ax2.bar(index_size, values_size, bar_width, label = "size")

    ax2.set_xlabel('File Types')
    ax2.set_ylabel('File size (in KB)')
    ax2.set_title('Comparison of File Types - Size')
    ax2.set_xticks(index_size)
    ax2.set_xticklabels(keys_size)
    ax2.legend()

    plt.tight_layout()
    plt.savefig(sym + ".png")
    plt.close(fig)
    plt.clf()

def plot_graph_3(compression_time_dict, decompression_time_dict, compressed_size_dict, sym):

    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8.84, 12.48))

    # Plotting for time
    keys_time = list(compression_time_dict.keys())
    values_time = list(compression_time_dict.values())

    bar_width = 0.35
    index_time = range(len(keys_time))
    ax1.bar(index_time, values_time, bar_width, label = "compression time", color = "green")

    ax1.set_xlabel('File Types')
    ax1.set_ylabel('Time (in milliseconds)')
    ax1.set_title('Comparison of File Types - Compression Time')
    ax1.set_xticks(index_time)
    ax1.set_xticklabels(keys_time)
    ax1.legend()

    # Plotting for time
    keys_time = list(decompression_time_dict.keys())
    values_time = list(decompression_time_dict.values())

    bar_width = 0.35
    index_time = range(len(keys_time))
    ax2.bar(index_time, values_time, bar_width, label = "decompression time", color = "orange")

    ax2.set_xlabel('File Types')
    ax2.set_ylabel('Time (in milliseconds)')
    ax2.set_title('Comparison of File Types - Decompression Time')
    ax2.set_xticks(index_time)
    ax2.set_xticklabels(keys_time)
    ax2.legend()

    # Plotting for size
    keys_size = list(compressed_size_dict.keys())
    values_size = list(compressed_size_dict.values())

    index_size = range(len(keys_size))
    ax3.bar(index_size, values_size, bar_width, label = "compressed size")

    ax3.set_xlabel('File Types')
    ax3.set_ylabel('File size (in KB)')
    ax3.set_title('Comparison of File Types - Compressed Size')
    ax3.set_xticks(index_size)
    ax3.set_xticklabels(keys_size)
    ax3.legend()

    plt.tight_layout()
    plt.savefig(sym + "_compress" + ".png")
    plt.close(fig)
    plt.clf()