from dataclasses import dataclass
from datetime import datetime
from pprint import pp
from struct import unpack
from typing import Any, Optional, Sequence
import json
import sys

SIZE_OF_ONE_GAME_IN_BYTES = 201729
SIZE_OF_SIMPLEVARS = 0xBC


@dataclass
class CameraMatrix:
    position_x: float
    position_y: float
    position_z: float


@dataclass
class Camera:
    car_zoom_indicator: float
    ped_zoom_indicator: float


@dataclass
class Clock:
    n_milliseconds_per_game_minute: int
    n_last_clock_tick: int
    n_game_clock_hours: int
    n_game_clock_minutes: int


@dataclass
class Pad:
    mode: int


@dataclass
class Timer:
    sn_time_in_milliseconds: int
    f_time_scale: float
    f_time_step: float
    f_time_step_non_clipped: float
    frame_counter: int


@dataclass
class TimeStep:
    f_time_step: float
    f_frames_per_update: float
    f_time_scale: float


@dataclass
class Weather:
    old_weather_type: int
    new_weather_type: int
    forced_weather_type: int
    interpolation_value: int
    weather_type_in_list: Optional[int] = None


@dataclass
class CompileDateTime:
    n_second: int
    n_minute: int
    n_hour: int
    n_day: int
    n_month: int
    n_year: int


@dataclass
class Save:
    size: int
    camera: Optional[Camera] = None
    clock: Optional[Clock] = None
    compile_date_time: Optional[CompileDateTime] = None
    current_level: Optional[int] = None
    matrix: Optional[CameraMatrix] = None
    pad: Optional[Pad] = None
    save_size: Optional[int] = None
    system_time: Optional[datetime] = None
    time_step: Optional[TimeStep] = None
    timer: Optional[Timer] = None
    title: Optional[str] = None
    weather: Optional[Weather] = None


class SaveEncoder(json.JSONEncoder):
    def default(self, obj: Any):
        if isinstance(obj, (float, int, str)):
            return json.JSONEncoder.default(self, obj)
        if isinstance(obj, datetime):
            return obj.strftime('%c')
        return obj.__dict__


def main(filename: str) -> int:
    with open(filename, 'rb') as f:
        save = Save(*unpack('<I', f.read(4)))
        save.title = f.read(48).decode('utf-16').split("'")[1]
        save.system_time = datetime(*unpack('<8H', f.read(16))[:7])
        f.seek(0x40)
        save.save_size = unpack('<Q', f.read(8))[0]
        save.current_level = unpack('<I', f.read(4))[0]
        save.matrix = CameraMatrix(*unpack('<3f', f.read(12)))
        save.clock = Clock(*unpack('<2I2H', f.read(12)))
        save.pad = Pad(*unpack('<H', f.read(2)))
        f.seek(2, 1)
        save.timer = Timer(*unpack('<I3fI', f.read(20)))
        save.time_step = TimeStep(*unpack('<3I', f.read(12)))
        weather_args = []
        for i in range(3):
            weather_args.append(unpack('<H', f.read(2))[0])
            f.seek(2, 1)
        weather_args.append(unpack('<f', f.read(4))[0])
        save.weather = Weather(*weather_args)
        save.compile_date_time = CompileDateTime(*unpack('<6I', f.read(24)))
        save.weather.weather_type_in_list = unpack('<I', f.read(4))[0]
        save.camera = Camera(*unpack('<2I', f.read(8)))
        assert f.tell() == SIZE_OF_SIMPLEVARS

        # TODO
        # Scripts
        # PedPool
        # Garages
        # Vehicles
        # Objects
        # Paths
        # Cranes
        # Pickups
        # Phone info
        # Restart points
        # Radar blips
        # Zones
        # Gang data
        # Car generators
        # Particles
        # AudioScript objects
        # Player info
        # Stats
        # Streaming stuff
        # PedType stuff

        print(json.dumps(save, cls=SaveEncoder, sort_keys=True, indent=2))


def command():
    code = 0
    for name in sys.argv[1:]:
        try:
            main(name)
        except Exception as e:
            print(f'Error processing {name}: {e}', file=sys.stderr)
            code = 1
    return code


if __name__ == '__main__':
    sys.exit(command())
