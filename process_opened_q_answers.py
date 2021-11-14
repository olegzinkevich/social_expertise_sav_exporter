def process_opened_q_answers(x, questions_ids, self, check):

    opened_q_id = x['q_spss_label'] + '_' + x['poll_block_type'] + '_' + 'opened' + '_' + x['question_id']

    questions_ids.append(opened_q_id)

    # check for unique answers
    if x['answer_id'] not in check:

        # отказ от ответа - 99
        if x['reply_type'] == 'reject':
            self._answers_data[opened_q_id][x['email']] = int(99)

        # затрудняюсь ответить - 98
        elif x['reply_type'] == 'other':
            self._answers_data[opened_q_id][x['email']] = str(98)

        elif x['reply_type'] == 'otherString':
            try:
                self._answers_data[opened_q_id][x['email']] = x['answer_rel_other']
            except:
                self._answers_data[opened_q_id][x['email']] = 99

        # остальные типы - text, date, location
        else:
            self._answers_data[opened_q_id][x['email']] = x['answer_rel_other']

    check.append(x['answer_id'])