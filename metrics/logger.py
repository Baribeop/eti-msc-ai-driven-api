# from time import perf_counter


# class PerformanceLogger:

#     def start(self):
#         return perf_counter()

#     def stop(self, start):

#         return round(
#             (perf_counter() - start) * 1000,
#             3
#         )


from time import perf_counter


class MetricsLogger:

    def start(self):

        return perf_counter()

    def stop(self, start):

        return round(
            (perf_counter() - start) * 1000,
            3
        )

    def log_operation(
        self,
        database,
        strategy,
        latency
    ):

        print({

            "database": database,

            "strategy": strategy,

            "latency_ms": latency
        })