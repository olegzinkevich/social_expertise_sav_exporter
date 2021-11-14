#!/usr/bin/python
# -*- coding: utf-8 -*-

from neo4j import GraphDatabase, basic_auth
from collections import defaultdict, OrderedDict
import pandas as pd
import pyreadstat
from dotenv import load_dotenv, get_key
import os
import os.path
import re
import numpy as np
import json
import sys
import os.path as path
# import logging
import traceback

# import sav_exporter inner modules
from process_table_questions import process_table_questions
from process_general_multiple_questions import process_general_multiple_questions
from process_general_questions import process_general_questions
from process_table_q_answers import process_table_q_answers
from process_general_multiple_q_answers import process_general_multiple_q_answers
from process_general_q_answers import process_general_q_answers
from process_user_profile_data import process_user_profile_data
from process_user_profile_data_answers import process_user_profile_data_answers
from process_scale_questions import process_scale_questions
from process_scale_q_answers import process_scale_q_answers
from process_opened_questions import process_opened_questions
from process_opened_q_answers import process_opened_q_answers

#####################
# .env path
#####################

ROOT_PATH = path.abspath(path.join(__file__, "../.."))
DOT_ENV_PATH = os.path.join(ROOT_PATH, '.env')

#####################
# load .env file
#####################

load_dotenv(dotenv_path=DOT_ENV_PATH)
HOST =  os.getenv('NEO4J_PROTOCOL') + '+s://' + os.getenv('NEO4J_HOST')
DB_NAME = os.getenv('NEO4J_DATABASE')
PASSWORD = os.getenv('NEO4J_PASSWORD')
FILE_PATH = os.getenv('FILE_PATH')
LOGS_PATH = os.getenv('LOGS_PATH')

#####################
# configure log files
#####################

LOGS_FILENAME = os.path.join(LOGS_PATH, 'sav_exporter.log')

if not os.path.exists(LOGS_FILENAME):
  open(LOGS_FILENAME, 'w').close()

#####################
# main class
#####################

