from django.contrib.messages import constants #constants para setar as classes css dos tipos de messages


MESSAGE_TAGS = { 
    constants.DEBUG : 'message-debug',
    constants.SUCCESS : 'message-success',
    constants.INFO : 'message-info',
    constants.WARNING : 'message-warning',
    constants.ERROR : 'message-error',
}