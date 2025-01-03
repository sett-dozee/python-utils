import shutil

log_file = '100.log'

if __name__ == "__main__":
    bak_file = log_file + '.bak'
    shutil.copy(log_file, bak_file)
    line_count = 0
    file_count = 1
    print("Current file count :", file_count)
    f = open(bak_file + '.' + str(file_count), 'a')
    for line in open(bak_file, errors='ignore'):
        line_count += 1
        f.write(line)
        if line_count % 20000 == 0:
            f.close()
            file_count += 1
            f = open(bak_file + '.' + str(file_count), 'a')
            print("Current file count :", file_count)
