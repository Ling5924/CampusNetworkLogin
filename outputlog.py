import inspect
import platform
import re
from datetime import datetime


def outputlog(log_path, text, level="info"):
    save_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    with open(log_path, "a", encoding="utf8") as f:
        if platform.system().lower() == 'windows':
            py_name = re.split(r"\\", str(inspect.stack()[1][1]))
        else:
            py_name = re.split("/", str(inspect.stack()[1][1]))
        py_name = py_name[-1]
        line = inspect.stack()[1][2]
        text = f"{py_name}({line}):{text}"
        msg = f"[{save_time} - {level.upper()}] : {str(text)}\n"
        print(msg)
        f.writelines(msg)
