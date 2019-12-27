class DBRouter:
    @staticmethod
    def db_for_read(model, **hints):
        if model._meta.app_label == "java_wallet":
            return "java_wallet"
        return None

    @staticmethod
    def db_for_write(model, **hints):
        if model._meta.app_label == "java_wallet":
            return "java_wallet"
        return None

    @staticmethod
    def allow_relation(obj1, obj2, **hints):
        if (
            obj1._meta.app_label == "java_wallet"
            or obj2._meta.app_label == "java_wallet"
        ):
            return True
        return None

    @staticmethod
    def allow_migrate(db, app_label, model_name=None, **hints):
        if app_label == "java_wallet":
            return db == "java_wallet"
        return None
