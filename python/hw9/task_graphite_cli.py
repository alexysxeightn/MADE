"""Script for generate graphite commands"""
from argparse import ArgumentParser
from datetime import datetime


def str_to_time(time_str):
    """Function for get timestamp"""
    return datetime.strptime(time_str, "%Y%m%d_%H%M%S.%f").timestamp()


def callback_parse_log(arguments):
    """ Main function """
    host = arguments.host
    port = arguments.port

    query_info = dict()

    with open(arguments.process, 'r') as fin:
        for log in fin:
            left, query = log.split(':')
            left_split = left.split()
            time = left_split[0]
            text = ' '.join(left_split[3:])

            if 'start' in text:
                query_info[query] = dict()
                start_time = str_to_time(time)
                query_info[query]['start'] = start_time

            elif 'found' in text:
                article_found = text.split()[1]
                query_info[query]['article_found'] = article_found

            elif 'finish' in text:
                finish_time = str_to_time(time)
                query_info[query]['finish'] = finish_time

                start_time = query_info[query]['start']
                article_found = query_info[query]['article_found']

                diff_time = finish_time - start_time
                finish_time = int(finish_time)

                print("echo \"wiki_search.article_found %s %s\" | nc -N %s %s" %
                      (article_found, finish_time, host, port))
                print("echo \"wiki_search.complexity %0.3f %s\" | nc -N %s %s" %
                      (diff_time, finish_time, host, port))


def setup_parser(parser):
    """ Function for add arguments in parser """
    parser.add_argument(
        "--process", required=True,
        help="name file with log",
    )

    parser.add_argument(
        "--host", default="localhost",
    )

    parser.add_argument(
        "--port", default="2003",
    )

    parser.set_defaults(callback=callback_parse_log)


if __name__ == "__main__":
    parser = ArgumentParser()
    setup_parser(parser)
    arguments = parser.parse_args()
    arguments.callback(arguments)
