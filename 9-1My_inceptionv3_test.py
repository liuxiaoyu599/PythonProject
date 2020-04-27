import tensorflow as tf
import os
import numpy as np
import re
from PIL import Image
import matplotlib.pyplot as plt

lines = tf.gfile.GFile('D:/PythonProject/retrain/output_labels.txt').readlines()
uid_to_name = {}
for uid, line in enumerate(lines):
    line = line.strip('\n')
    uid_to_name[uid] = line
print(uid_to_name)


def id_to_string(node_id):
    if node_id not in uid_to_name:
        return ''
    return uid_to_name[node_id]


# 创建一个图来存放google训练好的模型
with tf.gfile.FastGFile('D:/PythonProject/retrain/output_graph.pb', 'rb') as f:
    graph_def = tf.GraphDef()
    graph_def.ParseFromString(f.read())
    tf.import_graph_def(graph_def, name='')


with tf.Session() as sess:
    # 获得模型最后一层的输出
    softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    for root, dirs, files in os.walk('D:/PythonProject/retrain/data/test/'):
        for file in files:
            # 载入图片 将目录和文件合成一个路径
            image_data = tf.gfile.FastGFile(os.path.join(root, file), 'rb').read()
            # jpg图片解码 得到softmax值
            predictions = sess.run(softmax_tensor, {'DecodeJpeg/contents:0': image_data})
            # 把结果转为1维数据
            predictions = np.squeeze(predictions)

            # 打印图片路径和名称
            image_path = os.path.join(root, file)
            print(image_path)
            # 显示图片
            img = Image.open(image_path)
            plt.figure(5)
            plt.imshow(img)
            plt.axis('off')
            plt.show()

            # 排序 从小到大  从大到小的排序 argsort返回的是索引值
            top_k = predictions.argsort()[::-1]
            for node_id in top_k:
                # 获取分类名称
                human_string = id_to_string(node_id)
                # 获取该分类的置信度
                score = predictions[node_id]
                print('%s (score = %.5f)' % (human_string, score))
            print()
