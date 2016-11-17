# coding: utf-8
# 重新整理蚂蜂窝数据集，提取问句、候选答案及点赞数
import os
import re
import time


# 读取指定文件夹路径directory下指定数量num个文件,默认是全部读取
def read_file_dir(directory, num=0):
    time_begin = time.time()
    # 输出文件目录
    with open("mafengwo_data.txt", "w") as file_out:
        output_data = ""
        if os.path.isdir(directory):
            # 遍历路径
            for parent, dir_names, file_names in os.walk(directory):
                # 遍历所有文件，用get_file分别对这些文件进行处理
                if num == 0:
                    for file_name in file_names:
                        file_dir = directory + file_name
                        output = get_file(file_dir)
                        output_data += output
                else:
                    for i in range(num):
                        file_dir = directory + file_names[i + 1]
                        print file_dir
                        output = get_file(file_dir)
                        output_data += output
        else:
            print "This directory: \'" + directory + "\' is not a directory."
        file_out.write(output_data)
    time_end = time.time()
    time_consume = time_end - time_begin
    print "Finish"
    print "The get_file procedure cost " + str(time_consume) + " seconds."


# 处理每个文件，提取问题、答案和点赞数等数据
def get_file(file_dir):
    output = ""
    with open(file_dir, 'r') as file:
        answer_count = 0
        for line in file.readlines():
            line = line.strip()
            # 问题
            if line.find("TITLE:") != -1:
                question = line.split(":")[1]
                output += "Question:" + question + "\t"
                # file_out.write("Question:" + question)
                # file_out.write("\t")
            # 回答数量
            elif line.find("RETRESSIZE:") != -1:
                size = line.split(":")[1]
                output += "answer_size:" + size + "\t"
            # 回答
            elif line.find("RETRES") != -1:
                # 用正则表达式分别匹配答案句和点赞数
                pattern1 = 'RETRES_\d+_CONTENT:'
                pattern2 = 'RETRES_\d+_CNTZAN:'
                match_content = re.match(pattern1, line)
                match_like = re.match(pattern2, line)
                # 对答案句去噪，删除用户信息、答案采纳信息等
                if match_content:
                    answer_count += 1
                    # print matchObj.group()
                    answer = re.split("LV.\d+", line)[1]
                    # print answer
                    if answer.find("题主采纳") != -1:
                        answer = answer.split("题主采纳")[1]
                    if answer.find("指路人") != -1:
                        answer = answer.split("指路人")[1]
                    output += str(answer_count) + ':' + answer + "\t"
                # 点赞数，添加在每个答案句之后
                if match_like:
                    like_count = line.split("CNTZAN:")[1]
                    output += like_count + "\t"
        output += "\n"
    return output


# get_data_mafengwo.py on QA data from mafengwo
# def read_file(index_name, file_out, file_count=0):
#     dirs = os.listdir(index_name)
#     output = ""
#     for dir in dirs:
#         if dir == ".DS_Store":
#             continue
#         if file_count < 0:
#             break
#         file_count -= 1
#         print dir
#         file_in = open(index_name + dir, "r")
#         lines = file_in.readlines()
#         answer_count = 0
#         for line in lines:
#             line = line.strip()
#             if line.find("TITLE:") != -1:
#                 question = line.split(":")[1]
#                 output += "Question:" + question + "\t"
#                 # file_out.write("Question:" + question)
#                 # file_out.write("\t")
#             elif line.find("RETRESSIZE:") != -1:
#                 size = line.split(":")[1]
#                 output += "answer_size:" + size + "\t"
#             elif line.find("RETRES") != -1:
#                 pattern1 = 'RETRES_\d+_CONTENT:'
#                 pattern2 = 'RETRES_\d+_CNTZAN:'
#                 match_content = re.match(pattern1, line)
#                 match_like = re.match(pattern2, line)
#                 if match_content:
#                     answer_count += 1
#                     # print matchObj.group()
#                     answer = re.split("LV.\d+", line)[1]
#                     # print answer
#                     if answer.find("题主采纳") != -1:
#                         answer = answer.split("题主采纳")[1]
#                     if answer.find("指路人") != -1:
#                         answer = answer.split("指路人")[1]
#                     output += str(answer_count) + ':' + answer + "\t"
#                 if match_like:
#                     like_count = line.split("CNTZAN:")[1]
#                     output += like_count + "\t"
#         output += "\n"
#         file_in.close()
#     file_out.write(output)


if __name__ == '__main__':
    index_name = "/Users/zhangjiacheng/Downloads/tourQA/detail/"

    # 指定文件数量num
    read_file_dir(index_name, num=3)
    # 默认全部读取
    # read_file_dir(index_name)

    # with open("mafengwo_data.txt","w") as file_out:
    #     read_file(index_name, file_out，file_count=0)
