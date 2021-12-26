import logging
import logging.handlers
import sys
import time
import os


def make_dir(make_dir_path):
	path = make_dir_path.strip()
	if not os.path.exists(path):
		os.makedirs(path)
	return path


def get_logger():
	file_path = sys.argv[0]
	dir_path, file_name = os.path.split(file_path)

	log_dir_name = 'logs'
	log_file_name = 'logger-' + time.strftime('%Y-%m-%d', time.localtime(time.time())) + '.logs'
	log_file_folder = dir_path + os.sep + log_dir_name
	make_dir(log_file_folder)
	log_file_str = log_file_folder + os.sep + log_file_name

	logging.root.setLevel(logging.NOTSET)

	logger = logging.getLogger('scheduler')
	logger.setLevel(logging.NOTSET)
	fileout_handler = logging.FileHandler(log_file_str, mode='a', encoding='UTF-8')
	fileout_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
	stdout_handler = logging.StreamHandler()
	stdout_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
	logger.addHandler(stdout_handler)
	logger.addHandler(fileout_handler)
	return logger


logger = get_logger()
