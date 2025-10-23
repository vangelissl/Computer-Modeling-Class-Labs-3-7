import pandas as pd
import os
import msvcrt
from pick_up_point import PickUpPoint
from o_statistics import Statistics
from datetime import datetime
from plots import plot_time_distribution, plot_distribution, plot_line
from modified_plots import plot_metrics

STEP = 0.25
STEP_COUNT = int(10 / STEP)

stats = Statistics(STEP)
PUP = PickUpPoint(stats, datetime(2025, 1, 1, 10), STEP, 1)


def simulation(pup: PickUpPoint = PUP):
    for i in range(STEP_COUNT):
        pup.client_arrived()
        pup.client_service()
        if i == STEP_COUNT - 1:
            pup.end_shift()
        pup.end_interval_simulation()
        pup.increase_time()


def long_term_simulation(days: int, pup=PUP):
    for i in range(days):
        simulation(pup)
        pup.next_day()


def main_menu():
    run = True
    while run:
        clear_screen()
        print('--------------MENU--------------')
        print('1. Create new dataset')
        print('2. Load existing dataset')
        print('3. See graphs')
        print('11. Modified menu')
        print('-' * 33)

        if not stats.df.empty:
            print('5. View current logs statistics')
            print('6. View correlation of general metrics')
            print('7. View correlation of client metrics')
            print('8. Peek general statistics')
            print('9. Peek client logs')
            print('10. View general statistics')

        print('4. Exit')
        print('-' * 33)

        command = int(input('Choose command: '))
        match(command):
            case 1:
                create_dataset()
            case 2:
                load_dataset()
            case 3:
                graph_menu()
            case 4:
                run = False
            case 5:
                if not stats.client_logs.empty:
                    clear_screen()
                    print(stats.client_logs.describe())
                    press_key()
            case 6:
                if not stats.df.empty:
                    clear_screen()
                    df = stats.df.copy(deep=True)
                    df['hour'] = stats.df['datetime'].dt.hour + \
                        stats.df['datetime'].dt.minute / 60
                    print(df.corr())
                    press_key()
            case 7:
                if not stats.client_logs.empty:
                    clear_screen()
                    print(stats.client_logs.corr())
                    press_key()
            case 8:
                if not stats.df.empty:
                    clear_screen()
                    print(stats.df.head())
                    press_key()
            case 9:
                if not stats.client_logs.empty:
                    clear_screen()
                    print(stats.client_logs.head())
                    press_key()
            case 10:
                if not stats.df.empty:
                    clear_screen()
                    print(stats.df.describe())
                    press_key()
            case 11:
                clear_screen()
                modified_menu()
                press_key()
            case _:
                command_not_found()


def modified_menu():
    run = True
    days = 0 
    df = None
    while run:
        clear_screen()
        print('-------------MODIFIED MENU-------------')
        print('1. Create dataset')
        if df is not None and not df.empty:
            print('2. See graphs')
            print('3. See statistics')
        command = int(input('Choose command: '))
        match(command):
            case 1:
                clear_screen()
                df, days = create_modified_dataset()
                press_key()
            case 2:
                if df is not None:
                    plot_metrics(df, f'Imitation model results by {days} days')
            case 3:
                if df is not None:
                    clear_screen()
                    print(df.round(3))
                    press_key()
            case 4:
                run = False


def create_modified_dataset():
    min_workers = int(input('Min workers: '))
    max_workers = int(input('Max workers: '))
    number_of_days = int(input('Number of days: '))
    results = {}
    for c in range(min_workers, max_workers + 1):
        statistics = Statistics(STEP)
        pup = PickUpPoint(statistics, datetime(
            2025, 1, 1, 10), STEP, c)
        long_term_simulation(number_of_days, pup)
        results[f'c = {c}'] = statistics.get_averaged_data()

    df_sim = pd.DataFrame(results)
    return df_sim, number_of_days


def create_dataset():
    data_run = True
    while data_run:
        try:
            clear_screen()
            print('--------------DATA--------------')
            print('Create new simulation by specifying number of days')
            days_number = int(input('Number of days: '))
            stats.clear()
            long_term_simulation(days_number)
            filename = input('Filename (optional): ')
            if filename != '':
                path = f'datasets\\'
                stats_path = path + filename + '.xlsx'
                logs_path = path + 'logs\\' + filename + '_logs.xlsx'
                df_to_write = stats.df.copy(deep=True)
                df_to_write["datetime"] = stats.df["datetime"].dt.strftime(
                    "%m/%d/%Y, %H:%M:%S")
                df_to_write.to_excel(
                    stats_path, sheet_name=f'{len(df_to_write) / STEP_COUNT}', index=False)
                stats.client_logs.to_excel(
                    logs_path, sheet_name=f'{len(df_to_write) / STEP_COUNT}', index=False)
                print(f'All done.')
                print(f'Results are stored in "{stats_path}"')
                print(f'Logs are stored in "{logs_path}"')
            data_run = False
            press_key()

        except Exception as e:
            clear_screen()
            print(e)
            print('Something went wrong. Try again')
            answer = input('Try again (y/n): ')
            data_run = True if answer.lower() == 'y' else False


def load_dataset():
    run = True
    while run:
        try:
            clear_screen()
            print('----------------LOAD DATA-----------------')
            print('Load dataset from existing file')
            filename = input('Filename: ')
            path = f'datasets\\'
            dataset_path = path + filename + '.xlsx'
            logs_path = path + 'logs\\' + filename + '_logs.xlsx'
            stats.df = pd.read_excel(dataset_path, parse_dates=['datetime'])
            stats.client_logs = pd.read_excel(logs_path)
            print('Dataset has been loaded successfully')
            run = False
            press_key()
        except Exception as e:
            clear_screen()
            print(e)
            print('Something went wrong. Try again')
            answer = input('Try again (y/n): ')
            run = True if answer.lower() == 'y' else False


def graph_menu():
    graph_run = True
    while graph_run:
        clear_screen()
        print('------------Distibution Over Time------------')
        print('1. Lost clients')
        print('2. Served clients')
        print('3. Queue')
        print('------------Frequency Distibution------------')
        print('4. Total clients')
        print('5. Products')
        print('6. Service duration')
        print('------------Special Metrics------------')
        print('7. Throughput')
        print('8. Utilization')
        print('---------------------------------------------')
        print('9. Back')
        print('-------------------------------')
        command = int(input('Choose command: '))

        match(command):
            case 1:
                plot_time_distribution(stats.df, STEP)
            case 2:
                plot_time_distribution(stats.df, STEP, 'served clients')
            case 3:
                plot_time_distribution(stats.df, STEP, 'queue')
            case 4:
                plot_distribution(stats.df, 'clients total')
            case 5:
                plot_distribution(stats.client_logs)
            case 6:
                plot_distribution(stats.client_logs, 'duration')
            case 7:
                plot_line(stats.df)
            case 8:
                plot_line(stats.df, 'utilization')
            case 9:
                graph_run = False
            case _:
                command_not_found()


def clear_screen():
    os.system('cls')


def press_key():
    print('Press any key to continue...')
    continue_key = msvcrt.getch()


def command_not_found():
    print('Command not found. Try again')
    press_key()


def add_hour_column():
    stats.df['hour'] = stats.df['datetime'].hour + \
        stats.df['datetime'].minutes / 60


if __name__ == '__main__':
    main_menu()
