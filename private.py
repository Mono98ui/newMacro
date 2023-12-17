import os
class Private:

    def __init__(self):
        os.environ['DB_NAME'] = 'MacroDB'
        os.environ['DB_USER'] = 'Test_user'
        os.environ['DB_PASSWORD'] = 'test'
        os.environ['WEB_DRIVER_PATH'] = 'C:/Program Files/Mozilla Firefox/firefox.exe'
        os.environ['MAIL_BOT_PWD'] = 'nucgpfaiqqnhypmw'
        os.environ['MAIL_BOT'] = 'macrobot165@gmail.com'
        os.environ['MAIL_BOT_DEST'] = 'Jdannypham@gmail.com'

    def clean(self):        
        os.environ.pop('DB_NAME')
        os.environ.pop('DB_USER')
        os.environ.pop('DB_PASSWORD')
        os.environ.pop('WEB_DRIVER_PATH')
        os.environ.pop('MAIL_BOT_PWD')
        os.environ.pop('MAIL_BOT')
        os.environ.pop('MAIL_BOT_DEST')