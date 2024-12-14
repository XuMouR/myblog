from django.apps import AppConfig
from django.utils.module_loading import autodiscover_modules


class StarkConfig(AppConfig):
    name = 'stark'

    # 程序启动时，扫描app下的指定文件stark.py 并执行
    def ready(self):
        print("扫描stark app组件")
        autodiscover_modules('stark')