class SavExporter(object):

  def __init__(self, poll_id):
    '''
    Parameters
    ----------
    poll_id - string 'f53cd49a-148e-4746-b714-d8df1198dc8c'
    '''

    ### Neo4j driver ###
    # self.driver = GraphDatabase.driver(HOST, auth=(DB_NAME, PASSWORD), encrypted=True)
    self.driver = GraphDatabase.driver(HOST, auth=(DB_NAME, PASSWORD))

    self.poll_id = poll_id
    self._sav_file_name = None
    self._sav_file_label = None
    self._questions_ids = set()
    self._variable_value_labels = {}
    self._column_labels = {}
    self._variable_measure = {}
    self._formats = {}
    self._answers_data = defaultdict(dict)
    self._pd_answers_data = None

    ### Logging ###

    # logging.basicConfig(
    #     handlers = [logging.FileHandler(LOGS_FILENAME, 'a', 'utf-8')],
    #     level = logging.INFO,
    #     format = '%(name)s | %(asctime)s | %(levelname)s: %(message)s')
    #
    # self._logger = logging.getLogger(poll_id)

  def file_name_generator(self):
    '''Generates file name from id in format: f53cd49a_148e_4746_b714_d8df1198dc8c
    '''

    self._sav_file_name = self.poll_id.replace('-', '_')

  def remove_tags_spaces(text):
    '''Removes html tags, '\n', double spaces and 'nbsp;' from questions'''

    TAG_RE = re.compile(r'<[^>]+>')
    text = TAG_RE.sub('', text)
    text = re.sub(' +', ' ', text)
    text = text.replace("&nbsp;", " ")
    text = text.replace("\n", " ")
    return text

  def fetch_questions(self):
    '''Get questions and replies structure from the database'''

    with self.driver.session() as session:
      results = session.run(
        f"""
    OPTIONAL MATCH (reply:ReplyOption)-[HAS_A_REPLY_OPTION]-(q:Question)<-[HAS_A_QUESTION]-(pollBlock:PollBlock)<-[HAS_A_POLL_BLOCK]-(poll:Poll)
    WHERE poll.id="{self.poll_id}"
    RETURN poll.id, poll.description, pollBlock.type, pollBlock.body, pollBlock.weight, q.body, q.id, q.type, q.multiple,  q.weight, q.thead, q.spss_label, reply.body, reply.type, reply.weight, reply.id
    ORDER BY pollBlock.weight, q.weight, reply.weight
                """)

      loc_list = []
      for index, record in enumerate(results):

        ##############################
        ##### combine and normalize question text in paragraphs
        ##############################

        question_text_paragraphs = []
        for x in eval(record['q.body']):
          try:
            question_text_paragraphs.append(x['data']['text'])
          except:
            pass
        question_text = ' '.join(question_text_paragraphs)
        question_text = SavExporter.remove_tags_spaces(question_text)

        ##############################
        ##### prepare convenient data format
        ##############################

        local_dict = dict()
        local_dict['question_id'] = 'id_' + record["q.id"][:8].replace('-', '_')
        local_dict['question'] = question_text
        local_dict['question_weight'] = record['q.weight']
        local_dict['question_type'] = record['q.type']
        local_dict['q.thead'] = record['q.thead']
        if record['q.spss_label'] != None:
          local_dict['q_spss_label'] = 'q_' + re.sub(' +', '', record['q.spss_label']).replace('-', '_')
        else:
          local_dict['q_spss_label'] = 'z'
        local_dict['reply'] = record['reply.body']
        local_dict['reply_type'] = record['reply.type']
        local_dict['reply_weight'] = int(record['reply.weight'])+1
        local_dict['q_multiple'] = record['q.multiple']
        if record['pollBlock.type'] == 'demographic':
          local_dict['poll_block_type'] = 'demog'
        else:
          local_dict['poll_block_type'] = record['pollBlock.type']
        local_dict['poll_block_weight'] = record['pollBlock.weight']
        loc_list.append(local_dict)

        self._sav_file_label = record['poll.description']

      # if len(loc_list) < 1:
      # self.logger.warning("No data exists in the database")

      ##############
      # saving in loc_list only unique items
      ##############
      loc_list_unique = []
      for i in loc_list:
        if i not in loc_list_unique:
          loc_list_unique.append((i))

      tmp = defaultdict(list)
      check_question_ids = set()

      for index, x in enumerate(loc_list_unique):
        if x['poll_block_type'] == 'welcom' or x['poll_block_type'] == 'verify':
          pass

        else:
          if x['question_type'] == 'table':
            process_table_questions(x, self, check_question_ids, tmp)

          elif x['question_type'] == 'scale':
            process_scale_questions(x, self, check_question_ids, tmp)

          elif x['question_type'] == 'opened':
            process_opened_questions(x, self, check_question_ids, tmp)

          elif x['q_multiple'] == True:
            process_general_multiple_questions(x, self, check_question_ids, tmp)

          ##############################
          ##### process general questions - multiple and not
          ##############################
          else:
            process_general_questions(x, self, check_question_ids, tmp)

      ##############################
      # create question items for user profile data
      ##############################

      process_user_profile_data(self, tmp)

      ##############################
      # convert variable_value_labels inner list of dicts to dict:
      ##############################

      for key, val in tmp.items():

        self._variable_value_labels[key] = {k:v for element in val for k,v in element.items()}

    # important - not to get an error in shell (Underlying socket connection gone)
    self.driver.close()

  def fetch_answers(self):
    '''Get answers data from the database'''

    with self.driver.session() as session:
      results = session.run(
        f"""
            MATCH (profile:Profile)<-[HAS_A_PROFILE]-(user:User)-[HAS_A_SUBMISSION]->(submission:Submission)-[HAS_A_ANSWER]->(answer:Answer)-[answer_rel:IS_ANSWER_FROM_OPTION]->(reply:ReplyOption)-[HAS_A_REPLY_OPTION]-(q:Question)<-[HAS_A_QUESTION]-(pollBlock:PollBlock)<-[HAS_A_POLL_BLOCK]-(poll:Poll), (user)-[HAS_A_OAUTH_PROVIDER]->(oauth:OauthProvider)
WHERE poll.id="{self.poll_id}"
RETURN poll.id, profile.sex, profile.phone, oauth.login, pollBlock.type, pollBlock.body, pollBlock.weight, q.body, q.id, q.weight, q.spss_label, q.type, q.multiple, q.thead, reply.body, reply.weight, reply.id, answer.id, answer_rel.other, reply.type, submission.createdAt, submission.updatedAt, submission.status
ORDER BY pollBlock.weight, q.weight, reply.weight
                """)

      ##############################
      ##### prepare convenient data format
      ##############################
      loc_list_answers = []
      for record in results:

        local_dict_answer = dict()
        local_dict_answer['question_id'] = 'id_' + record["q.id"][:8].replace('-', '_')
        local_dict_answer['question_weight'] = record['q.weight']
        local_dict_answer['question_type'] = record['q.type']
        local_dict_answer['q_thead'] = record['q.thead']
        if record['q.spss_label'] != None:
          local_dict_answer['q_spss_label'] = 'q_' + re.sub(' +', '', record['q.spss_label']).replace('-', '_')
        else:
          local_dict_answer['q_spss_label'] = 'z'
        if record['pollBlock.type'] == 'demographic':
          local_dict_answer['poll_block_type'] = 'demog'
        else:
          local_dict_answer['poll_block_type'] = record['pollBlock.type']
        local_dict_answer['poll_block_weight'] = record['pollBlock.weight']
        local_dict_answer['reply'] = record['reply.body']
        local_dict_answer['reply_weight'] = int(record['reply.weight'])+1
        local_dict_answer['reply_type'] = record['reply.type']
        local_dict_answer['answer_rel_other'] = record["answer_rel.other"]
        local_dict_answer['answer_id'] = record["answer.id"]
        local_dict_answer['q_multiple'] = record['q.multiple']
        local_dict_answer['email'] = record['oauth.login']
        local_dict_answer['sex'] = record['profile.sex']
        local_dict_answer['phone'] = record['profile.phone']
        local_dict_answer['answer_start'] = record['submission.createdAt']
        local_dict_answer['answer_finish'] = record['submission.updatedAt']
        local_dict_answer['submission_status'] = record['submission.status']
        loc_list_answers.append(local_dict_answer)

      ##############################
      ##### format
      ##############################

      questions_ids = []
      check = []

      for x in loc_list_answers:

        if x['submission_status'] == 'finished':

          if x['poll_block_type'] == 'welcom' or x['poll_block_type'] == 'verify':
            pass

          else:

            if x['question_type'] == 'table':
              process_table_q_answers(x, questions_ids, self)

            elif x['question_type'] == 'opened':
              process_opened_q_answers(x, questions_ids, self, check)

            elif x['question_type'] == 'scale':
              process_scale_q_answers(x, questions_ids, self, check)

            ##############################
            ##### process general questions - multiple and not
            ##############################

            else:

              if x['q_multiple'] == True:
                process_general_multiple_q_answers(x, questions_ids, self, check)

              else:
                process_general_q_answers(x, questions_ids, self, check)

          ##############################
          ##### process user profile data
          ##############################

          process_user_profile_data_answers(x, questions_ids, self)

    # important - not to get an error in shell (Underlying socket connection gone)
    self.driver.close()

  def check_missing_data(self):
    '''Checks for missing answers. If found missing data it's filled with 99'''

    pd_answers_data = pd.DataFrame.from_dict(self._answers_data, orient='index')
    pd_answers_data = pd_answers_data.transpose()

    missing_questions = []

    for q in self._questions_ids:

      if q not in pd_answers_data.columns:
        missing_questions.append(q)

    for q in missing_questions:
      pd_answers_data[q] = '.'

    self._pd_answers_data = pd_answers_data

  def check_data_lengths(self):
    pass

  def save_file(self):

    save_dir = os.path.join(FILE_PATH, f'{self._sav_file_name}')
    if not os.path.exists(save_dir):
      os.mkdir(save_dir)

    file_to_save = os.path.join(save_dir, f'{self._sav_file_name}')

    self._pd_answers_data.to_csv(f'{file_to_save}_answers.csv', sep=',')

    var_lables_df = pd.DataFrame(self._variable_value_labels)
    var_lables_df.to_csv(f'{file_to_save}_value_lables.csv', sep=',')

    ##########################
    # save file
    ##########################
    try:
      pyreadstat.write_sav(self._pd_answers_data, f'{file_to_save}.sav', file_label=f'{self._sav_file_label}', column_labels=self._column_labels, variable_value_labels=self._variable_value_labels, variable_measure=self._variable_measure, variable_format=self._formats)

      print(file_to_save + '.sav')
      # self._logger.info("SAV file export: SUCCESS")

    except Exception as e:
      with open('traceback.txt', 'a') as f:
        # print(traceback.format_exc())
        f.write(str(e))
        f.write(traceback.format_exc())

      # download file with traceback
      with open(file_to_save, 'w') as f:
        f.write(str(e))
        f.write(traceback.format_exc())
        print(file_to_save)

if __name__ == '__main__':

  poll_id = sys.argv[1]

  export_data = SavExporter(poll_id=poll_id)
  export_data.file_name_generator()
  export_data.fetch_questions()
  export_data.fetch_answers()
  export_data.check_missing_data()
  export_data.check_data_lengths()
  export_data.save_file()
