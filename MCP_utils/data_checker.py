import ast
from itertools import count
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np


class FILE_PROCESSOR:
    def __init__(self, filenames=None):
        if filenames is None:
            self.f_sh1_bcg_name = "logs/data/SH1_BCG.csv"
            self.f_sh2_bcg_name = "logs/data/SH2_BCG.csv"
            self.f_sh2_fsr_name = "logs/data/SH2_FSR.csv"
            self.f_spo2_name = "logs/data/SPO2.csv"
            self.f_temp_name = "logs/data/Temp.csv"
            self.f_nibp_name = "logs/data/NIBP.csv"
        else:
            self.f_sh1_bcg_name = filenames[0]
            self.f_sh2_bcg_name = filenames[1]
            self.f_sh2_fsr_name = filenames[2]
            self.f_spo2_name = filenames[3]
            self.f_temp_name = filenames[4]
            self.f_nibp_name = filenames[5]
        self.filenames = filenames

    def check_len_of_data(self):
        self.len_info = {"SH1_BCG_TOTAL": 0,
                         "SH2_BCG_TOTAL": 0,
                         "SH2_FSR_TOTAL": 0,
                         "SPO2_TOTAL": 0,
                         "TEMP_TOTAL": 0,
                         "NIBP_TOTAL": 0,
                         "SH1_BCG_INCORRECT": 0,
                         "SH2_BCG_INCORRECT": 0,
                         "SH2_FSR_INCORRECT": 0,
                         "SPO2_INCORRECT": 0,
                         "TEMP_INCORRECT": 0,
                         "NIBP_INCORRECT": 0}

        for file in [self.f_sh1_bcg, self.f_sh2_bcg]:
            for line in file:
                if file == self.f_sh1_bcg:
                    self.len_info["SH1_BCG_TOTAL"] += 1
                else:
                    self.len_info["SH2_BCG_TOTAL"] += 1
                timestamp = line.split(",", 1)[0]
                data = line.split(",", 1)[1]
                byte_data = ast.literal_eval(data)
                if len(byte_data) < 500 or len(byte_data) > 504:
                    print(timestamp, len(byte_data))
                    if file == self.f_sh1_bcg:
                        self.len_info["SH1_BCG_INCORRECT"] += 1
                    else:
                        self.len_info["SH2_BCG_INCORRECT"] += 1
        for line in self.f_sh2_fsr:
            self.len_info["SH2_FSR_TOTAL"] += 1
            timestamp = line.split(",", 1)[0]
            data = line.split(",", 1)[1]
            byte_data = ast.literal_eval(data)
            if len(byte_data) != 10:
                print(timestamp, len(byte_data))
                self.len_info["SH2_FSR_INCORRECT"] += 1
        for line in self.f_spo2:
            self.len_info["SPO2_TOTAL"] += 1
            timestamp = line.split(",", 1)[0]
            data = line.split(",", 1)[1]
            byte_data = ast.literal_eval(data)
            if len(byte_data) != 500:
                print(timestamp, len(byte_data))
                self.len_info["SPO2_INCORRECT"] += 1
        for line in self.f_temp:
            self.len_info["TEMP_TOTAL"] += 1
            timestamp = line.split(",", 1)[0]
            data = line.split(",", 1)[1]
            byte_data = ast.literal_eval(data)
            if len(byte_data) != 2:
                print(timestamp, len(byte_data))
                self.len_info["TEMP_INCORRECT"] += 1
        for line in self.f_nibp:
            self.len_info["NIBP_TOTAL"] += 1
            timestamp = line.split(",", 1)[0]
            data = line.split(",", 1)[1]
            byte_data = ast.literal_eval(data)
            if len(byte_data) != 8:
                print(timestamp, len(byte_data))
                self.len_info["NIBP_INCORRECT"] += 1
        print("Data Length Check Results : \n" +
              f"SH1 BCG : {self.len_info['SH1_BCG_INCORRECT']}/{self.len_info['SH1_BCG_TOTAL']}\n" +
              f"SH2 BCG : {self.len_info['SH2_BCG_INCORRECT']}/{self.len_info['SH2_BCG_TOTAL']}\n" +
              f"SH2 FSR : {self.len_info['SH2_FSR_INCORRECT']}/{self.len_info['SH2_FSR_TOTAL']}\n" +
              f"SPO2    : {self.len_info['SPO2_INCORRECT']}/{self.len_info['SPO2_TOTAL']}\n" +
              f"TEMP    : {self.len_info['TEMP_INCORRECT']}/{self.len_info['TEMP_TOTAL']}\n"
              f"NIBP    : {self.len_info['NIBP_INCORRECT']}/{self.len_info['NIBP_TOTAL']}")

    def check_interval_of_data(self):
        all_vals = []
        group_labels = ["SH1_BCG", "SH2_BCG", "SH2_FSR", "SPO2", "TEMP", "NIBP"]
        for file in [self.f_sh1_bcg, self.f_sh2_bcg, self.f_sh2_fsr, self.f_spo2, self.f_temp, self.f_nibp]:
            first_timestamp = True
            prev_timestamp = 0
            index = count(0, 1)
            y_vals = []
            x_vals = []
            print(f"Checking Intervals for filename {file.name}")
            for line in file:
                timestamp = line.split(",", 1)[0]
                if first_timestamp is True:
                    first_timestamp = False
                    prev_timestamp = timestamp
                    continue
                x_vals.append(next(index))
                diff = float(timestamp) - float(prev_timestamp)
                y_vals.append(diff)
                prev_timestamp = timestamp
            data_plots = [go.Scatter(x=x_vals,
                                     y=y_vals,
                                     mode='lines',
                                     name=file.name,
                                     line=dict(width=1))]
            data_figure = go.Figure(data=data_plots,
                                    layout=go.Layout(title=file.name,
                                                     xaxis=dict(title="Index"),
                                                     yaxis=dict(title="Interval (s)")))
            data_figure.show()
            all_vals.append(y_vals)
        fig = ff.create_distplot(all_vals, group_labels, show_hist=False)
        fig.show()

    def parse_and_plot_data(self, file):
        if file in [self.f_sh1_bcg, self.f_sh2_bcg]:
            print(f"Parsing BCG Data for {file.name}")
            x_vals = []
            y_vals = []
            counter = 0
            fig = make_subplots(rows=2, cols=4)
            row = 1
            column = 1
            for line in file:
                print(f"Counter : {counter}")
                timestamp = line.split(",", 1)[0]
                data = line.split(",", 1)[1]
                byte_data = ast.literal_eval(data)
                bcg_arr = []
                ts_arr = []
                for i in range(0, len(byte_data), 2):
                    ts = float(timestamp) + i/2*4/1000
                    bcg_val = (byte_data[i] << 8) + byte_data[i + 1]
                    x_vals.append(ts)
                    ts_arr.append(ts)
                    y_vals.append(bcg_val)
                    bcg_arr.append(bcg_val)
                counter += 1
                if counter % 5000 == 0:  # Plot every 1000th BCG data
                    print("Adding plot for BCG")
                    fig.add_trace(go.Scatter(x=ts_arr,
                                             y=bcg_arr,
                                             mode='lines',
                                             name=f"BCG_{counter}",
                                             line=dict(width=1)),
                                             row=row, col=column)
                    column += 1
                    if column == 5:
                        row += 1
                        column = 1
            print("Parsing completed. Plotting ...")
            bcg_data = np.array(y_vals)
            diff = np.diff(bcg_data)
            print(f"BCG change max magnitude : {np.max(np.abs(diff))}")
            fig.update_layout(height=1000, width=1000, title_text="BCG Data")
            fig.show()
        if file is self.f_sh2_fsr:
            print(f"Parsing FSR Data for {file.name}")
            x_vals = []
            y_vals = []
            for line in file:
                timestamp = line.split(",", 1)[0]
                data = line.split(",", 1)[1]
                byte_data = ast.literal_eval(data)
                for i in range(0, len(byte_data), 2):
                    ts = float(timestamp) + i/2*4/1000
                    fsr = ((byte_data[i] - 80) << 8) + byte_data[i + 1]
                    x_vals.append(ts)
                    y_vals.append(fsr)
            fig = ff.create_distplot([y_vals], ["FSR"], show_hist=False)
            fig.show()
        if file is self.f_temp:
            print(f"Parsing Temperature Data for {file.name}")
            x_vals = []
            y_vals = []
            for line in file:
                timestamp = line.split(",", 1)[0]
                data = line.split(",", 1)[1]
                byte_data = ast.literal_eval(data)
                for i in range(0, len(byte_data), 2):
                    ts = float(timestamp) + i/2*4/1000
                    adc_raw = (byte_data[i] << 8) + byte_data[i + 1]
                    x_vals.append(ts)
                    y_vals.append(adc_raw)
            fig = ff.create_distplot([y_vals], ["T_ADC_RAW"], show_hist=False)
            fig.show()
        if file is self.f_nibp:
            print(f"Parsing NiBP Data for {file.name}")
            x_vals = []
            errorCodes_vals = []
            sysBP_vals = []
            diaBP_vals = []
            hr_vals = []
            for line in file:
                timestamp = line.split(",", 1)[0]
                data = line.split(",", 1)[1]
                byte_data = ast.literal_eval(data)
                for i in range(0, len(byte_data), 8):
                    ts = float(timestamp) + i/2*4/1000
                    errorCode = (byte_data[i] << 8) + byte_data[i + 1]
                    sysBP = (byte_data[i + 2] << 8) + byte_data[i + 3]
                    diaBP = (byte_data[i + 4] << 8) + byte_data[i + 5]
                    hr = (byte_data[i + 6] << 8) + byte_data[i + 7]
                    x_vals.append(ts)
                    errorCodes_vals.append(errorCode)
                    sysBP_vals.append(sysBP)
                    diaBP_vals.append(diaBP)
                    hr_vals.append(hr)
            data_plots = [go.Scatter(x=x_vals,
                                     y=errorCodes_vals,
                                     mode='lines',
                                     name="Error Codes",
                                     line=dict(width=1)),
                          go.Scatter(x=x_vals,
                                     y=sysBP_vals,
                                     mode='lines',
                                     name="SYS BP",
                                     line=dict(width=1)),
                          go.Scatter(x=x_vals,
                                     y=diaBP_vals,
                                     mode='lines',
                                     name = "DIA BP",
                                     line=dict(width=1)),
                          go.Scatter(x=x_vals,
                                     y=hr_vals,
                                     mode='lines',
                                     name = "HR",
                                     line=dict(width=1))]

            data_figure = go.Figure(data=data_plots,
                                    layout=go.Layout(title=file.name,
                                                     xaxis=dict(title="Index"),
                                                     yaxis=dict(title="Value")))
            data_figure.show()
        if file is self.f_spo2:
            print(f"Parsing SpO2 Data for {file.name}")
            x_vals = []
            spo2_vals = []
            pr_vals = []
            finger_vals = []
            probe_vals = []
            pleth_vals = []
            counter = 0
            fig = make_subplots(rows=2, cols=4)
            row = 1
            column = 1

            for line in file:
                timestamp = line.split(",", 1)[0]
                data = line.split(",", 1)[1]
                byte_data = ast.literal_eval(data)
                pleth_arr = []
                ts_arr = []
                for i in range(0, len(byte_data), 5):
                    if counter == 0 and i == 0:
                        continue
                    ts = float(timestamp) + i/2*4/1000
                    x_vals.append(ts)
                    ts_arr.append(ts)
                    if (byte_data[i] & (1 << 5)):
                        probe = 0
                    else:
                        probe = 1
                    probe_vals.append(probe)
                    pleth = byte_data[i + 1]
                    pleth_vals.append(pleth)
                    pleth_arr.append(pleth)
                    if (byte_data[i + 2] & (1 << 4)):
                        finger = 0
                    else:
                        finger = 1
                    finger_vals.append(finger)
                    pr = (byte_data[i + 3]) + ((byte_data[i + 2] & 0x40) << 1)
                    pr_vals.append(pr)
                    spo2 = byte_data[i + 4]
                    spo2_vals.append(spo2)
                if counter % 5000 == 0:  # Plot every 100th pleth data
                    fig.add_trace(go.Scatter(x=ts_arr,
                                             y=pleth_arr,
                                             mode='lines',
                                             name=f"Pleth_{counter}",
                                             line=dict(width=1)),
                                             row=row, col=column)
                    column += 1
                    if column == 5:
                        row += 1
                        column = 1
                    # data_plots = [go.Scatter(x=x_vals,
                    #                          y=pleth_arr,
                    #                          mode='lines',
                    #                          name="Pleth",
                    #                          line=dict(width=1))]
                    # data_figure = go.Figure(data=data_plots,
                    #                         layout=go.Layout(title=f"Pleth Plot {counter}",
                    #                                          xaxis=dict(title="Index"),
                    #                                          yaxis=dict(title="Pleth")))
                counter += 1
                # if counter == 100:
                #     break
            fig.update_layout(height=1000, width=1000, title_text="Pleth Data")
            fig.show()
            pr_counts = {}
            for i in range(0, max(pr_vals) + 1):
                count_i = pr_vals.count(i)
                if count_i > 0:
                    pr_counts[i] = count_i
            spo2_counts = {}
            for i in range(0, max(spo2_vals) + 1):
                count_i = spo2_vals.count(i)
                if count_i > 0:
                    spo2_counts[i] = count_i
            finger_counts = {}
            for i in range(0, max(finger_vals) + 1):
                count_i = finger_vals.count(i)
                if count_i > 0:
                    finger_counts[i] = count_i
            probe_counts = {}
            for i in range(0, max(probe_vals) + 1):
                count_i = probe_vals.count(i)
                if count_i > 0:
                    probe_counts[i] = count_i
            print("""----- PR Count Info -----\n"""
                  f"""{pr_counts}\n"""
                  """----- PR Count Info -----\n"""
                  """----- SPO2 Count Info -----\n"""
                  f"""{spo2_counts}\n"""
                  """----- SPO2 Count Info -----\n"""
                  """----- Finger Count Info -----\n"""
                  f"""{finger_counts}\n"""
                  """----- Finger Count Info -----\n"""
                  """----- Probe Count Info -----\n"""
                  f"""{probe_counts}\n"""
                  """----- Probe Count Info -----\n""")
            pleth_data = np.array(pleth_vals)
            diff = np.diff(pleth_data)
            print(f"Pleth change magnitude : {np.max(np.abs(diff))}")
            std_dev = np.std(pleth_data)
            if std_dev < 1:  # Threshold for very flat data (no signal)
                print("Signal too flat, likely invalid")
            # data_plots = [go.Scatter(x=x_vals,
            #                          y=pleth_vals,
            #                          mode='lines',
            #                          name="Pleth",
            #                          line=dict(width=1))]
            # data_figure = go.Figure(data=data_plots,
            #                         layout=go.Layout(title="Pleth Plot",
            #                                          xaxis=dict(title="Index"),
            #                                          yaxis=dict(title="Pleth")))
            # data_figure.show()
            # df = pd.DataFrame({"Pleth": pleth_vals})
            # fig = px.histogram(df, x="Pleth", nbins=256)
            # fig.show()

    def check_data_quality(self, files):
        for file in files:
            self.parse_and_plot_data(file)

    def open_files(self):
        self.f_sh1_bcg = open(self.f_sh1_bcg_name)
        self.f_sh2_bcg = open(self.f_sh2_bcg_name)
        self.f_sh2_fsr = open(self.f_sh2_fsr_name)
        self.f_spo2 = open(self.f_spo2_name)
        self.f_temp = open(self.f_temp_name)
        self.f_nibp = open(self.f_nibp_name)
        self.files = [self.f_sh1_bcg, self.f_sh2_bcg, self.f_sh2_fsr, self.f_spo2, self.f_temp, self.f_nibp]

    def process_data(self):
        # Check length of all frames #
        # self.check_len_of_data()

        # Check for missing dataframes #
        # self.check_interval_of_data()

        # Plot all data
        # self.check_data_quality([self.f_sh1_bcg])
        # self.check_data_quality([self.f_sh2_bcg])
        self.check_data_quality([self.f_sh2_fsr])
        # self.check_data_quality([self.f_temp])
        # self.check_data_quality([self.f_nibp])
        # self.check_data_quality([self.f_spo2])
        pass

    def close_files(self):
        self.f_sh1_bcg.close()
        self.f_sh2_bcg.close()
        self.f_sh2_fsr.close()
        self.f_spo2.close()
        self.f_temp.close()
        self.f_nibp.close()


if __name__ == "__main__":
    time_now = "2024_11_12_19:58:13"
    filenames = [f"logs/data_{time_now}/SH1_BCG.csv",
                 f"logs/data_{time_now}/SH2_BCG.csv",
                 f"logs/data_{time_now}/SH2_FSR.csv",
                 f"logs/data_{time_now}/SPO2.csv",
                 f"logs/data_{time_now}/Temp.csv",
                 f"logs/data_{time_now}/NIBP.csv"]
    f_processor = FILE_PROCESSOR(filenames)
    f_processor.open_files()
    f_processor.process_data()
    f_processor.close_files()
