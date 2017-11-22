from IPython.core.magic import register_line_magic
from IPython.lib import backgroundjobs as bg

@register_line_magic
def start(fun):
    jobs = bg.BackgroundJobManager()
    jobs.new(fun)
    return jobs
