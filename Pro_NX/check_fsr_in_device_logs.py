import plotly.figure_factory as ff
import plotly.express as px
from datetime import datetime


dt_fmt = "%Y-%m-%d %H:%M:%S.%f"


def convert_datetime_string_to_epoch(input, format):
    utc_time = datetime.strptime(input, format)
    epoch_time = (utc_time - datetime(1970, 1, 1)).total_seconds()
    return epoch_time


def check_all_fsr_vals(filename):
    file = open(filename, "r", errors="ignore")
    total_raw_fsr = 0
    invalid_fsr_count = 0
    invalid_fsr_median_count = 0
    fsr_count_acquired_1_sec = 0
    fsr_count_acquired_1_sec_list = []
    fsr_count_acquired_15_sec = 0
    fsr_count_acquired_15_sec_list = []
    invalid_fsr_count = 0
    raw_fsr_list = []
    fsr_median_list_1_sec = []
    fsr_median_list_15_sec = []
    fsr_mean_list_fpa = []
    ts_last = 0
    ts_diff_list = []

    for line in file:
        if "rst:0x" in line:
            ts_last = 0
        if "AVERAGE FSR VAL 1 SEC" in line:
            mean_fsr = int(line.split(" = ")[-1].split(",")[0])
            fsr_mean_list_fpa.append(mean_fsr)
        if "FSR RX INDEX" in line:
            total_raw_fsr += 1
            try:
                parts = line.split(", ")
                fsr = int(parts[-1])
                ts = parts[0].split(" I ")[0][1:-1]
                raw_fsr_list.append(fsr)
                if fsr < 700 or fsr > 1000:
                    print(f"FSR = {fsr:<3} @ {ts}")
                    invalid_fsr_count += 1
            except:
                parts = line.split(" ")
                fsr = int(parts[-1])
                ts = parts[0].split(" I ")[0][1:-1]
                raw_fsr_list.append(fsr)
                if fsr < 700 or fsr > 1000:
                    print(f"FSR = {fsr} @ {ts}")
                    invalid_fsr_count += 1

        if "FSR_COUNT" in line:
            parts = line.split(": ")
            median_fsr = int(parts[-1])
            fsr_median_list_1_sec.append(median_fsr)
            ts = parts[0].split(" I ")[0][1:-1]
            fsr_count = int(parts[-2].split(" ")[0])
            fsr_count_acquired_1_sec_list.append(fsr_count)
            # print(median_fsr)
            fsr_count_acquired_15_sec += 1
            if median_fsr < 700 or median_fsr > 1000:
                print(f"1 SEC FSR MEDIAN = {median_fsr} @ {ts}")
            if fsr_count != 5:
                print(f"1 SEC FSR_COUNT = {fsr_count} @ {ts}")
        if "15 SEC FSR MEDIAN" in line:
            parts = line.split(" : ")
            fsr_median_15_sec = int(parts[-1])
            fsr_median_list_15_sec.append(fsr_median_15_sec)
            ts = parts[0].split(" I ")[0][1:-1]
            ts_conv = convert_datetime_string_to_epoch(ts, dt_fmt)
            fsr_count_acquired_15_sec_list.append(fsr_count_acquired_15_sec)
            fsr_count_acquired_15_sec = 0
            if ts_last != 0:
                ts_diff = round(ts_conv - ts_last, 4)
                ts_diff_list.append(ts_diff)
                # if ts_diff > 30:
                #     print(ts)
            ts_last = ts_conv
            if fsr_median_15_sec < 700 or fsr_median_15_sec > 1000:
                print(f"15 SEC FSR MEDIAN = {fsr_median_15_sec} @ {ts}")
                invalid_fsr_median_count += 1
        # if "FSR COUNT ACQUIRED" in line:
        #     parts = line.split(" : ")
        #     fsr_count = int(parts[-1])
        #     ts = parts[0].split(" I ")[0][1:-1]
        #     # print(f"FSR COUNT ACQUIRED = {fsr_count} @ {ts}")
        #     print(line)
        #     if fsr_count < 15:
        #         # print("FSR COUNT less than 15")
        #         fsr_count_acquired  += 1
    invalid_fsr_statement = 'NONE' if invalid_fsr_count == 0 else invalid_fsr_count
    invalid_median_statement = 'NONE' if invalid_fsr_median_count == 0 \
            else invalid_fsr_median_count
    fsr_count_acquired_1_sec = 'NONE' if fsr_count_acquired_1_sec == 0 else fsr_count_acquired_1_sec
    print(f"INVALID FSR DISCRETE                | {invalid_fsr_statement}/{total_raw_fsr}")
    print(f"INVALID FSR MEDIAN                  | {invalid_median_statement}")
    print(f"FSR MEDIAN COUNT 1 SEC/15 SEC       | {len(fsr_median_list_1_sec)}/{len(fsr_median_list_15_sec)}")
    # print(f"LESS THAN 15 FSR COUNT ACQUIRED | {fsr_count_acquired}")
    file.close()

    fig0 = px.scatter(x=range(0, len(fsr_mean_list_fpa)), y=fsr_mean_list_fpa)
    fig0.show()
    fig1 = px.scatter(x=range(0, len(fsr_count_acquired_15_sec_list)), y=fsr_count_acquired_15_sec_list)
    fig1.show()
    fig2 = px.scatter(x=range(0, len(fsr_count_acquired_1_sec_list)), y=fsr_count_acquired_1_sec_list)
    fig2.show()
    fig5 = ff.create_distplot([fsr_count_acquired_1_sec_list], ['FSR ACQUIRED every 1 SEC'])
    fig5.show()
    fig3 = ff.create_distplot([raw_fsr_list,
                               fsr_median_list_1_sec,
                               fsr_median_list_15_sec],
                              ['RAW FSR',
                               'FSR MEDIAN 1 SEC',
                               'FSR MEDIAN 15 SEC'])
    fig3.show()
    fig3.write_image('./fsr_vals_dist_plot.png')
    fig4 = ff.create_distplot([ts_diff_list], ['FSR WRITE INTERVAL'])
    fig4.show()


if __name__ == "__main__":
    check_all_fsr_vals("/home/dozee/Dozee/Git-Repos/dozee_pro_nx_48/50")
    # check_all_fsr_vals("/home/dozee/20")
