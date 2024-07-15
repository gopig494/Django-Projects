from Learning_ORM_queries.models import DBTransactions

# This example won’t work if any of the models in myapp contain relationships to models outside of the other database. 
# Cross-database relationships introduce referential integrity problems that Django can’t currently handle.

class MyRouter:

    # use different databse in app level is advicable so we have to check only the app label is enought

    app_names = ["customer","Learning_ORM_queries"]

    def db_for_read(self, model, **hints):
        # print(f"-------------------model name-------------{model._meta.model_name}-----")
        if model._meta.app_label in MyRouter.app_names:
            print(f"-------------------app name-------------{model._meta.app_label}-----")
            if model._meta.app_label == "Learning_ORM_queries":
                return 'postgresql_db'
            return "sql_lite_db"
        return None
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label in MyRouter.app_names:
            if model._meta.app_label == "Learning_ORM_queries":
                return 'postgresql_db'
            return "sql_lite_db"
        return 'postgresql_db'

    def allow_relation(self, obj1, obj2, **hints):

        # Return True if a relation between obj1 and obj2 should be allowed, False if the relation should be prevented, or None if the router has no opinion. This is purely a validation operation, 
        # used by foreign key and many to many operations to determine if a relation should be allowed between two objects.

        """
        Allow relations if both models are in same db whcih means if relation model is in another db it won't work
        """
        if obj1._meta.app_label in MyRouter.app_names or obj2._meta.app_label in MyRouter.app_names:
            if obj1._meta.app_label == 'Learning_ORM_queries':
                if obj1._meta.app_label == 'Learning_ORM_queries' and obj2._meta.app_label == 'Learning_ORM_queries':
                    return True
                return False
        return True


    def allow_migrate(self, db, app_label, model_name=None, **hints):

        print("--------db-->",db)
        print("--------app_label-->",app_label)
        print("--------model_name-->",model_name)
        print("--------hints-->",hints)

        # makemigrations always creates migrations for model changes, but if allow_migrate() returns False, any migration operations for the model_name will be silently skipped when running migrate on the db. Changing the behavior of allow_migrate() for models that already have migrations may result in broken foreign keys, extra tables, or missing tables. 
        # When makemigrations verifies the migration history, it skips databases where no app is allowed to migrate


        # Hints¶

        # The hints received by the database router can be used to decide which database should receive a given request.

        # At present, the only hint that will be provided is instance, an object instance that is related to the read or write operation that is underway. This might be the instance that is being saved, or it might be an instance that is being added in a many-to-many relation. In some cases, no instance hint will be provided at all. The router checks for the existence of an instance hint, and determine if that hint should be used to alter routing behavior.

        # if true means the migration will be continue or false means the migration will be skipped

        if app_label in MyRouter.app_names:
            if app_label == 'Learning_ORM_queries':
                return db == 'postgresql_db'
        return True
    
    # A router doesn’t have to provide all these methods – it may omit one or more of them. 
    # If one of the methods is omitted, Django will skip that router when performing the relevant check.

from Learning_ORM_queries.models import DBTransactions

# This example won’t work if any of the models in myapp contain relationships to models outside of the other database. 
# Cross-database relationships introduce referential integrity problems that Django can’t currently handle.

class MyRouterCopy:

    # use different databse in app level is advicable so we have to check only the app label is enought

    app_names = ["customer","Learning_ORM_queries"]

    def db_for_read(self, model, **hints):
        # print(f"-------------------model name-------------{model._meta.model_name}-----")
        print(f"-------------------app name-----copy--------{model._meta.app_label}-----")
        if model._meta.app_label in MyRouter.app_names:
            if model._meta.app_label == "Learning_ORM_queries":
                return 'postgresql_db'
            return "sql_lite_db"
        return 'postgresql_db'
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label in MyRouter.app_names:
            if model._meta.app_label == "Learning_ORM_queries":
                return 'postgresql_db'
            return "sql_lite_db"
        return 'postgresql_db'

    def allow_relation(self, obj1, obj2, **hints):

        # Return True if a relation between obj1 and obj2 should be allowed, False if the relation should be prevented, or None if the router has no opinion. This is purely a validation operation, 
        # used by foreign key and many to many operations to determine if a relation should be allowed between two objects.

        """
        Allow relations if both models are in same db whcih means if relation model is in another db it won't work
        """
        if obj1._meta.app_label in MyRouter.app_names or obj2._meta.app_label in MyRouter.app_names:
            if obj1._meta.app_label == 'Learning_ORM_queries':
                if obj1._meta.app_label == 'Learning_ORM_queries' and obj2._meta.app_label == 'Learning_ORM_queries':
                    return True
                return False
        return True


    def allow_migrate(self, db, app_label, model_name=None, **hints):

        # makemigrations always creates migrations for model changes, but if allow_migrate() returns False, any migration operations for the model_name will be silently skipped when running migrate on the db. Changing the behavior of allow_migrate() for models that already have migrations may result in broken foreign keys, extra tables, or missing tables. 
        # When makemigrations verifies the migration history, it skips databases where no app is allowed to migrate


        # Hints¶

        # The hints received by the database router can be used to decide which database should receive a given request.

        # At present, the only hint that will be provided is instance, an object instance that is related to the read or write operation that is underway. This might be the instance that is being saved, or it might be an instance that is being added in a many-to-many relation. In some cases, no instance hint will be provided at all. The router checks for the existence of an instance hint, and determine if that hint should be used to alter routing behavior.

        # if true means the migration will be continue or false means the migration will be skipped

        if app_label in MyRouter.app_names:
            if app_label == 'Learning_ORM_queries':
                return db == 'postgresql_db'
        return True
    
    # A router doesn’t have to provide all these methods – it may omit one or more of them. 
    # If one of the methods is omitted, Django will skip that router when performing the relevant check.







#########2



class MyRouter_3:
    app_names = ["customer","Learning_ORM_queries"]

    def db_for_read(self, model, **hints):
        print(f"-------------------model name-------------{model._meta.model_name}-----")
        if model._meta.app_label in MyRouter.app_names:
            print(f"-------------------app name-------------{model._meta.app_label}-----")
            if model._meta.app_label == "Learning_ORM_queries":
                return 'postgresql_db'
            # return "sql_lite_db"
        return "postgresql_db"
    
    def db_for_write(self, model, **hints):
        if model._meta.app_label in MyRouter.app_names:
            if model._meta.app_label == "Learning_ORM_queries":
                return 'postgresql_db'
            # return "sql_lite_db"
        return 'postgresql_db'

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in MyRouter.app_names or obj2._meta.app_label in MyRouter.app_names:
            if obj1._meta.app_label == 'Learning_ORM_queries':
                if obj1._meta.app_label == 'Learning_ORM_queries' and obj2._meta.app_label == 'Learning_ORM_queries':
                    return True
                return False
        return True


    def allow_migrate(self, db, app_label, model_name=None, **hints):

        if model_name == "testmigrate2":
            print("--------db-->",db)
            print("--------app_label-->",app_label)
            print("--------model_name-->",model_name)
            print("--------hints-->",hints)
            # if app_label in MyRouter.app_names:
            #     return db == 'postgresql_db'
        return True
