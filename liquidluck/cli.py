
from writer import Walker, Writer
from config import Config

config = Config('.config')
writer = Writer(config, '.')


print writer.run()
