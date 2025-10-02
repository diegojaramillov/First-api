from models.series import Series
from extensions import db

class SeriesRepository:

    @staticmethod
    def create_series(title, description=None, year=None):
        s = Series(title=title, description=description, year=year)
        db.session.add(s)
        db.session.commit()
        return s

    @staticmethod
    def get_all():
        return Series.query.order_by(Series.id.asc()).all()

    @staticmethod
    def get_by_id(series_id):
        return Series.query.get(series_id)

    @staticmethod
    def update_series(series_obj):
        db.session.commit()
        return series_obj

    @staticmethod
    def delete_series(series_obj):
        db.session.delete(series_obj)
        db.session.commit()
