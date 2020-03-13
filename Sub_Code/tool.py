import datetime
import os
import re

import chardet
import xlwt


class Sub_Counts(object):
    """
    :param input_path: input dirs/files path
    :param save_path: output file save path
    """
    def __init__(self, input_path, save_path):
        self.input_path = input_path
        self.save_path = save_path
        self.log_path = os.path.join(self.save_path, 'log.txt')

    def mainloop(self):
        self.file_names = []
        self.str_types = []
        self.files_path = []
        self.word_freq = []
        # 指定字幕类型（包含英文）
        # type_filter = ["chs", "eng", "Cht", "cht", "Eng", "x264-rovers", "chs&eng", "英文",
        # "简体", "繁体", "简体&英文", "繁体&英文"]
        file_cannot_read = 0
        self.log('程序开始运行.....')
        print('File is loading and processing....')
        for file in self.input_path:
            file_name = file.split('\\', -1)[-1]
            file_name = ''.join(file_name.rsplit('.', 2)[0])
            str_type = file.split('.', -1)[-2]
            # if str_type in type_filter:
            try:
                encoding = self.get_Encoding(file)
                # 读入文件 正则化删除中文
                with open(file, 'r', encoding=encoding) as reader:
                    lines = reader.readlines() # 文本列表
                new_lines = self.OnlyChar(lines)
                frequency = self.frq_counts(new_lines)
                print(f'{file}')
                print('词频：', frequency)
                self.files_path.append(file)
                self.file_names.append(file_name)
                self.str_types.append(str_type)
                self.word_freq.append(frequency)
                self.log(f'Y-File <{file}> is finished!.')
            except BaseException as err:
                file_cannot_read += 1
                err_note = f'发生异常：{file}\t{err}, {encoding}'
                self.log(err_note)
            # else:
            #     self.log(f'N-File <{file}> is not the specified type ! ')
        # self.save_txt(filenames=self.file_names, files_path=self.files_path, types=self.str_types,
        #               frequency=self.word_freq)
        self.save_xls()
        self.log(f'文件保存成功!\t本次运行结果：{len(self.word_freq)} subtitle files were processed\t'
                f'{file_cannot_read} subtitle files cannot read\t\n')

    def save_txt(self,  filenames, files_path, types, frequency):
        save_filename = self.get_time_str()
        save_filename += '.txt'
        save_filename = os.path.join(self.save_path, save_filename)
        with open(save_filename, 'w') as writer:
            for index in range(len(filenames)):
                writer.write('文件名称：' + str(index + 1) + '@' + filenames[index] + '\n')
                writer.write('文件路径：' + files_path[index] + '\n')
                writer.write('字幕类型：' + types[index] + '\n')
                writer.write('英文词频：' + str(frequency[index]) + '\n')
                writer.write('\n')
        print('Output file is saved！')

    def save_xls(self):
        save_filename = self.get_time_str()
        save_filename += '.xls'
        workbook = xlwt.Workbook()
        sheet = workbook.add_sheet("Sheet1")
        sheet.col(0).width = 12000
        sheet.col(1).width = 20000
        sheet.col(2).width = 3000
        sheet.col(3).width = 3000
        title_style = xlwt.XFStyle()
        title_style.font.bold = True
        title_style.font.height = 20*12
        title_style.alignment.horz = 2
        sheet.write(0, 0, "文件名", title_style)
        sheet.write(0, 1, "文件路径", title_style)
        sheet.write(0, 2, "字幕类型", title_style)
        sheet.write(0, 3, "词频", title_style)
        for index in range(len(self.file_names)):
            sheet.write(index+1, 0, self.file_names[index-1])
            sheet.write(index+1, 1, self.files_path[index-1])
            sheet.write(index+1, 2, self.str_types[index-1])
            sheet.write(index+1, 3, float(self.word_freq[index-1]))
        workbook.save(os.path.join(self.save_path, save_filename))
        print('Output file is saved！')

    def log(self, notes):
        with open(self.log_path, 'a') as writer:
            writer.write('['+str(datetime.datetime.now())+']'+notes+'\n')

    @staticmethod
    def get_Encoding(file):
        f = open(file, 'rb')
        data = f.read()
        f.close()
        encoding = chardet.detect(data).get('encoding')
        return encoding

    @staticmethod
    def find_srt_file(filename):
        file_filters = [".srt"]
        result = []
        if filename.endswith('.srt'):
            result.append(filename)
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
    def frq_counts(lines):
        target_line = 0
        total_words = 0
        speak_time = 0
        sub_frq = 0.0

        for line in lines:
            if line.find(' --> ') != -1:
                line = line.replace(':', ' ').replace(',', ' ').replace('-->', '')
                t = line.split()
                start_time = int(t[0])*3600 + int(t[1])*60 + int(t[2]) + int(t[3])/1000
                end_time = int(t[4])*3600 + int(t[5])*60 + int(t[6]) + int(t[7])/1000
                sten_speak_time = (end_time - start_time)/60
                target_line += 1
                if target_line < len(lines):
                    if 'a' <= lines[target_line].lower()[0] <= 'z':
                        words_arr = lines[target_line].replace(',', ' ').replace(':', ' ').split()
                        if words_arr:
                            total_words += len(words_arr)
                            speak_time += sten_speak_time
            else:
                target_line += 1
        if speak_time != 0:
            sub_frq = total_words/speak_time

        return round(sub_frq,2)

    @staticmethod
    def OnlyChar(lines):
        """
        :param lines:input line list
        :return: processed line list, which has been deleted chinese
        """
        new_lines = []
        reg = "[^0-9A-Za-z.'{},:!? -><_]"
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
