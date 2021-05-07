from abc import ABC
from abc import abstractmethod


class UseCase(ABC):

    @abstractmethod
    def execute(self):
        pass


class UseCaseMixin:
    usecase = None

    def _run_usecase(self, *args, **kwargs):
        exact_usecase = self.usecase(*args, **kwargs)
        return exact_usecase.execute()
