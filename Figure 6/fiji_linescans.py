# %%
import pandas as pd
import numpy as np
import sklearn
import scipy.signal as ss
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.backends.backend_pdf import PdfPages
import os
import re


def rename_MCF10A_files(indir):
    # Loop through all files in the folder
    for filename in os.listdir(indir):
        if filename.endswith('_CPC.csv'):
            print(filename)
            # Match the pattern "ImageXX"
            match = re.search(r'(Image\d+)', filename)
            if match:
                image_id = match.group(1)
                new_name = f"{image_id}_CPC.csv"
                old_path = os.path.join(indir, filename)
                new_path = os.path.join(indir, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_name}")
        elif filename.endswith('_KT.csv'):
            print(filename)

            # Match the pattern "ImageXX"
            match = re.search(r'(Image\d+)', filename)
            if match:
                image_id = match.group(1)
                new_name = f"{image_id}_KT.csv"
                old_path = os.path.join(indir, filename)
                new_path = os.path.join(indir, new_name)
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_name}")


indir = "/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/MCF10A/MCF10A_CPC_analysis/"
outdir = "/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/MCF10A/MCF10A_CPC_analysis/analysis/linescans"

# rename_MCF10A_files(indir)


def plot_linescan_condensates(
    indir, image, rescaled=True, max_width=800, min_width=100, prominence=15, suffix=""
):
    if rescaled:
        name = f"{indir}/Image_{image}_rescaled{suffix}.pdf"
    else:
        name = f"{indir}/Image_{image}{suffix}.pdf"
    print(name)
    pdf = PdfPages(name)

    tmp = np.genfromtxt(f"{indir}/Image{image}_CPC.csv",
                        max_rows=1, delimiter=",")
    num_chr = round(tmp.shape[0] / 2)

    for i in range(num_chr):
        figure = plt.figure()
        df = pd.read_csv(
            f"{indir}/Image{image}_CPC.csv",
            usecols=[2 * i, 2 * i + 1],
            header=0,
            index_col=None,
        )
        df.columns = ["X", "Y"]
        df.dropna()
        df["Y_rescaled"] = df["Y"] / df["Y"].max()
        kt = pd.read_csv(
            f"{indir}/Image{image}_KT.csv",
            usecols=[2 * i, 2 * i + 1],
            header=0,
            index_col=None,
        )
        kt.columns = ["X", "Y"]
        kt.dropna()
        kt["Y_rescaled"] = kt["Y"] / kt["Y"].max()
        if rescaled:
            value = "Y_rescaled"
        else:
            value = "Y"
        pixel_width = 60.13

        if rescaled:
            prominence = prominence / df["Y"].max()
        peaks, properties = ss.find_peaks(
            df[value],
            prominence=prominence,
            width=[round(min_width / pixel_width),
                   round(max_width / pixel_width)],
        )
        # prominences = ss.peak_prominences(df[value], peaks)[0]
        # widths = ss.peak_widths(df[value], peaks)[0]

        plt.plot(df[value], label="CPC (AurkB Intensity)")
        plt.plot(
            kt[value], c="grey", linestyle="--", label="Kinetochore (ACA Intensity)"
        )
        plt.vlines(
            x=peaks,
            ymin=df[value][peaks] - properties["prominences"],
            ymax=df[value][peaks],
            color="bisque",
            label="Prominence of condensate",
        )
        plt.hlines(
            y=properties["width_heights"],
            xmin=properties["left_ips"],
            xmax=properties["right_ips"],
            color="C1",
            label="Width of condensate",
        )
        plt.plot(peaks, df[value][peaks], "X",
                 label="Condensates (Intensity Peaks)")
        plt.legend(loc="best", prop={"size": 8})
        plt.title(
            f"CPC Condensate Intensity along pH3 axis \n Max width: {max_width}nm ({round(max_width/pixel_width)} pixels), Min width: {min_width}nm ({round(min_width/pixel_width)} pixels) \n Min Prominence: {round(prominence,3)}"
        )
        if rescaled:
            plt.ylabel("Normalized Intensity")
        else:
            plt.ylabel("Intensity")
        plt.xlabel("Microns")
        plt.xticks(
            plt.xticks()[0][1:-1],
            [round(j * 0.06013, 3) for j in plt.xticks()[0][1:-1]],
            fontsize=8,
        )
        plt.tight_layout()
        # plt.show()
        figure.text(0.5 / 8.5, 0.5 / 11.0, str(i + 1), ha="center", fontsize=8)

        pdf.savefig()
        plt.close()

    pdf.close()


