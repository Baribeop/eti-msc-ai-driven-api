def calculate_scs(data, depth=1):

    if isinstance(data, dict):

        return depth + sum(
            calculate_scs(v, depth + 1)
            for v in data.values()
        )

    elif isinstance(data, list):

        return depth + sum(
            calculate_scs(i, depth + 1)
            for i in data
        )

    return depth


