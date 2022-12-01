def main(day_input):
    elfs_calories = [0]
    for food in day_input:
        if not food:
            elfs_calories.append(0)
            continue
        elfs_calories[-1] += int(food)
    
    return max(elfs_calories), sum(sorted(elfs_calories, reverse=True)[:3])