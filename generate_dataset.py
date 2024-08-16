# -*- coding: utf-8 -*-
import pandas
import os
import re

TYPE_LABEL = ['经济','科技', '军事', '政治', '外交', '社会', '网信', '教育', '文体', '卫生', '民生', '其他']
TYPE_LABEL_MAP = {
    '经济': 'economy',
    '科技': 'technology',
    '军事': 'military',
    '政治': 'politics',
    '外交': 'foreign policy',
    '社会': 'society',
    '网信': ''
    '其他': 'other'
}


class DatasetGenerator:
    
    def __init__(self, dataset_path, output_path):
        self.dataset_path = dataset_path
        self.output_path = output_path
        self.dataset_path = dataset_path
        self.dataset = self.init_dataset()
    
    def init_dataset(self):
        # 读取数据集
        chinese = []
        english = []
        type_label = []
        rate_label = []
        # 读取数据集
        excel_data = pandas.read_excel(self.dataset_path, sheet_name=None)
        for sheet_name, sheet_data in excel_data.items():
            chinese.extend(sheet_data['中文'].tolist())
            english.extend(sheet_data['英文'].tolist())
            type_label.extend(sheet_data['类型'].tolist())
            rate_label.extend(sheet_data['级别'].tolist())
        for i in range(len(chinese)):
            temp = chinese[i]
            if '\n\n\n' in temp:
                chinese[i] = temp.replace('\n\n\n', '#@#@#')
                chinese[i] = temp.replace('\n', '')
            elif '\n\n' in temp:
                chinese[i] = temp.replace('\n\n', '#@#@#')
                chinese[i] = temp.replace('\n', '')
            elif '\n' in temp:
                chinese[i] = temp.replace('\n', '#@#@#')
            else:
                chinese[i] = temp
        for i in range(len(english)):
            temp = english[i]
            if '\n\n\n' in temp:
                english[i] = temp.replace('\n\n\n', '#@#@#')
                english[i] = temp.replace('\n', '')
            elif '\n\n' in temp:
                english[i] = temp.replace('\n\n', '#@#@#')
                english[i] = temp.replace('\n', '')
            elif '\n' in temp:
                english[i] = temp.replace('\n', '#@#@#')
            else:
                english[i] = temp
        dataset = pandas.DataFrame({'chinese': chinese, 'english': english, 'type_label': type_label, 'rate_label': rate_label})
        return dataset

    def generate_dataset(self, sentence_length = 0):
        if sentence_length == 0:
            self.generate_dataset_with_paragraph()
        elif sentence_length > 0:
            self.generate_dataset_with_sentence(sentence_length)
        else:
            raise ValueError("sentence_length must be greater than 0")

    def generate_dataset_with_paragraph(self):
        chinese_list = []
        label_list = []
        for chinese, type_label, rate_label in zip(self.dataset['chinese'], self.dataset['type_label'], self.dataset['rate_label']):
            paragraphs = re.split('#@#@#', chinese)
            for paragraph in paragraphs:
                chinese_list.append(paragraph)
                label_list.append(type_label)
        dataset = pandas.DataFrame({'chinese': chinese_list, 'type_label': label_list})
        dataset.to_csv(os.path.join(self.output_path, 'dataset_0_chinese.csv'), index=False)

        english_list = []
        label_list = []
        for english, type_label in zip(self.dataset['english'], self.dataset['type_label']):
            paragraphs = re.split('#@#@#', english)
            for paragraph in paragraphs:
                english_list.append(paragraph)
                label_list.append(LABEL_MAP[type_label])
        dataset = pandas.DataFrame({'english': english_list, 'type_label': label_list})
        dataset.to_csv(os.path.join(self.output_path, 'dataset_0_english.csv'), index=False)
            
    
    def generate_dataset_with_sentence(self, sentence_length):
        chinese_list = []
        label_list = []
        for chinese, type_label in zip(self.dataset['chinese'], self.dataset['type_label']):
            chinese = chinese.replace('#@#@#', '。')
            sentences = re.split(r'。', chinese)
            item =''
            index = 0
            for sentence in sentences:
                if sentence == '':
                    continue
                if index < sentence_length:
                    item += sentence + '。 '
                    index += 1
                else:
                    chinese_list.append(item)
                    label_list.append(type_label)
                    item = sentence
                    index = 1
            if item != '':
              chinese_list.append(item)
              label_list.append(type_label)
        dataset = pandas.DataFrame({'chinese': chinese_list, 'type_label': label_list})
        dataset.to_csv(os.path.join(self.output_path, 'dataset_{}_chinese.csv'.format(sentence_length)), index=False)

        english_list = []
        label_list = []
        for english, type_label in zip(self.dataset['english'], self.dataset['type_label']):
            english = english.replace('#@#@#', '. ')
            # pattern = r'(?<!\d)[(.]|[.](?!\d)'
            pattern = r'\.\s'

            sentences = re.split(pattern, english)
            item =''
            index = 0
            for sentence in sentences:
                if sentence == '':
                    continue
                if index < sentence_length:
                    item += sentence + '. '
                    index += 1
                else:
                    english_list.append(item)
                    label_list.append(LABEL_MAP[type_label])
                    item = sentence
                    index = 1
            if item != '':
              english_list.append(item)
              label_list.append(LABEL_MAP[type_label])
        dataset = pandas.DataFrame({'english': english_list, 'type_label': label_list})
        dataset.to_csv(os.path.join(self.output_path, 'dataset_{}_english.csv'.format(sentence_length)), index=False)


if __name__ == '__main__':
    dataset_path = '20240715.xlsx'
    output_path = ''
    dataset_generator = DatasetGenerator(dataset_path, output_path)
    dataset_generator.generate_dataset(sentence_length=1)