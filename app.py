import argparse
import logging
import os
from typing import Iterator

import gpxpy
from gpxpy.gpx import GPXWaypoint


def parse_cmd_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--working-directory", type=str, help='Directory to look for gpx files')
    parser.add_argument("--gpx-file", type=str, help="GPX file to update")
    parser.add_argument('--overwrite-symbol', action='store_true', help='Overwrite the waypoint symbols.')
    parser.add_argument('--verbose', action='store_true')

    return parser.parse_args()


def find_gpx_files(working_dir: str) -> Iterator[str]:
    for file in os.listdir(working_dir):
        if file.endswith(".gpx"):
            yield os.path.join(working_dir, file)


def get_locus_icon(number: int) -> str:
    return f'file:Locus Misc.zip:number_{number}.png'


def missing_symbol(waypoint: GPXWaypoint) -> bool:
    return waypoint.symbol is None or 'Locus Misc.zip' not in waypoint.symbol


def update_gpx(gpx_file_path: str) -> gpxpy.gpx:
    with open(gpx_file_path, 'r', encoding='utf-8') as gpx_file:
        gpx = gpxpy.parse(gpx_file)

        waypoint: GPXWaypoint
        if any([missing_symbol(waypoint) for waypoint in gpx.waypoints]):
            for number, waypoint in enumerate(gpx.waypoints, start=1):
                waypoint.symbol = get_locus_icon(number)

            return gpx


def main() -> None:
    args = parse_cmd_arguments()

    if args.working_directory:
        for gpx_file in find_gpx_files(args.working_directory):
            updated_gpx_file = update_gpx(gpx_file)

            if updated_gpx_file:
                with open(gpx_file, 'w', encoding='utf-8') as gpx_fp:
                    gpx_fp.write(updated_gpx_file.to_xml())
                    logging.info(f'Updated {gpx_file}')
    elif args.gpx_file:
        updated_gpx_file = update_gpx(args.gpx_file)

        if updated_gpx_file:
            with open(args.gpx_file, 'w', encoding='utf-8') as gpx_fp:
                gpx_fp.write(updated_gpx_file.to_xml())
                logging.info(f'Updated {args.gpx_file}')


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format="%(threadName)s::%(asctime)s::%(message)s")

    main()