# indir = "/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/MCF10A/MCF10A_CPC_analysis/analysis/linescans"
# for i in range(1, 50):
#     try:
#         plot_linescan_condensates(
#             indir, image=i, rescaled=True, max_width=800, min_width=100, prominence=15
#         )
#         plot_linescan_condensates(
#             indir, image=i, rescaled=False, max_width=800, min_width=100, prominence=15
#         )
#     except FileNotFoundError:
#         print(f"File not found for image {i}")
# plot_linescan_condensates(indir, image=3, rescaled=False,
#                           max_width=800, min_width=100, prominence=15)
# plot_linescan_condensates(indir, image=4, rescaled=False,
#                           max_width=800, min_width=100, prominence=15)
# plot_linescan_condensates(indir, image=6, rescaled=False,
#                           max_width=800, min_width=100, prominence=15)


# plot_linescan_condensates(indir, image=0, rescaled=True,max_width = 800, min_width = 100, prominence = 15)
# plot_linescan_condensates(indir, image=0, rescaled=False,max_width = 800, min_width = 100, prominence = 15)

# plot_linescan_condensates(indir, image=1, rescaled=True,max_width = 800, min_width = 100, prominence = 15)
# plot_linescan_condensates(indir, image=1, rescaled=False,max_width = 800, min_width = 100, prominence = 15)

# plot_linescan_condensates(indir, image=5, rescaled=True,max_width = 800, min_width = 100, prominence = 15)
# plot_linescan_condensates(indir, image=5, rescaled=False,max_width = 800, min_width = 100, prominence = 15)

# plot_linescan_condensates(indir, image=8, rescaled=True,max_width = 800, min_width = 100, prominence = 15)
# plot_linescan_condensates(indir, image=8, rescaled=False,max_width = 800, min_width = 100, prominence = 15)

# plot_linescan_condensates(indir, image=9, rescaled=True,max_width = 800, min_width = 100, prominence = 15)
# plot_linescan_condensates(indir, image=9, rescaled=False,max_width = 800, min_width = 100, prominence = 15)

# plot_linescan_condensates(
#     indir, image=10, rescaled=False, max_width=800, min_width=100, prominence=15
# )

############
#  replot linescans for just HeLa Image 3 and MCF10A Image 29 (Figure 6) centered on ACA peak, with x axis showing distance from IC

