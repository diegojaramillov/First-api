from extensions import db

class Series(db.Model):
    __tablename__ = 'series'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    year = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'year': self.year,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
