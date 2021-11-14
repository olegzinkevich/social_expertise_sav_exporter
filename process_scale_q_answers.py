def process_scale_q_answers(x, questions_ids, self, check):

    scale_q_id = x['q_spss_label'] + '_' + x['poll_block_type'] + '_' + 'scale' + '_' + x['question_id']

    questions_ids.append(scale_q_id)

    # check for unique answers
    if x['answer_id'] not in check:

        if x['reply_type'] == 'scale':
            self._answers_data[scale_q_id][x['email']] = x['answer_rel_other']

        elif x['reply_type'] == 'otherNumber':
            self._answers_data[scale_q_id][x['email']] = x['answer_rel_other']

        elif x['reply_type'] == 'otherString':
            self._answers_data[scale_q_id][x['email']] = x['answer_rel_other']

        # затрудняюсь ответить - 98
        elif x['reply_type'] == 'other':
            self._answers_data[scale_q_id][x['email']] = int(98)

        # # отказ от ответа - 99
        elif x['reply_type'] == 'reject':
            self._answers_data[scale_q_id][x['email']] = int(99)

        check.append(x['answer_id'])