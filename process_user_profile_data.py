def process_user_profile_data(self, tmp):

    ##############################
    ##### variable_measure
    ##############################

    ###### Data Structure: #######
    # keys being variable names and values being strings one of “nominal”, “ordinal”, “scale”. Format: {'s1':'scale', 's2':'scale', 's3': 'nominal'}
    ##############################

    self._variable_measure['phone'] = 'nominal'
    self._variable_measure['sex'] = 'nominal'
    self._variable_measure['email'] = 'nominal'
    self._variable_measure['total_answer_time'] = 'scale'

    ##############################
    ##### formats
    ##############################

    ###### Data Structure: #######
    # a dictionary with the column name as key and a string with the format as values: {'s1':'N4', 'v1':'F1.0'}
    ##############################

    self._formats['phone'] = str()
    self._formats['sex'] = str()
    self._formats['email'] = str()
    self._formats['total_answer_time'] = 'F1.0'

    ##############################
    ##### column_labels
    ##############################

    ###### Data Structure: #######
    # ["s1 Скажите, пользовались ли...", "s2 Вызывает ли?", "texdr другое"]
    ##############################

    self._column_labels['phone'] = 'Телефон'
    self._column_labels['sex'] = 'Пол'
    self._column_labels['email'] = 'email'
    self._column_labels['total_answer_time'] = 'Время ответа'

    ##############################
    ##### variable_value_labels
    ##############################

    ###### Data Structure: #######
    # {'s1': {1: 'Да, приобретал(а)', 2: 'Нет, не приобретал(а)'}, 's2': {1: 'Да, видела', 2: 'Нет, не видела', 3: 'другое'}, 's3': {}}
    ##############################

    # [{'question_id':'141njn23423', 'question_weight': 3, {1: 'Да, приобретал(а)', 2: 'Нет, не приобретал(а)'}}
    
    # tmp['phone'].append({0: 'None'})
    tmp['phone'].append({})
    tmp['sex'].append({})
    tmp['email'].append({})
    tmp['total_answer_time'].append({})

    self._questions_ids.add('phone')
    self._questions_ids.add('sex')
    self._questions_ids.add('email')
    self._questions_ids.add('total_answer_time')