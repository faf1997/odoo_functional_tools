import logging
import subprocess
import shlex

from odoo import models

_logger = logging.getLogger(__name__)


class QueueJob(models.Model):
    _inherit = 'queue.job'

    def launch_queue_job(self):
        _logger.info('Launching ensure_processes from launch_queue_job')
        self.ensure_processes()

    def is_running(self, name):
        _logger.debug('Checking if process is running: %s', name)
        result = subprocess.run(['ps', 'aux'], capture_output=True, text=True)
        running = any(name in line and 'grep' not in line for line in result.stdout.splitlines())
        _logger.debug('Process %s running: %s', name, running)
        return running

    def start_process(self, command):
        _logger.warning('Starting process: %s', command)
        try:
            subprocess.Popen(shlex.split(command))
            _logger.info('Process started: %s', command)
        except Exception as e:
            _logger.error('Failed to start %s: %s', command, e)

    def ensure_processes(self):
        services = {
            'queue_job': 'odoo-bin --load=queue_job'
        }
        for name, cmd in services.items():
            if self.is_running(name):
                _logger.info('Service already running: %s', name)
            else:
                _logger.info('Service not running, will launch: %s', name)
                self.start_process(cmd)
