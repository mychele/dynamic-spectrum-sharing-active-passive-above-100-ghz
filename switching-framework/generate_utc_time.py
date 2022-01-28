# Copyright 2021, Michele Polese <michele.polese@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation;
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


# This script outputs a 10 UTC timestamps spaced by 60 s

import time
from datetime import datetime


def main():
    time_now = time.time()

    print("[%d, %d, %d, %d, %d]" %
    	(time_now + 120, time_now + 180, time_now + 240, time_now + 300, time_now + 360))
    print("[%d, %d, %d, %d, %d]" %
    	(time_now + 150, time_now + 210, time_now + 270, time_now + 330, time_now + 390))


if __name__ == '__main__':
    main()
