import subprocess
import string
import plotly.graph_objects as go
import random
import time
import os
import datetime
import pandas as pd


def save_time_taken_to_file(time_taken):
    save_file = open(save_file_name, "a")
    save_file.write(f"{time_taken}\n")
    save_file.close()


def measure_function_execution_time(func, *args):
    start = time.time()
    func(*args)
    end = time.time()
    time_taken = round((end - start) * 1000, 2)
    print(f"Time taken to write {args[0]}: {time_taken} ms")
    return time_taken


def check_sd_card():
    # Currently you can only check if the SD card is present or not
    # after it is mounted
    command = "ls /media/dozee"
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    output, _ = process.communicate()
    if len(output) == 0:
        print("No SD card found")
        return False
    sd_card_path = "/media/dozee/" + output.decode('utf-8')[:-1].strip()
    print(f"SD card found at /media/dozee/{sd_card_path}")
    return sd_card_path


def create_file_and_insert_data(filename, type_of_data):
    f = open(filename, "w")
    if type_of_data in ["PZ", "KZ"]:
        for _ in range(0, 125):
            f.write(bcg)
    elif type_of_data == "FS":
        f.write(fsr)
    f.close()


def get_file_name(directory, file_num, type_of_data):
    return f"{directory}/{type_of_data}_{file_num}.pz"


write_dat = create_file_and_insert_data
profile_t = measure_function_execution_time


def run_test_on_sd_card(sd_card_path, folder_start=1000, folder_count=100):
    for folder_id in range(folder_start, folder_start + folder_count):
        directory = sd_card_path + f"/R{folder_id}"
        os.mkdir(directory)
        for file_num in range(0, 150):
            file_name = get_file_name(directory, file_num, "PZ")
            save_time_taken_to_file(profile_t(write_dat,
                                              file_name,
                                              "PZ"))
            file_name = get_file_name(directory, file_num, "KZ")
            save_time_taken_to_file(profile_t(write_dat,
                                              file_name,
                                              "KZ"))
        directory = sd_card_path + f"/F{folder_id}"
        os.mkdir(directory)
        for file_num in range(0, 150):
            file_name = get_file_name(directory, file_num, "FS")
            save_time_taken_to_file(profile_t(write_dat,
                                              file_name,
                                              "FS"))


def plot_data(title, x_vals, y_vals):
    data_plots = [go.Scatter(x=x_vals,
                             y=y_vals,
                             mode='lines',
                             name=title,
                             line=dict(width=1))]
    data_figure = go.Figure(data=data_plots,
                            layout=go.Layout(title=title,
                                             xaxis=dict(title="Index"),
                                             yaxis=dict(title="Tick Interval (ms)")))
    data_figure.show()


if __name__ == "__main__":
    # bcg = ''.join(random.choices(string.ascii_letters,
    #                              k=500))  # initializing size of string
    # fsr = ''.join(random.choices(string.ascii_letters,
    #                              k=100))  # initializing size of string
    #
    # save_file_name = str(datetime.datetime.now()).replace(" ", "_")
    #
    # sd_card_path = check_sd_card()
    # if sd_card_path is False:
    #     exit(0)
    #
    # run_test_on_sd_card(sd_card_path,
    #                     folder_start=4050,
    #                     folder_count=10)

    df = pd.read_csv("2024-12-13_13:58:16.094724")
    # print(df)
    x = list(df.index.values)
    y = list(df["TimeTaken"].values)
    plot_data("Time Taken", x, y)
