import utilities as ut
import dumper

import time

class NotificationManager(dumper.Dumper):
    def __init__(self, dumpfile, groups):
        super().__init__(dumpfile)

        self.messages = dict()

        self.groups = groups

    def create_notification(self, user, sender, message, timestamp):
        """
        create_notification(user, sender, message, timestamp) -> None
        """

        if user not in self.messages:
            self.messages[user] = []

        self.messages[user].append((sender, message, timestamp))

    def add_notification(self, user, sender, message, timestamp):
        """
        add_notification(user, sender, message, timestamp) -> None

        Add notification for a certain user or group.
        """

        tp = user[0]
        receiver = ut.filter_nick(user[1:])

        if tp == "@":  #Normal notification
            self.create_notification(receiver, sender, message, timestamp)
        elif tp == "*":  #Group notification
            for p in self.groups.get_users(receiver):
                if p not in self.messages:
                    self.messages[p] = []
                self.create_notification(p, sender, message, timestamp)
        else:
            return

        return "Message will be delivered to %s." % user

    def get_notifications(self, user):
        """
        get_notifications(user) -> List

        Clear and return all messages for a certain user.
        """

        messages = []
        if user in self.messages:
            messages = self.messages[user]
            self.messages[user] = []

        conmessages = []
        for message in messages:
            user, content, timestamp = message
            cm = "[" + user + ", " + ut.extract_time(int(time.time()) -
                            timestamp) + " ago] " + content
            conmessages.append(cm)

        return conmessages

    def has_notifications(self, user):
        """
        has_notifications(user) -> Bool

        Tests if a user has some notifications waiting for them.
        """

        if user in self.messages and self.messages[user] != []:
            return True
        else:
            return False

    def dump_notifications(self):
        self.dump(self.messages)

    def recover_notifications(self):
        self.messages = self.recover()
        if self.messages is None:
            self.messages = dict()
