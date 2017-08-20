from abc import ABCMeta, abstractmethod


class ExpBase(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def wait(self):
        pass

    @abstractmethod
    def stop(self):
        pass