import mock

# fabric.api
settings = mock.MagicMock(name='settings')
run = mock.MagicMock(name='run')
cd = mock.MagicMock(name='cd')
lcd = mock.MagicMock(name='lcd')
put = mock.MagicMock(name='put')
get = mock.MagicMock(name='get')
local = mock.MagicMock(name='local')
env = mock.MagicMock(name='env')
with_settings = mock.MagicMock(name='with_settings')

# fabric.colors
green = mock.MagicMock(name='green')
blue = mock.MagicMock(name='blue')

# fabric.contrib.files
append = mock.MagicMock(name="append")
