import euphoria

import notification
import groups
import notifybot

class MultiRoom(euphoria.execgroup.ExecGroup):
    def __init__(self, rooms):
        super().__init__()

        grouping = groups.GroupManager("group_dump.txt")
        grouping.recover_groups()

        notifies = notification.NotificationManager("message_dump.txt", grouping)
        notifies.recover_notifications()

        for i in rooms:
            self.add(notifybot.NotifyBot(notifies, grouping, 60, i, rooms[i]))
