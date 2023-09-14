# This file is executed on every boot (including wake-boot from deepsleep)
import esp
esp.osdebug(None)
import webrepl
webrepl.start()
import net
net.activate()
import ntptime
import time
ntptime.settime()
print("Local time after synchronization：%s" %str(time.localtime()))
net.status()
