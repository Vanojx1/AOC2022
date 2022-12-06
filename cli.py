import click
import importlib
import time
from colorama import just_fix_windows_console
from termcolor import colored
from art import tprint

TEXT_COLOR = 'red'

just_fix_windows_console()

@click.command()
@click.option('--day', prompt='OAC day', help='Select AOC day to run.')

def main(day):
    try:
        my_module = importlib.import_module(f'days.day{day}.day')
    except ModuleNotFoundError:
        print('Day not found!')
        exit(0)

    with open(f'days\\day{day}\\input') as f:
        day_input = f.read().splitlines()
    
    click.echo()
    click.echo('Running ' + colored(f'Day {day}', TEXT_COLOR))

    start_time = time.time()
    part1, part2 = map(str, my_module.main(day_input))

    click.echo("Done in {:.2f} ms".format((time.time() - start_time) * 1000))
    click.echo('Part ' + colored('1', TEXT_COLOR) + f': {part1}')
    tprint(part1)
    click.echo('Part ' + colored('2', TEXT_COLOR) + f': {part2}')
    tprint(part2)

if __name__ == '__main__':
    main()