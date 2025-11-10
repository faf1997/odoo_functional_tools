from . import models

def post_init_hook(env):
    env['resource.calendar.leaves'].sudo().create_holidays()