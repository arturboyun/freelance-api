#
# class BaseService(ABC):
#     def __init__(self, session: AsyncSession | Any = None):
#         if not session:
#             raise ValueError("session attribute is required")
#         self.session = None
#
#     @abstractmethod
#     def get(self, _id):
#         pass
#
#     @abstractmethod
#     def get_all(self):
#         pass
#
#     @abstractmethod
#     def create(self, data):
#         pass
#
#     @abstractmethod
#     def update(self, _id, data):
#         pass
#
#     @abstractmethod
#     def delete(self, _id):
#         pass