# %%
def plot_centered_linescan_condensates(indir,
                                       image,
                                       num_chr,
                                       xmin=-5,
                                       xmax=5,
                                       rescaled=True,
                                       max_width=800,
                                       min_width=100,
                                       prominence=15,
                                       suffix=""):
    if rescaled:
        name = f"{indir}/Centered_image_{image}_{num_chr}_rescaled{suffix}.pdf"
    else:
        name = f"{indir}/Cnetered_image_{image}_{num_chr}{suffix}.pdf"
    print(name)
    pdf = PdfPages(name)

    tmp = np.genfromtxt(f"{indir}/Image{image}_CPC.csv",
                        max_rows=1,
                        delimiter=",")
    i = num_chr - 1
    figure = plt.figure()
    df = pd.read_csv(
        f"{indir}/Image{image}_CPC.csv",
        usecols=[2 * i, 2 * i + 1],
        header=0,
        index_col=None,
    )
    df.columns = ["X", "Y"]
    df.dropna()
    df["Y_rescaled"] = df["Y"] / df["Y"].max()
    kt = pd.read_csv(
        f"{indir}/Image{image}_KT.csv",
        usecols=[2 * i, 2 * i + 1],
        header=0,
        index_col=None,
    )
    kt.columns = ["X", "Y"]
    kt.dropna()
    kt["Y_rescaled"] = kt["Y"] / kt["Y"].max()
    if rescaled:
        value = "Y_rescaled"
    else:
        value = "Y"
    pixel_width = 60.13

    if rescaled:
        prominence = prominence / df["Y"].max()
    peaks, properties = ss.find_peaks(
        df[value],
        prominence=prominence,
        width=[
            round(min_width / pixel_width),
            round(max_width / pixel_width)
        ],
    )
    # prominences = ss.peak_prominences(df[value], peaks)[0]
    # widths = ss.peak_widths(df[value], peaks)[0]

    # find the index of the kt peak
    IC_peak = kt[value].idxmax()
    kt['distance_from_IC'] = (kt.index - IC_peak) * 0.06013  # in um
    df['distance_from_IC'] = (df.index - IC_peak) * 0.06013  # in um

    # plt.plot(df[value], label="CPC (AurkB Intensity)")
    sns.lineplot(data=df,
                 x='distance_from_IC',
                 y=value,
                 label="CPC (AurkB Intensity)")
    sns.lineplot(data=kt,
                 x='distance_from_IC',
                 y=value,
                 c="grey",
                 linestyle="--",
                 label="Kinetochore (ACA Intensity)")
    # plt.plot(
    #     kt[value], c="grey", linestyle="--", label="Kinetochore (ACA Intensity)"
    # )
    # plt.vlines(
    #     x=peaks,
    #     ymin=df[value][peaks] - properties["prominences"],
    #     ymax=df[value][peaks],
    #     color="bisque",
    #     label="Prominence of condensate",
    # )
    # plt.hlines(
    #     y=properties["width_heights"],
    #     xmin=properties["left_ips"],
    #     xmax=properties["right_ips"],
    #     color="C1",
    #     label="Width of condensate",
    # )
    # plt.plot(peaks, df[value][peaks], "X",
    #          label="Condensates (Intensity Peaks)")
    plt.legend(loc="best", prop={"size": 8})
    plt.title(
        f"CPC Condensate Intensity along pH3 axis \n Max width: {max_width}nm ({round(max_width/pixel_width)} pixels), Min width: {min_width}nm ({round(min_width/pixel_width)} pixels) \n Min Prominence: {round(prominence,3)}"
    )
    if rescaled:
        plt.ylabel("Normalized Intensity")
    else:
        plt.ylabel("Intensity")
    plt.xlabel("Microns from ACA Peak")
    plt.xlim(xmin, xmax)
    # plt.xticks(
    #     plt.xticks()[0][1:-1],
    #     [round(j * 0.06013, 3) for j in plt.xticks()[0][1:-1]],
    #     fontsize=8,
    # )
    plt.tight_layout()
    # plt.show()
    figure.text(0.5 / 8.5, 0.5 / 11.0, str(i + 1), ha="center", fontsize=8)
    # break
    pdf.savefig()
    plt.close()

    pdf.close()

# 1.6um / 0.06013nm = 26.6 grid points per 1.6um


indir = "/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/haspin_stripe_linescans/analysis"
outdir = "/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/haspin_stripe_linescans/linescan_peak_plots/"

plot_centered_linescan_condensates(
    indir, image=3, num_chr=9, xmin=-3, xmax=5.1, rescaled=True, max_width=800, min_width=100, prominence=15)

indir = "/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/MCF10A/MCF10A_CPC_analysis/analysis/linescans"
outdir = "/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/MCF10A/MCF10A_CPC_analysis/analysis/linescans"
# plot_centered_linescan_condensates(
# indir, image=29, num_chr=2, xmax=3, xmin=-5.1, rescaled=True, max_width=800, min_width=100, prominence=15)


