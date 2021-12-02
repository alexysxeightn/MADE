import pytest

from task_repeater import (
	verbose_context, verbose, repeater
)

def test_repeater_work_correct(capsys):
	@repeater(5)
	def print_test_message():
		"""doc_string for print_test_message"""
		print("Test message")
	print_test_message()

	captured = capsys.readouterr().out.strip().split('\n')
	assert 5 * ["Test message"] == captured
	assert "doc_string for print_test_message" == print_test_message.__doc__
	assert "print_test_message" == print_test_message.__name__


def test_verbose_work_correct(capsys):
	@verbose
	def print_test_message():
		"""doc_string for print_test_message"""
		print("Test message")
	print_test_message()

	correct_answer = ['before function call', 'Test message', 'after function call']
	captured = capsys.readouterr().out.strip().split('\n')
	assert correct_answer == captured
	assert "doc_string for print_test_message" == print_test_message.__doc__
	assert "print_test_message" == print_test_message.__name__


def test_class_verbose_context_work_correct(capsys):
	@verbose_context()
	def print_test_message():
		"""doc_string for print_test_message"""
		print("Test message")
	print_test_message()

	correct_answer = ['class: before function call', 'Test message', 'class: after function call']
	captured = capsys.readouterr().out.strip().split('\n')
	assert correct_answer == captured
	assert "doc_string for print_test_message" == print_test_message.__doc__
	assert "print_test_message" == print_test_message.__name__


def test_all_decorator_together_work_correct(capsys):
	@verbose_context()
	@repeater(4)
	@verbose
	def print_test_message():
		"""doc_string for print_test_message"""
		print("Test message")
	print_test_message()

	correct_answer = ['class: before function call'] + \
					 4 * ['before function call','Test message', 'after function call'] + \
					 ['class: after function call']
	captured = capsys.readouterr().out.strip().split('\n')
	assert correct_answer == captured
	assert "doc_string for print_test_message" == print_test_message.__doc__
	assert "print_test_message" == print_test_message.__name__