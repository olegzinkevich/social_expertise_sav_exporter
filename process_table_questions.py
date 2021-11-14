import json

def process_table_questions(x, self, check_question_ids, tmp):

    ##############################
    ##### process table questions
    ##############################

    table_q_id = x['q_spss_label'] + '_' + 'row' + str(x['reply_weight']) + '_' + x['poll_block_type'] + '_' + 'table' + '_' + x['question_id']

    self._questions_ids.add(table_q_id)

    ##############################
    ##### variable_measure
    ##############################

    ###### Data Structure: #######
    # keys being variable names and values being strings one of “nominal”, “ordinal”, “scale”. Format: {'s1':'scale', 's2':'scale', 's3': 'nominal'}
    ##############################

    self._variable_measure[table_q_id] = 'scale'

    ##############################
    ##### formats
    ##############################

    ###### Data Structure: #######
    # a dictionary with the column name as key and a string with the format as values: {'s1':'N4', 'v1':'F1.0'}
    ##############################

    self._formats[table_q_id] = 'F1.0'

    ##############################
    ##### column_labels
    ##############################

    if table_q_id not in check_question_ids:

        self._column_labels[table_q_id] = x['question']
        check_question_ids.add(table_q_id)

    # convert json to python dict with normalized boolean values: false > False
    table_head_list = json.loads(x['q.thead'])
    th_len = len(table_head_list)

    # skipping table_head_list[0]: {"th":"","type":false,"weight":0}
    for i in range(1, th_len):

        ##############################
        ##### variable_value_labels
        ##############################

        ###### Data Structure: #######
        # {'s1': {1: 'Да, приобретал(а)', 2: 'Нет, не приобретал(а)'}, 's2': {1: 'Да, видела', 2: 'Нет, не видела', 3: 'другое'}, 's3': {}}
        ##############################

        # [{'th': '', 'type': False, 'weight': 0}, {'th': 'col 1', 'type': 'boolean', 'weight': 1, 'body': False}, {'th': 'col 2', 'type': 'boolean', 'weight': 2, 'body': False}]
        # tmp[table_q_id].append({int(table_head_list[i]['weight'])-1: table_head_list[i]['th']})

        tmp[table_q_id].append({int(table_head_list[i]['weight'])-1: table_head_list[i]['th']})

        # # todo = mapping 99, 98 как в closed q - нет такого поля в базе в reply_type - reject, стоит multiple
        # if x['reply_type'] == 'reject':
        #     tmp[table_q_id].append({int(99): table_head_list[i]['th']})
        #
        # elif x['reply_type'] == 'other':
        #     tmp[table_q_id].append({int(98): table_head_list[i]['th']})
        #
        # else:
        #     tmp[table_q_id].append({int(table_head_list[i]['weight']): table_head_list[i]['th']})
        #
        # # if {x['reply_weight']: x['reply']} not in tmp[x['question_id']]:
        # #     tmp[x['question_id']].append({x['reply_weight']: x['reply']})