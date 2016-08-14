class ToDoClientConfiguration(object):

    def __init__(self, api_token, project=None, dry_run=False):
        self.api_token = api_token
        self.project = project
        self.dry_run = dry_run
