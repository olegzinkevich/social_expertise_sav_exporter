from datetime import datetime
import re

def process_user_profile_data_answers(x, questions_ids, self):

    if x['email'] not in questions_ids:
        questions_ids.append(x['email'])
        
    elif x['sex'] not in questions_ids:
        questions_ids.append(x['sex'])
        
    elif x['phone'] not in questions_ids:
        questions_ids.append(x['phone'])

    elif 'total_answer_time' not in questions_ids:
        questions_ids.append('total_answer_time')

    #######################
    # calculate total time
    #######################

    # split by regex on multiple strings  T and [T|\. ]:
    # start_splitted = re.split('[T|\. ]', start)
    start_splitted = re.split('\.', str(x['answer_start']))
    start_converted = datetime.strptime(start_splitted[0], "%Y-%m-%dT%H:%M:%S")
    finish_splitted =  re.split('\.', str(x['answer_finish']))
    finish_converted = datetime.strptime(finish_splitted[0], "%Y-%m-%dT%H:%M:%S")

    total_answer_time = (finish_converted - start_converted).total_seconds()

    ######################
    # writing answers
    ######################

    # search by unique email
    if x['email'] not in self._answers_data['email']:
        self._answers_data['email'][x['email']]= str(x['email'])
        self._answers_data['sex'][x['email']] = str(x['sex'])
        self._answers_data['phone'][x['email']] = str(x['phone'])
        self._answers_data['total_answer_time'][x['email']] = str(total_answer_time)
