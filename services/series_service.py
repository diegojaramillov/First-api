from repositories.series_repository import SeriesRepository

class SeriesService:

    @staticmethod
    def list_series():
        return SeriesRepository.get_all()

    @staticmethod
    def get_series(series_id):
        return SeriesRepository.get_by_id(series_id)

    @staticmethod
    def create_series(data):
        title = data.get('title')
        description = data.get('description')
        year = data.get('year')
        return SeriesRepository.create_series(title, description, year)

    @staticmethod
    def update_series(series_obj, data):
        series_obj.title = data.get('title', series_obj.title)
        series_obj.description = data.get('description', series_obj.description)
        series_obj.year = data.get('year', series_obj.year)
        return SeriesRepository.update_series(series_obj)

    @staticmethod
    def delete_series(series_obj):
        return SeriesRepository.delete_series(series_obj)
