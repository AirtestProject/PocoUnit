# PocoUnit (unittest framework)

可配合airtest和poco使用的单元测试框架。规范了脚本编写的格式，提供流式日志（stream log）记录服务，然后可以使用[PocoResultPlayer](http://poco.readthedocs.io/en/latest/source/doc/about-test-result-player.html)将运行的内容回放。

## Installation

```bash
pip install pocounit
```

## 用法

首先需要继承基类PocoTestCase实现项目组自己的GxxTestCase，在GxxTestCase预处理中将需要用到的对象准备好（包括实例化hunter和poco和动作捕捉），以后在其余用例中继承GxxTestCase即可。

基本用法可参考一下代码模板。

```python
# coding=utf-8

from pocounit.case import PocoTestCase
from pocounit.addons.poco.action_tracking import ActionTracker

from poco.drivers.unity3d import UnityPoco


class GxxTestCase(PocoTestCase):
    @classmethod
    def setUpClass(cls):
        super(GxxTestCase, cls).setUpClass()
        cls.poco = UnityPoco(('<ip>', 5001))

        # 启用动作捕捉(action tracker)
        action_tracker = ActionTracker(cls.poco)
        cls.register_addon(action_tracker)
```

然后可以开始编写自己的testcase

```python
# coding=utf8

from ... import GxxTestCase


# 一个文件里建议就只有一个TestCase
# 一个Case做的事情尽量简单，不要把一大串操作都放到一起
class MyTestCase(GxxTestCase):     
    def setUp(self):
        # 可以调用一些前置条件指令和预处理指令
        pass

    # 函数名就是这个，用其他名字无效
    def runTest(self):
        # 普通语句跟原来一样
        self.poco(text='角色').click()
        
        # 断言语句跟python unittest写法一模一样
        self.assertTrue(self.poco(text='最大生命').wait(3).exists(), "看到了最大生命")

        self.poco('btn_close').click()
        self.poco('movetouch_panel').offspring('point_img').swipe('up')

    def tearDown(self):
        # 如果没有清场操作，这个函数就不用写出来
        pass

    # 不要写以test开头的函数，除非你知道会发生什么
    # def test_xxx():
    #     pass


if __name__ in ('__main__', 'airtest.cli.runner'):
    import pocounit
    pocounit.main() 

```