def count_peaks(
    indir, image, rescaled=True, max_width=800, min_width=100, prominence=15, suffix=""
):
    # if rescaled:
    #     name = f'{indir}/Image_{image}_rescaled{suffix}.pdf'
    # else:
    #     name = f'{indir}/Image_{image}{suffix}.pdf'
    # print(name)
    # pdf = PdfPages(name)

    tmp = np.genfromtxt(f"{indir}/Image{image}_CPC.csv", delimiter=",")
    tmp = tmp[:, ~np.isnan(tmp).all(axis=0)]

    print("CPC file loaded")

    num_chr = round(tmp.shape[1] / 2)
    results = pd.DataFrame(
        columns=[
            "image_num",
            "chr_num",
            "chr_length",
            "IC_peaks",
            "kt_peak",
            "l_arm_length",
            "r_arm_length",
            "left_peaks",
            "right_peaks",
            "chr_per_1.6um_L",
            "chr_per_1.6um_R",
        ]
    )
    print(num_chr)
    for i in range(num_chr):

        # figure = plt.figure()
        df = pd.read_csv(
            f"{indir}/Image{image}_CPC.csv",
            usecols=[2 * i, 2 * i + 1],
            header=0,
            index_col=None,
        )
        df.columns = ["X", "Y"]
        df.dropna()
        df["Y_rescaled"] = df["Y"] / df["Y"].max()
        kt = pd.read_csv(
            f"{indir}/Image{image}_KT.csv",
            usecols=[2 * i, 2 * i + 1],
            header=0,
            index_col=None,
        )
        kt.columns = ["X", "Y"]
        kt.dropna()
        kt["Y_rescaled"] = kt["Y"] / kt["Y"].max()
        if rescaled:
            value = "Y_rescaled"
        else:
            value = "Y"
        pixel_width = 60.13
        len_chr = df["X"].max() * 10000

        if rescaled:
            prominence = prominence / df["Y"].max()
        peaks, properties = ss.find_peaks(
            df[value],
            prominence=prominence,
            width=[round(min_width / pixel_width),
                   round(max_width / pixel_width)],
        )
        IC_peak = kt[value].idxmax()
        kt_peaks, kt_properties = ss.find_peaks(
            kt[value],
            prominence=prominence,
            height=0.6,
            width=round(min_width / pixel_width),
        )
        print(kt_peaks)
        # print(i)
        # print("     IC peak:", IC_peak)
        idx_max = np.argmax(kt_properties["peak_heights"])
        kt_left = kt_properties["left_ips"][idx_max]
        kt_right = kt_properties["right_ips"][idx_max]
        # print("     ", kt_left, kt_right)
        ic_CPC_peaks = []
        left_CPC_peaks = []
        right_CPC_peaks = []
        left_CPC_peaks_1600nm = []
        right_CPC_peaks_1600nm = []
        for j, p in enumerate(peaks):
            CPC_left = properties["left_ips"][j]
            CPC_right = properties["right_ips"][j]
            if kt_left <= CPC_right and kt_right >= CPC_left:
                # print("     ", p)
                ic_CPC_peaks.append(p)
                # CPC_left_boundary = CPC_left
                # CPC_right_boundary = CPC_left
            elif CPC_right < kt_left:
                left_CPC_peaks.append(p)
                if p >= IC_peak - 26.6:
                    left_CPC_peaks_1600nm.append(p)
            elif CPC_left > kt_right:
                right_CPC_peaks.append(p)
                if p <= IC_peak + 26.6:
                    right_CPC_peaks_1600nm.append(p)
        # print("     ic ",ic_CPC_peaks)
        # print("     left ",left_CPC_peaks)
        # print("     right ",right_CPC_peaks)
        # print("     left within 1.6um",left_CPC_peaks_1600nm)
        # print("     right within 1.6um",right_CPC_peaks_1600nm)
        l_arm_length = kt_peaks[idx_max] * 0.06013
        r_arm_length = (df["X"].idxmax() - kt_peaks[idx_max]) * 0.06013
        results = pd.concat(
            [
                pd.DataFrame(
                    [
                        [
                            image,
                            i,
                            len_chr,
                            ic_CPC_peaks,
                            kt_peaks[idx_max],
                            l_arm_length,
                            r_arm_length,
                            left_CPC_peaks,
                            right_CPC_peaks,
                            len(left_CPC_peaks_1600nm),
                            len(right_CPC_peaks_1600nm),
                        ]
                    ],
                    columns=results.columns,
                ),
                results,
            ],
            ignore_index=True,
        )
        # tmp_results = pd.Series({"image_num":[image],
        #                         "chr_num":[i],
        #                         "chr_length":[len_chr],
        #                         "IC_peaks":[ic_CPC_peaks],
        #                         "left_peaks":[left_CPC_peaks],
        #                         "right_peaks":[right_CPC_peaks],
        #                         "chr_per_1.6um_L":[len(left_CPC_peaks_1600nm)],
        #                         "chr_per_1.6um_R":[len(right_CPC_peaks_1600nm)]})
        # results = pd.concat([results,tmp_results], axis = 1, ignore_index=True)

    return results

    # widths = ss.peak_widths(df[value], peaks)[0]

    #     plt.plot(df[value], label = "CPC (AurkB Intensity)")
    #     plt.plot(kt[value], c = 'grey', linestyle = "--", label = "Kinetochore (ACA Intensity)")
    #     plt.vlines(x=peaks, ymin=df[value][peaks] - properties["prominences"],
    #             ymax = df[value][peaks], color = "bisque", label = "Prominence of condensate")
    #     plt.hlines(y=properties["width_heights"], xmin=properties["left_ips"],
    #             xmax=properties["right_ips"], color = "C1", label = "Width of condensate")
    #     plt.plot(peaks, df[value][peaks], "X", label = "Condensates (Intensity Peaks)")
    #     plt.legend(loc="best",prop={'size': 8})
    #     plt.title(f"CPC Condensate Intensity along pH3 axis \n Max width: {max_width}nm ({round(max_width/pixel_width)} pixels), Min width: {min_width}nm ({round(min_width/pixel_width)} pixels) \n Min Prominence: {round(prominence,3)}")
    #     if rescaled:
    #         plt.ylabel("Normalized Intensity")
    #     else:
    #         plt.ylabel("Intensity")
    #     plt.xlabel("Microns")
    #     plt.xticks(plt.xticks()[0][1:-1], [round(j*.06013,3) for j in plt.xticks()[0][1:-1]], fontsize = 8)
    #     plt.tight_layout()
    #     # plt.show()
    #     figure.text(0.5/8.5, 0.5/11., str(i+1), ha='center', fontsize=8)

    #     pdf.savefig()
    #     plt.close()

    # pdf.close()


