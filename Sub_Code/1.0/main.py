import argparse
import os
import datetime
from tool import Sub_Counts

# parse command line args
parser = argparse.ArgumentParser()
parser.description = "此文件用于字幕统计"
parser.add_argument("-input_path", default=r'D:\PythonProject\Sub_Code\data', help="path to input dataset")
parser.add_argument("-save_path",  default=r'D:\PythonProject\Sub_Code\save', help="path to output save")
args = parser.parse_args()


def path_check(input_path, save_path):
    while not os.path.exists(input_path):
        input_path = (str(input("Input path is not exists!Please input correct path: ")))
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    return input_path, save_path


def main():
    dataset, save = path_check(args.input_path, args.save_path)
    start = datetime.datetime.now()
    sub = Sub_Counts(dataset, save)
    sub.mainloop()
    end = datetime.datetime.now()
    print("Running time:", end-start)


if __name__ == '__main__':
    main()


