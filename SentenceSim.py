# coding: utf-8
import jieba
import gensim
import numpy
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def open_file():
    with open('mafengwo_data.txt', 'r') as data:
        file_lines = data.readlines()
    return file_lines


def get_question_answer(line):
    question = line.strip().split('\t')[0].split(":")[1]
    answer_count = line.strip().split('\t')[1].split(":")[1]
    answer_list = [(line.strip().split('\t')[2 * i + 2].split(":")[1], line.strip().split('\t')[2 * i + 3].split(":")[0]) for i in range(int(answer_count))]
    return question, answer_count, answer_list


def sentence_parse(sentence):
    # print sentence
    seg_list = jieba.cut(sentence, cut_all=False)
    # return " ".join(seg_list).split(" ")
    return list(seg_list)
    # print "Full Mode:" + " ".join(seg_list)


def word_sim(worda, wordb):
    sim_val = 0
    # if worda not in model:
    #     print worda + ' is not in model'
    # if wordb not in model:
    #     print wordb + ' is not in model'
    if worda in model and wordb in model:
        sim_val = model.similarity(worda, wordb)
    # print "similarity between " + worda + " and " + wordb + " is: " + str(sim_val)
    return sim_val
    # gensim.load()


def delete_stop_words(sentence):
    sentence = sentence.replace("?", "")
    sentence = sentence.replace("!", "")
    sentence = sentence.replace(":", "")
    sentence = sentence.replace("\"", "")
    sentence = sentence.replace("\'", "")
    sentence = sentence.replace("(", "")
    sentence = sentence.replace(")", "")
    sentence = sentence.replace("~", "")
    sentence = sentence.replace(";", "")
    sentence = sentence.replace(",", "")
    sentence = sentence.replace("？", "")
    sentence = sentence.replace("！", "")
    sentence = sentence.replace("：", "")
    sentence = sentence.replace("\"", "")
    sentence = sentence.replace("\"", "")
    sentence = sentence.replace("）", "")
    sentence = sentence.replace("（", "")
    sentence = sentence.replace("～", "")
    sentence = sentence.replace("；", "")
    sentence = sentence.replace("，", "")
    return sentence


def sentence_sim(question, answer):
    question = delete_stop_words(question)
    answer = delete_stop_words(answer)
    question_seg = sentence_parse(question)
    answer_seg = sentence_parse(answer)
    sim = 0
    q_size = len(question_seg)
    a_size = len(answer_seg)
    for answer_word in answer_seg:
        for question_word in question_seg:
            sim += word_sim(unicode(answer_word), unicode(question_word))
    return sim / (q_size * a_size)


def process(lines, output):
    print "process begins"
    for line in lines:
        question, candidate_answers = line_process(line)
        output.write("question:" + question + "\n")
        for answer in candidate_answers:
            # print answer
            output.write("score:" + str(answer[0]) + "\n")
            output.write("answer:" + answer[1][0] + "\n")
    print "process finished"


def line_process(line):
    candidate_answers = []
    question, answer_count, answer_list = get_question_answer(line)
    # print question
    for answer in answer_list:
        print answer[0], len(answer[0])
        if len(answer[0]) < 20:
            continue
        sim_value = sentence_sim(question, answer[0])
        # if sim_value >= 0.4:
        candidate_answers.append((sim_value, answer))
        candidate_answers = sorted(candidate_answers, key=lambda sim_value: sim_value[0], reverse=1)
    return question, candidate_answers

if __name__ == '__main__':
    # sentence = "工信处女干事每月经过下属科室都要亲口交代24口交换机等技术性器件的安装工作"
    model = gensim.models.Word2Vec.load_word2vec_format("vecmodel.bin", binary=False)
    # with open('nanren.txt', 'r') as nanren:
    #     line1 = unicode(nanren.readline().strip())
    #     line2 = unicode(nanren.readline().strip())
    #     word_sim_val = word_sim(model, line1, line2)
    # word_sim_val = word_sim(model, unicode('男人'), unicode('女人'))
    # word_sim_val = word_sim(model, unicode('狗'), unicode('女人'))
    # word_sim_val = word_sim(model, unicode('小三'), unicode('女人'))
    # word_sim_val = word_sim(model, unicode('小三'), unicode('男人'))
    output = open('out_file.txt', 'w')
    lines = open_file()
    process(lines, output)
    output.close()