indir = "/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/haspin_stripe_linescans/analysis"
outdir = "/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/haspin_stripe_linescans/quantifying_condensates_plots/"

# outdir = "/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/haspin_stripe_linescans/MCF10A"
# indir = "/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/MCF10A/MCF10A_CPC_analysis/analysis/linescans"

# outdir = "/Users/smgroves/Box/CPC_Model_Project/CPC_condensate_images/MCF10A/MCF10A_CPC_analysis/analysis/linescans/count_peak_plots/"
if False:
    all_results = pd.DataFrame(
        columns=[
            "image_num",
            "chr_num",
            "chr_length",
            "IC_peaks",
            "kt_peak",
            "l_arm_length",
            "r_arm_length",
            "left_peaks",
            "right_peaks",
            "chr_per_1.6um_L",
            "chr_per_1.6um_R",
        ]
    )
    for image in range(10):
        # if (image == 22) or (image == 39):
        #     continue
        try:
            print(image)
            results = count_peaks(
                indir, image=image, rescaled=True, max_width=800, min_width=100, prominence=15
            )
            # sns.countplot(data=results, x="chr_per_1.6um_L")
            # plt.title("Number of Condensates per 1.6um L")
            # plt.savefig(f"{outdir}/{image}_L.png")
            # plt.close()

            # sns.countplot(data=results, x="chr_per_1.6um_R")
            # plt.title("Number of Condensates per 1.6um R")
            # plt.savefig(f"{outdir}/{image}_R.png")
            # plt.close()

            # cross = pd.crosstab(results["chr_per_1.6um_L"],results["chr_per_1.6um_R"])
            # sns.heatmap(cross)
            # plt.title("Number of Condensates per 1.6um L and R")
            # plt.ylabel("Right")
            # plt.xlabel("Left")
            # plt.savefig(f"{outdir}/{image}_crosstab.png")
            # plt.close()

            all_results = pd.concat([all_results, results], ignore_index=True)
            results.to_csv(f"{indir}/count_peaks_image{image}_.csv")
        except FileNotFoundError:
            print(f"File not found for image {image}")
    all_results.to_csv(f"{indir}/all_count_peaks.csv")

