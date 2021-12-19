from argparse import Namespace

from task_graphite_cli import callback_parse_log


WIKIPEDIA_LOG_DUMP_FILEPATH = 'wiki_search_app.log'
CORRECT_OUT_FILEPATH = 'correct_out_for_parse_log.txt'


def test_callback_parse_log_work_correct(capsys):
	arguments = Namespace(
		process=WIKIPEDIA_LOG_DUMP_FILEPATH,
		host='test_host',
		port=666,
	)
	callback_parse_log(arguments)
	captured = capsys.readouterr().out.split('\n')
	with open(CORRECT_OUT_FILEPATH) as fin:
		correct_out = fin.read().split('\n')
	for out_string in captured:
		assert out_string in correct_out