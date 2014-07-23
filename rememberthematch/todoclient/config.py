class ToDoClientConfiguration(object):

    def __init__(self, username, password, project=None, dry_run=False):
        self.username = username
        self.password = password
        self.project = project
        self.dry_run = dry_run