# cross = pd.crosstab(all_results["chr_per_1.6um_L"],
#                     all_results["chr_per_1.6um_R"])
# sns.heatmap(cross)
# plt.title("Number of Condensates per 1.6um L and R")
# plt.ylabel("Right")
# plt.xlabel("Left")
# plt.savefig(f"{outdir}/images10_crosstab.png")
# plt.close()

# melted_results = pd.melt(
#     all_results, value_vars=["chr_per_1.6um_L", "chr_per_1.6um_R"], id_vars="image_num"
# )

# melted_results = melted_results.loc[
#     [np.isclose(1.6, i, atol=0.2) for i in melted_results["length"]]
# ]

# sns.countplot(data=melted_results, x="value")
# plt.title(
#     "Number of chromosomes per 1.6um from IC across all images  \n IC condensates were removed"
# )
# plt.ylabel("Frequency")
# plt.xlabel("Chromosomes per 1.6um from IC")
# plt.savefig(f"{outdir}/image10_L_R.png")
# plt.close()
# plt.show()

# sns.countplot(data=melted_results, x="value", hue="variable")
# plt.title(
#     "Number of chromosomes per 1.6um from IC across all images  \n IC condensates were removed"
# )
# plt.ylabel("Frequency")
# plt.xlabel("Chromosomes per 1.6um from IC")
# plt.savefig(f"{outdir}/image10_L_R_split.png")
# plt.close()

# sns.countplot(data = melted_results, x = 'value', hue = "image_num")
# plt.title("Number of chromosomes per 1.6um from IC across all images  \n IC condensates were removed")
# plt.ylabel("Frequency")
# plt.xlabel("Chromosomes per 1.6um from IC")
# plt.savefig(f"{outdir}/images[0125789]_L_R_by_image.png")
# plt.close()

# num_per_domain = []
# for i,r in all_results.iterrows():
#     num_per_domain.append(r["chr_per_1.6um_L"])
#     num_per_domain.append(r["chr_per_1.6um_R"])

# plt.hist(num_per_domain)
# plt.savefig(f"{outdir}/images[017]_L_R.png")

# melted_results = pd.melt(all_results,  value_vars=["chr_per_1.6um_L","chr_per_1.6um_R"], id_vars="image_num")
# print(melted_results)

# # sns.histplot(data = melted_results, x = 'value', bins = 20)
# # plt.title("Chromosome arm lengths")
# # # plt.ylabel("Frequency")
# # plt.xlabel("Arm length (um)")
# # plt.savefig(f"{outdir}/arm_lengths_0125789.png")
# # plt.close()
# # plt.show()

# melt_by_image = pd.crosstab(melted_results['image_num'], melted_results['value'], normalize ='index')
# # print(melt_by_image)
# melt_by_image['image_num'] = melt_by_image.index
# melt_by_image.columns = ['0','1','2','3','4','image_num']
# melt_by_image = pd.melt(melt_by_image,  value_vars=['1','2','3','4'], id_vars="image_num")
# # print(melt_by_image)
# sns.barplot(data = melt_by_image, x = "variable", y = "value",label = "mean +/- 95% CI")
# plt.title(f"Number of droplets per 1.6um from IC across all images \n  n = {len(melted_results)}, X = simulation value")
# plt.ylabel("Frequency of chromosomes (normalized by image)")
# plt.xlabel("Droplets per 1.6um from IC")
# for x,val in enumerate([0.530232558139535,0.362790697674419,0.0953488372093023,0.0116279069767442]):
#     plt.annotate("X", (.98*x, val), )
# plt.ylim(0, .6)
# plt.legend()
# plt.savefig(f"{outdir}/annot_norm_barplot_images[0125789]_L_R_by_image.png")
# plt.close()
# plt.show()


