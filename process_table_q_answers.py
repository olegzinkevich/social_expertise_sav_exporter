import json

def process_table_q_answers(x, questions_ids, self):

    table_q_id = x['q_spss_label'] + '_' + 'row' + str(x['reply_weight']) + '_' + x['poll_block_type'] + '_' + 'table' + '_' + x['question_id']

    # dictOne = {"v1":[1, 2, 3],
    #            "v2":[4, 5, 6],
    #            "v3":[7, 8, 9]}

    # self._answers_data = defaultdict(list)

    questions_ids.append(table_q_id)
    self._questions_ids.add(table_q_id)

    # convert json to python dict with normalized boolean values: false > False
    table_head_list = json.loads(x['q_thead'])

    # [{"th":"кол2","type":"reject","other":null,"weight":1}]
    # [{"th":"col1","type":"otherString","other":"car","weight":0}]
    # "[{"th":"цена от 50","type":"boolean","other":null,"weight":0}]"

    if str(json.loads(x['answer_rel_other'])[0]['type']) == 'otherString':
        self._answers_data[table_q_id][x['email']] = str(json.loads(x['answer_rel_other'])[0]['weight']) + ':' + str(json.loads(x['answer_rel_other'])[0]['other'])

    elif str(json.loads(x['answer_rel_other'])[0]['type']) == 'otherNumber':
        self._answers_data[table_q_id][x['email']] = str(json.loads(x['answer_rel_other'])[0]['weight']) + ':' + str(json.loads(x['answer_rel_other'])[0]['other'])

    elif str(json.loads(x['answer_rel_other'])[0]['type']) == 'other':
        self._answers_data[table_q_id][x['email']] = int(98)

    elif str(json.loads(x['answer_rel_other'])[0]['type']) == 'reject':
        self._answers_data[table_q_id][x['email']] = int(99)

    else:
        self._answers_data[table_q_id][x['email']] = int(json.loads(x['answer_rel_other'])[0]['weight'])


    #  with x:y variant

#      if str(json.loads(x['answer_rel_other'])[0]['type']) == 'otherString':
#         self._answers_data[table_q_id][x['email']] = str(json.loads(x['answer_rel_other'])[0]['weight']) + ':' + str(json.loads(x['answer_rel_other'])[0]['other'])
#
#     elif str(json.loads(x['answer_rel_other'])[0]['type']) == 'otherNumber':
#         self._answers_data[table_q_id][x['email']] = str(json.loads(x['answer_rel_other'])[0]['weight']) + ':' + str(json.loads(x['answer_rel_other'])[0]['other'])
#
#     elif str(json.loads(x['answer_rel_other'])[0]['type']) == 'other':
#         self._answers_data[table_q_id][x['email']] = str(98)
#
#     elif str(json.loads(x['answer_rel_other'])[0]['type']) == 'reject':
#         self._answers_data[table_q_id][x['email']] = str(99)
#
#     else:
#         self._answers_data[table_q_id][x['email']] = str(json.loads(x['answer_rel_other'])[0]['th'])




