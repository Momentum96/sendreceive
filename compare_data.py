import os

path = "C:/Users/USER/Desktop/BANF/00. 업무자료/02. 내부자료/03. Software/01. data/"
dir1 = path + "AWS_S3_Files/"
dir2 = path + "ClientPC_Files/"

file_list = os.listdir(dir1)

for file in file_list:
    print("=" * 100)
    print(file + " start")
    with open(dir1 + file, "r") as file1, open(dir2 + file) as file2:
        # Read the entire contents of both files and split them by tabs
        same = 0
        dif = 0

        while True:
            line1 = file1.readline()
            line2 = file2.readline()
            if not line1:
                break
            if line1 == line2:
                same += 1
            else:
                dif += 1
        print("same : " + str(same))
        print("dif : " + str(dif))

    print("=" * 100)
