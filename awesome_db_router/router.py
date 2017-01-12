class AwesomeGameRouter(object):
    def db_for_read(self, model, **hints):
        if model._meta.app_label in ['awesome_users', 'awesome_rooms']:
            return 'common'
        return 'default'

    def db_for_write(self, model, **hints):
        if model._meta.app_label in ['awesome_users', 'awesome_rooms']:
            return 'common'
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth app is involved.
        """
        return True

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth app only appears in the 'auth_db'
        database.
        """
        if app_label in ['awesome_users', 'awesome_rooms']:
            return db == 'common'
        else:
            return db == 'default'
