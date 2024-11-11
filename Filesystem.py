from abc import ABC, abstractmethod
from typing import List

class FileSystemComponent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def search(self, criteria):
        pass

class File(FileSystemComponent):
    def __init__(self, name: str, size: int):
        super().__init__(name)
        self.size = size

    def search(self, criteria):
        if criteria.match(self):
            return [self]
        return []

class Directory(FileSystemComponent):
    def __init__(self, name: str):
        super().__init__(name)
        self.children: List[FileSystemComponent] = []

    def add(self, component: FileSystemComponent):
        self.children.append(component)

    def search(self, criteria):
        results = []
        if criteria.match(self):
            results.append(self)
        for child in self.children:
            results.extend(child.search(criteria))
        return results
    
from abc import ABC, abstractmethod

class SearchCriteria(ABC):
    @abstractmethod
    def match(self, component: FileSystemComponent) -> bool:
        pass

class NameCriteria(SearchCriteria):
    def __init__(self, name: str):
        self.name = name.lower()

    def match(self, component: FileSystemComponent) -> bool:
        return self.name in component.name.lower()

class SizeCriteria(SearchCriteria):
    def __init__(self, min_size: int, max_size: int):
        self.min_size = min_size
        self.max_size = max_size

    def match(self, component: FileSystemComponent) -> bool:
        return isinstance(component, File) and self.min_size <= component.size <= self.max_size

class AndCriteria(SearchCriteria):
    def __init__(self, criteria1: SearchCriteria, criteria2: SearchCriteria):
        self.criteria1 = criteria1
        self.criteria2 = criteria2

    def match(self, component: FileSystemComponent) -> bool:
        return self.criteria1.match(component) and self.criteria2.match(component)

class OrCriteria(SearchCriteria):
    def __init__(self, criteria1: SearchCriteria, criteria2: SearchCriteria):
        self.criteria1 = criteria1
        self.criteria2 = criteria2

    def match(self, component: FileSystemComponent) -> bool:
        return self.criteria1.match(component) or self.criteria2.match(component)
    

class FileSystemSearch:
    def __init__(self, root: Directory):
        self.root = root

    def search(self, criteria: SearchCriteria) -> List[FileSystemComponent]:
        return self.root.search(criteria)
    

if __name__ == '__main__':
    # Create a file system structure
    root = Directory('/')
    home = Directory('home')
    root.add(home)
    user = Directory('user')
    home.add(user)
    user.add(File('document.txt', 1024))
    user.add(File('image.jpg', 2048))
    root.add(File('system.log', 512))

    # Create search criteria
    name_criteria = NameCriteria('doc')
    size_criteria = SizeCriteria(1000, 3000)
    combined_criteria = AndCriteria(name_criteria, size_criteria)

    # Perform search
    file_system_search = FileSystemSearch(root)
    results = file_system_search.search(combined_criteria)

    # Print results
    print('Search Results:')
    for item in results:
        if isinstance(item, File):
            print(f'File: {item.name} (Size: {item.size} bytes)')
        else:
            print(f'Directory: {item.name}')