# atol = .3

# melted_results = pd.melt(all_results,  value_vars=["chr_per_1.6um_L","chr_per_1.6um_R"], id_vars=["image_num", 'l_arm_length','r_arm_length'])
# length = []
# for i,r in melted_results.iterrows():
#     if r['variable'] == "chr_per_1.6um_L":
#         length.append(r["l_arm_length"])
#     elif r['variable'] == "chr_per_1.6um_R":
#         length.append(r["r_arm_length"])
# melted_results["length"] = length

# melted_results = melted_results.loc[[np.isclose(1.6, i, atol = atol) for i in melted_results['length']]]
# print(len(melted_results))

# melt_by_image = pd.crosstab(melted_results['image_num'], melted_results['value'], normalize ='index')
# # print(melt_by_image)
# melt_by_image['image_num'] = melt_by_image.index
# melt_by_image.columns = ['0','1','2','3','4','image_num']
# melt_by_image = pd.melt(melt_by_image,  value_vars=['1','2','3','4'], id_vars="image_num")
# # print(melt_by_image)
# sns.barplot(data = melt_by_image, x = "variable", y = "value", label = "mean +/- 95% CI")
# plt.title(f"Number of droplets per chromosome arm \n chr length tol = 1.6um+/-{atol}, n = {len(melted_results)}")
# plt.ylabel("Frequency of chromosomes (normalized by image)")
# plt.xlabel("Droplets per 1.6um from IC")
# for x,val in enumerate([0.530232558139535,0.362790697674419,0.0953488372093023,0.0116279069767442]):
#     plt.annotate("X", (.98*x, val))
# # plt.ylim(0, .6)
# plt.legend()
# plt.savefig(f"{outdir}/annot_norm_barplot_images[0125789]_L_R_by_image_tol_{atol}.png")
# plt.close()
# plt.show()


# melted_results = pd.melt(all_results,  value_vars=["chr_per_1.6um_L","chr_per_1.6um_R"], id_vars=["image_num", 'l_arm_length','r_arm_length'])
# length = []
# for i,r in melted_results.iterrows():
#     if r['variable'] == "chr_per_1.6um_L":
#         length.append(r["l_arm_length"])
#     elif r['variable'] == "chr_per_1.6um_R":
#         length.append(r["r_arm_length"])
# melted_results["length"] = length

# melted_results = melted_results.loc[melted_results['length']>=1.6]
# print(len(melted_results))

# melt_by_image = pd.crosstab(melted_results['image_num'], melted_results['value'], normalize ='index')
# # print(melt_by_image)
# melt_by_image['image_num'] = melt_by_image.index
# melt_by_image.columns = ['0','1','2','3','4','image_num']
# melt_by_image = pd.melt(melt_by_image,  value_vars=['1','2','3','4'], id_vars="image_num")
# # print(melt_by_image)
# sns.barplot(data = melt_by_image, x = "variable", y = "value", label = "mean +/- 95% CI")
# plt.title(f"Number of droplets per 1.6um from IC across all images \n chr arm length >= 1.6um, n = {len(melted_results)}")
# plt.ylabel("Frequency of chromosomes (normalized by image)")
# plt.xlabel("Droplets per 1.6um from IC")
# for x,val in enumerate([0.530232558139535,0.362790697674419,0.0953488372093023,0.0116279069767442]):
#     plt.annotate("X", (.98*x, val))
# # plt.ylim(0, .6)
# plt.legend()
# plt.savefig(f"{outdir}/annot_norm_barplot_images[0125789]_L_R_by_image_geq_1.6.png")
# plt.close()

# %%
