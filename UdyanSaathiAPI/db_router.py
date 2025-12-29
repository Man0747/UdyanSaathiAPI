"""
Database router to use production database for reads and local for writes
Routes queries intelligently based on model type
"""

class ProductionRouter:
    """
    Routes database queries:
    - Read queries for pollution data → production database (Azure)
    - Write queries and new models → local database (SQLite)
    """
    
    # Models that should use production DB for reads
    production_models = {
        'stationmodel',
        'stationscoordinatesmodel', 
        'pollutionmodel',
        'aqicalendarmodel',
        'hourlymodel',
        'mlmodel',
        'mapdatamodel'
    }
    
    def db_for_read(self, model, **hints):
        """
        Reads from production database for pollution data models
        """
        if model._meta.model_name.lower() in self.production_models:
            return 'production'
        return 'default'
    
    def db_for_write(self, model, **hints):
        """
        Writes go to local database (for ward data, dispatch data, etc.)
        """
        return 'default'
    
    def allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if both models are in the same database
        """
        return True
    
    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Only migrate new models (Ward, DispatchTicket) to local DB
        Don't migrate production models to local DB
        """
        if model_name and model_name.lower() in self.production_models:
            return db == 'production'
        return db == 'default'
