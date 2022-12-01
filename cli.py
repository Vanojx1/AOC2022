import click
import importlib
import time

@click.command()
@click.option('--day', prompt='OAC day', help='Select AOC day to run.')

def main(day):
    try:
        my_module = importlib.import_module(f'days.day{day}.day')
    except Exception:
        print('Day not found!')
        exit(0)

    with open(f'days\\day{day}\\input') as f:
        day_input = f.read().splitlines()
    
    click.echo()
    click.echo(f'Running day {day}')

    start_time = time.time()
    part1, part2 = my_module.main(day_input)

    click.echo("Done in {:.2f} ms".format((time.time() - start_time) * 1000))
    click.echo(f'Part 1: {part1}')
    click.echo(f'Part 2: {part2}')

if __name__ == '__main__':
    main()