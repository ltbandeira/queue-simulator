import sys
from .yaml_parser import YamlParser
from .simulator import Simulator


def main(config_path: str = '../config/model.yaml'):
    parser = YamlParser(config_path)
    scheduler, rnd, queues = parser.load()
    sim = Simulator(scheduler, rnd, queues)
    sim.run()


if __name__ == '__main__':
    path = sys.argv[1] if len(sys.argv) > 1 else '../config/model.yaml'
    main(path)