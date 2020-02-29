import os
import re
import datetime


class Sub_Counts(object):
    """

    :param dataset: input dirs/files path
    :param save_path: output file save path
    """
    def __init__(self, dataset, save_path):
        self.dataset = dataset
        self.save_path = save_path

    def mainloop(self):
        file_names = []
        str_types = []
        video_len = []
        word_list = []
        word_frequency = []
        # 指定字幕类型（包含英文）
        type_filter = ["eng", "chs&eng", "英文", "简体&英文", "繁体&英文"]

        files_path = self.find_srt_file(self.dataset)
        print('File is loading and processing....')
        for file in files_path:
            # print(file) #绝对路径
            file_name = file.split('\\', -1)[-1]
            file_name = ''.join(file_name.rsplit('.', 2)[0])
            str_type = file.split('.', -1)[-2]
            if str_type in type_filter:
                file_names.append(file_name)
                str_types.append(str_type)

                # 读入文件 正则化删除中文
                reader = open(file, 'r', encoding='gbk', errors='ignore')
                lines = reader.readlines() # 文本列表
                new_lines = self.OnlyChar(lines)

                # 获取视频长度
                video_time = self.get_video_time(new_lines)
                video_time_in_minute = int(video_time[0] + video_time[1]) * 60 + int(video_time[2] + video_time[3])
                # print('视频长度：', video_time, end=' ')
                words_count = self.count_words(new_lines)
                # print('总的单词量：', words_count)
                frequency = words_count / video_time_in_minute
                frequency = round(frequency, 2)
                video_len.append(video_time)
                word_list.append(words_count)
                word_frequency.append(frequency)
                reader.close()
                print('Y-File <%s> is finished!. ' % file)
            else:
                print('N-File <%s> is not the specified type ! ' % file)
        print("%d subtitle files were processed，saving....." % len(file_names))
        self.save(save_path=self.save_path, filenames=file_names, files_path=files_path, types=str_types,
                  videolen=video_len, words=word_list, frequency=word_frequency)

    def save(self, save_path, filenames, files_path, types, videolen, words, frequency):
        # get time
        save_filename = self.get_time_str()
        save_filename += '.txt'
        writer = open(os.path.join(save_path, save_filename), 'w')
        for index in range(len(filenames)):
            writer.write('文件名称：' + str(index + 1) + '@' + filenames[index] + '\n')
            writer.write('文件路径：' + files_path[index] + '\n')
            writer.write('字幕类型：' + types[index] + '\n')
            # 把时长从字符串转换为正确格式
            videotime = list(videolen[index].strip('\n'))
            videotime.insert(-3, ',')
            videotime.insert(2, ':')
            videotime.insert(5, ':')
            videotime = ''.join(videotime)
            writer.write('视频时长：' + videotime + '\n')
            writer.write('单词总量：' + str(words[index]) + '\n')
            writer.write('英文词频：' + str(frequency[index]) + '\n')
            writer.write('\n')
        writer.close()
        print('Output file is saved！')

    @staticmethod
    def find_srt_file(filename):
        file_filters = [".srt"]
        result = []
        for root, dirs, files in os.walk(filename):
            # root 当前主目录
            # dirs 当前主目录下的所有目录
            # files 当前主目录下的所有文件
            for name in files:
                files_path = os.path.join(root, name)
                ext = os.path.splitext(files_path)[1]  # 获取文件后缀 [0]获取的是除了文件名以外的内容
                if ext in file_filters:
                    result.append(files_path)
        return result

    @staticmethod
    def get_video_time(lines):
        video_time = '0'
        for line in lines:
            if line.find(' --> ') != -1:
                end = line.split(' --> ')[1]
                # change time to 'str' for comparing
                temp = end.split(':', 2)[0] + end.split(':', 2)[1] + \
                       end.split(':', 2)[2].split(',')[0] + end.split(',')[1]
                if temp > video_time:
                    video_time = temp
        return video_time

    @staticmethod
    def count_words(lines):
        """

        :param lines: input line list
        :return: total words
        """
        target_line = 0
        total_words = 0
        arr = []
        for line in lines:
            if line.find(' --> ') != -1:
                # 时间轴的下一行是英文字幕
                target_line += 1
                if target_line < len(lines):
                    sentence = lines[target_line]
                    words_arr = sentence.split()
                    # print(words_arr)
                    total_words += len(words_arr)
                    # print(total_words)
            else:
                target_line += 1
        return total_words

    @staticmethod
    def OnlyChar(lines):
        """

        :param lines:input line list
        :return: processed line list, which has been deleted chinese
        """
        new_lines = []
        reg = "[^0-9A-Za-z.',:!? -><_]"
        for line in lines:
            new = re.sub(reg, '', line)
            if len(line) < 100:
                new_lines.append(new)
        while '' in new_lines:
            new_lines.remove('')
        return new_lines

    @staticmethod
    def get_time_str():
        time = datetime.datetime.now()
        time_str = str(time)
        time_str = time_str.split('.')[0]
        time_str = time_str.replace('-', '')
        time_str = time_str.replace(':', '')
        time_str = time_str.replace(' ', '')
        return time_str
