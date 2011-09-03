
from writer import Writer
from config import Config

config = Config('.config')
writer = Writer(config, '.')

for f in writer.walk():
    writer.write_post(f)
