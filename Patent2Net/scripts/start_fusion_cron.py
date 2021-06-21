import time
from Patent2Net.app.fusion import checkFusions


print("START FUSION CRON")

starttime = time.time()
while True:
    print("tick")
    print("[FUSION CRON] check waiting fusions")
    checkFusions()
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))