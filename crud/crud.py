class CRUD:
    
    @staticmethod
    def save(db, model):
        """Saves an instance model to the database"""
        db.add(model)
        db.commit()
        return model
    
    @staticmethod
    def update(db) -> None:
        """Commits changes to the database"""
        db.commit()
    
    @staticmethod
    def delete(db, model) -> None:
        """Deletes a record from the database through an instance model"""
        db.delete(model)
        db.commit()
