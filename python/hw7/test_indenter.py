import pytest

from task_indenter import Indenter

def test_indenter_without_params_work_correct(capsys):
	with Indenter() as indent:
		indent.print("hi")
		with indent:
			indent.print("hello")
			with indent:
				indent.print("bonjour")
		indent.print("hey")

	correct_answer = ['hi', ' ' * 4 + 'hello', ' ' * 8 + 'bonjour', 'hey']
	captured = capsys.readouterr().out.strip().split('\n')
	assert correct_answer == captured


def test_indenter_with_params_work_correct(capsys):
	with Indenter(indent_str="--", indent_level=1) as indent:
		indent.print("hi")
		with indent:
			indent.print("hello")
			with indent:
				indent.print("bonjour")
		indent.print("hey")

	indent_str = '--'
	correct_answer = [indent_str + 'hi', indent_str * 2 + 'hello', indent_str * 3 + 'bonjour', indent_str + 'hey']
	captured = capsys.readouterr().out.strip().split('\n')
	assert correct_answer == captured