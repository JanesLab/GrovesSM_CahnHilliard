# %%
import scipy.stats as stats
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import csv

plt.rcParams['pdf.use14corefonts'] = True


def get_lengths(indir):
    lengths = []
    total_lengths = []
    image_cnt = 0
    for image in range(50):
        try:
            tmp = pd.read_csv(
                f"{indir}/count_peaks_image{image}_.csv", header=0, index_col=0)
            for i, r in tmp.iterrows():
                lengths.append(r['l_arm_length'])
                lengths.append(r['r_arm_length'])
                total_lengths.append(r['l_arm_length'] + r['r_arm_length'])
            image_cnt += 1
        except FileNotFoundError:
            print(f"Image {image} not found")
    return lengths, total_lengths, image_cnt


def plot_violin_plots(lengths, total_lengths, image_cnt):
    # sns.histplot(lengths, bins=30)
    plt.axhline(np.percentile(lengths, 95), color='red',
                linestyle='--', label='95th percentile')
    plt.axhline(np.mean(lengths), color='grey', linestyle='--', label='mean')
    # plt.legend()
    sns.violinplot(lengths)
    plt.ylim(0, 9)
    plt.title(
        f"{cell_line} chromosome arm lengths in images \n n = {image_cnt} images, {len(lengths)//2} chromosomes; mean = {round(np.mean(lengths),3)} (um, one-arm length)")
    plt.savefig(f"{outdir}/chr_arm_lengths_violin_{cell_line}.pdf")
    # plt.show()
    plt.close()
    sns.violinplot(total_lengths)
    plt.ylim(0, 18)

    # sns.histplot(total_lengths, bins=30)
    plt.axhline(np.percentile(total_lengths, 95), color='red',
                linestyle='--', label='95th percentile')
    plt.axhline(np.mean(total_lengths), color='grey',
                linestyle='--', label='mean')
    # plt.legend()
    plt.title(
        f"Histo{cell_line} chromosome sizes in images \n n = {image_cnt} images, {len(total_lengths)} chromosomes; mean = {round(np.mean(total_lengths),3)} (um, full length)")
    # plt.show()
    plt.savefig(f"{outdir}/chr_full_lengths_violin_{cell_line}.pdf")
    plt.close()
    # np.savetxt(f"{outdir}/chromosome_lengths_{cell_line}_v2.csv",
    #            lengths, fmt="%f", delimiter=",")


# %%
indir = "/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/haspin_stripe_linescans/analysis/"
outdir = "/Users/smgroves/Documents/GitHub/Cahn_Hilliard_Model/plotting/image_analysis"
cell_line = "HeLa"
lengths_HeLa, total_lengths_HeLa, image_cnt_HeLa = get_lengths(indir)


indir = '/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/MCF10A/MCF10A_CPC_analysis/analysis/linescans'
lengths_MCF10A, total_lengths_MCF10A, image_cnt_MCF10A = get_lengths(indir)

# %%

# ks test
s, p = stats.kstest(lengths_HeLa, lengths_MCF10A)
print(s, p)

# %%
np.percentile(lengths_HeLa, 95)
# %%
