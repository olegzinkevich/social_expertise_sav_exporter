def process_scale_questions(x, self, check_question_ids, tmp):

    ##############################
    ##### process general questions multiple
    ##############################

    scale_q_id = x['q_spss_label'] + '_' + x['poll_block_type'] + '_' + 'scale' + '_' + x['question_id']

    ##############################
    ##### variable_measure
    ##############################

    ###### Data Structure: #######
    # keys being variable names and values being strings one of “nominal”, “ordinal”, “scale”. Format: {'s1':'scale', 's2':'scale', 's3': 'nominal'}
    ##############################

    self._variable_measure[scale_q_id] = 'scale'

    ##############################
    ##### formats
    ##############################

    ###### Data Structure: #######
    # a dictionary with the column name as key and a string with the format as values: {'s1':'N4', 'v1':'F1.0'}
    ##############################

    self._formats[scale_q_id] = 'F1.0'

    ##############################
    ##### column_labels
    ##############################
    # ["s1 Скажите, пользовались ли...", "s2 Вызывает ли?", "texdr другое"]
    # _column_labels = {'id_53726480_b157_41fc_9c0d_72f227a277d7': 'Лейбл 1', 'id_2179dc63_679b_4c68_84c8_49c3ca7d1d57': 'Лейбл 2',}
    ##############################

    if scale_q_id not in check_question_ids:

        self._column_labels[scale_q_id] = x['question']
        check_question_ids.add(scale_q_id)

    ##############################
    ##### variable_value_labels
    ##############################

    ###### Data Structure: #######
    # {'s1': {1: 'Да, приобретал(а)', 2: 'Нет, не приобретал(а)'}, 's2': {1: 'Да, видела', 2: 'Нет, не видела', 3: 'другое'}, 's3': {}}
    ##############################

    # [{'question_id':'141njn23423', 'question_weight': 3, {1: 'Да, приобретал(а)', 2: 'Нет, не приобретал(а)'}}

    tmp[scale_q_id].append({})

    self._questions_ids.add(scale_q_id)

