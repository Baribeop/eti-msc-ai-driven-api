# from influxdb_client import InfluxDBClient
# from app.config import INFLUX_URL


# class InfluxAdapter:

#     def __init__(self):

#         self.client = InfluxDBClient(url=INFLUX_URL)

#     def insert(self, data):

#         print("Stored in InfluxDB")

#         return True

from influxdb_client import InfluxDBClient

from app.config import INFLUX_URL


class InfluxAdapter:

    def __init__(self):

        self.client = InfluxDBClient(
            url=INFLUX_URL
        )

    def write_point(self, data):

        print("Influx point written")

        return {
            "status": "point_written"
        }

    def batch_write(self, data):

        print("Influx batch write")

        return {
            "status": "batch_written",
            "count": len(data)
        }