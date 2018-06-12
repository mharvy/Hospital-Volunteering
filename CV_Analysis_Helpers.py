def percent_corrector(percents):
    new_percents = []
    total_percent = 0
    for percent in percents:
        total_percent += percent
        new_percents.append(total_percent)
    return new_percents
