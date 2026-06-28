# # from influxdb_client import InfluxDBClient
# # from app.config import INFLUX_URL


# # class InfluxAdapter:

# #     def __init__(self):

# #         self.client = InfluxDBClient(url=INFLUX_URL)

# #     def insert(self, data):

# #         print("Stored in InfluxDB")

# #         return True

# from influxdb_client import InfluxDBClient

# from app.config import INFLUX_URL


# class InfluxAdapter:

#     def __init__(self):

#         self.client = InfluxDBClient(
#             url=INFLUX_URL
#         )

#     def write_point(self, data):

#         print("Influx point written")

#         return {
#             "status": "point_written"
#         }

#     def batch_write(self, data):

#         print("Influx batch write")

#         return {
#             "status": "batch_written",
#             "count": len(data)
#         }


"""
influx_adapter.py (CORRECTED)
-------------------------------
Same security model as the other adapters: every method accepts a
`connection` dict supplied by the calling client in the SAME request,
builds a short-lived InfluxDBClient from it, writes the point(s), and
closes the connection immediately after. No credentials are stored,
logged, or persisted by this middleware.

STORAGE MODEL NOTE:
InfluxDB stores time-series "points," each with a measurement name,
optional tags (indexed, string-valued metadata), fields (the actual
numeric/string values being recorded), and a timestamp. This adapter
maps an arbitrary incoming payload onto this model as follows: any
top-level key with a numeric value becomes a field; any top-level key
with a string/boolean value becomes a tag; a "measurement" key in the
payload (or connection["measurement"]) selects the measurement name,
defaulting to "polyglot_data"; a "timestamp" key in the payload is used
if present, otherwise InfluxDB's server-side current time is used.

Expected `connection` dict shape:
{
    "type": "influxdb",
    "url": "http://localhost:8086",
    "token": "my-influx-token",
    "org": "my-org",
    "bucket": "my-bucket",
    "measurement": "sensor_readings"   # optional, defaults to "polyglot_data"
}
"""

from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
import logging

logger = logging.getLogger(__name__)


class InfluxAdapter:

    def _build_client(self, connection: dict):
        required = ["url", "token", "org", "bucket"]
        missing = [f for f in required if not connection.get(f)]
        if missing:
            raise ValueError(f"Missing required connection fields: {missing}")

        client = InfluxDBClient(
            url=connection["url"],
            token=connection["token"],
            org=connection["org"],
        )
        return client

    def _build_point(self, data: dict, measurement: str) -> Point:
        point = Point(measurement)
        for key, value in data.items():
            if key in ("measurement", "timestamp"):
                continue
            if isinstance(value, bool):
                point = point.field(key, value)
            elif isinstance(value, (int, float)):
                point = point.field(key, value)
            elif isinstance(value, str):
                point = point.tag(key, value)
            # nested dict/list values are skipped - Influx points are flat
            # by design; this is a known limitation noted in the thesis.
        if "timestamp" in data:
            point = point.time(data["timestamp"])
        return point

    def insert(self, data, connection: dict = None):
        """Generic entry point matching the other adapters' insert()
        signature, so main.py's /persist handler can call all five
        adapters uniformly. Delegates to write_point()."""
        return self.write_point(data, connection=connection)

    def write_point(self, data, connection: dict = None):
        if connection is None:
            raise ValueError("InfluxAdapter.write_point() requires a connection dict")

        client = self._build_client(connection)
        try:
            data_dict = dict(data)
            measurement = data_dict.get("measurement") or connection.get("measurement", "polyglot_data")
            bucket = connection["bucket"]

            point = self._build_point(data_dict, measurement)

            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=bucket, org=connection["org"], record=point)

            logger.info(f"Influx point written: measurement={measurement}, bucket={bucket}")
            return {
                "status": "point_written",
                "database": "influxdb",
                "measurement": measurement,
                "bucket": bucket
            }
        finally:
            client.close()

    def batch_write(self, data: list, connection: dict = None):
        if connection is None:
            raise ValueError("InfluxAdapter.batch_write() requires a connection dict")

        client = self._build_client(connection)
        try:
            bucket = connection["bucket"]
            measurement_default = connection.get("measurement", "polyglot_data")

            points = []
            for item in data:
                item_dict = dict(item)
                measurement = item_dict.get("measurement") or measurement_default
                points.append(self._build_point(item_dict, measurement))

            write_api = client.write_api(write_options=SYNCHRONOUS)
            write_api.write(bucket=bucket, org=connection["org"], record=points)

            logger.info(f"Influx batch write successful: count={len(points)}, bucket={bucket}")
            return {
                "status": "batch_written",
                "database": "influxdb",
                "bucket": bucket,
                "count": len(points)
            }
        finally:
            client.close()
