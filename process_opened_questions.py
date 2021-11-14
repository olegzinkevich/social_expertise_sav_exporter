def process_opened_questions(x, self, check_question_ids, tmp):

    opened_q_id = x['q_spss_label'] + '_' + x['poll_block_type'] + '_' + 'opened' + '_' + x['question_id']

    ##############################
    ##### variable_measure
    ##############################

    ###### Data Structure: #######
    # keys being variable names and values being strings one of “nominal”, “ordinal”, “scale”. Format: {'s1':'scale', 's2':'scale', 's3': 'nominal'}
    ##############################

    self._variable_measure[opened_q_id] = 'scale'

    ##############################
    ##### formats
    ##############################

    ###### Data Structure: #######
    # a dictionary with the column name as key and a string with the format as values: {'s1':'N4', 'v1':'F1.0'}
    ##############################

    self._formats[opened_q_id] = str()

    ##############################
    ##### column_labels
    ##############################

    ###### Data Structure: #######
    # ["s1 Скажите, пользовались ли...", "s2 Вызывает ли?", "texdr другое"]
    ##############################

    if opened_q_id not in check_question_ids:

        self._column_labels[opened_q_id] = x['question']
        check_question_ids.add(opened_q_id)

    ##############################
    ##### variable_value_labels
    ##############################

    ###### Data Structure: #######
    # {'s1': {1: 'Да, приобретал(а)', 2: 'Нет, не приобретал(а)'}, 's2': {1: 'Да, видела', 2: 'Нет, не видела', 3: 'другое'}, 's3': {}}
    ##############################

    # [{'question_id':'141njn23423', 'question_weight': 3, {1: 'Да, приобретал(а)', 2: 'Нет, не приобретал(а)'}}

    tmp[opened_q_id].append({})

    # todo - проверить opened 98,99 mapping - должно быть, как в closed q.
    # отказ от ответа - 99
    # if x['reply_type'] == 'reject':
    #     tmp[opened_q_id].append({x['reply_weight']-1: str(99)})
    #
    # # затрудняюсь ответить - 98
    # elif x['reply_type'] == 'other':
    #     tmp[opened_q_id].append({x['reply_weight']-1: str(98)})
    #
    # # остальные типы - text, date, location
    # else:
    #     tmp[opened_q_id].append({x['reply_weight']-1: x['reply']})
    #     # tmp[x['question_id']].append({int(x['reply_weight']): x['reply']})
    #
    # self._questions_ids.add(opened_q_id)