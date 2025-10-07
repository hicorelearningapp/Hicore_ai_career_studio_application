from sqlalchemy.orm import Session

class BaseManager:
    def __init__(self, db: Session):
        self.db = db

    def add(self, instance):
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)
        return instance

    def get_by_id(self, model, _id):
        return self.db.query(model).filter(model.id == _id).first()
