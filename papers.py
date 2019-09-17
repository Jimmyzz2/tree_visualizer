import csv
from typing import List, Dict
from tm_trees import TMTree

# Filename for the dataset
DATA_FILE = 'cs1_papers.csv'


class PaperTree(TMTree):
    """A tree representation of Computer Science Education research paper data.

    === Private Attributes ===
    _authors:
        The authors of this paper, or '' if it is a category
    _doi:
        The web link of this paper, or '' if it is a category
    These should store information about this paper's <authors> and <doi>.

    === Inherited Attributes ===
    rect:
        The pygame rectangle representing this node in the treemap
        visualization.
    data_size:
        The size of the data represented by this tree.
    _colour:
        The RGB colour value of the root of this tree.
    _name:
        The root value of this tree, or None if this tree is empty.
    _subtrees:
        The subtrees of this tree.
    _parent_tree:
        The parent tree of this tree; i.e., the tree that contains this tree
        as a subtree, or None if this tree is not part of a larger tree.
    _expanded:
        Whether or not this tree is considered expanded for visualization.

    === Representation Invariants ===
    - All TMTree RIs are inherited.
    """

    _authors: str
    _doi: str

    def __init__(self, name: str, subtrees: List[TMTree], authors: str = '',
                 doi: str = '', citations: int = 0, by_year: bool = True,
                 all_papers: bool = False) -> None:
        """Initialize a new PaperTree with the given <name> and <subtrees>,
        <authors> and <doi>, and with <citations> as the size of the data.

        If <all_papers> is True, then this tree is to be the root of the paper
        tree. In that case, load data about papers from DATA_FILE to build the
        tree.

        If <all_papers> is False, Do NOT load new data.

        <by_year> indicates whether or not the first level of subtrees should be
        the years, followed by each category, subcategory, and so on. If
        <by_year> is False, then the year in the dataset is simply ignored.
        """
        # case root of the paper tree, only the 0 depth
        if all_papers:
            dic = _load_papers_to_dict(by_year)
            size = 0
            lst = _build_tree_from_dict(dic)
            TMTree.__init__(self, name, lst, size)
            self._authors = authors
            self._doi = doi
        # case not root
        elif not all_papers:
            TMTree.__init__(self, name, subtrees, citations)
            self._authors = authors
            self._doi = doi

    def get_separator(self) -> str:
        """Return the string used to separate names in the string
        representation of a path from the tree root to this tree.
        """
        return '/'

    def get_suffix(self) -> str:
        """Return the string used at the end of the string representation of
        a path from the tree root to this tree.
        """
        if len(self._subtrees) == 0:
            return ' (paper)'
        else:
            return ' (category)'


def _load_papers_to_dict(by_year: bool = True) -> Dict:
    """Return a nested dictionary of the data read from the papers dataset file.

    If <by_year>, then use years as the roots of the subtrees of the root of
    the whole tree. Otherwise, ignore years and use categories only.
    """
    dic = {}
    file = open(DATA_FILE, 'r')
    read = csv.reader(file)
    next(read)
    # case by_year
    if by_year:
        for line in read:
            # create a list to feed the dictionary
            lst = []
            # extend year
            lst.extend([line[2]])
            lst.extend(line[3].split(':'))
            # the last item is tuple of the form paper_name, author
            # doi, citations
            tup = (line[1], line[0], line[-2], int(line[-1]))
            lst.extend([tup])
            _add_lst_to_dic(lst, dic)
    # case not by_year
    else:
        for line in read:
            # create a list to feed the dictionary
            lst = []
            lst.extend(line[3].split(':'))
            # the last item is tuple of the form paper_name, author
            # doi, citations
            tup = (line[1], line[0], line[-2], int(line[-1]))
            lst.extend([tup])
            _add_lst_to_dic(lst, dic)
    file.close()
    return dic


def _add_lst_to_dic(lst: list, dic: dict) -> None:
    """
    Add a list in the order of category: subcategory: subsubcategory...
    to a dictionary. If the category already exists, then do nothing
    and continue on subcategory.

    If tuple in the list, do not split the tuple into category
    >>> lst = [1, 2, 3, 4]
    >>> dic = {}
    >>> _add_lst_to_dic(lst, dic)
    >>> dic
    {1: {2: {3: {4: {}}}}}
    >>> lst = ['a', 'b', 'c', 'd']
    >>> _add_lst_to_dic(lst, dic)
    >>> dic
    {1: {2: {3: {4: {}}}}, 'a': {'b': {'c': {'d': {}}}}}
    >>> lst = [1, 2, 3, 'g']
    >>> _add_lst_to_dic(lst, dic)
    >>> dic
    {1: {2: {3: {4: {}, 'g': {}}}}, 'a': {'b': {'c': {'d': {}}}}}
    >>> lst = ['m', 'n', 'g', 'q']
    >>> _add_lst_to_dic(lst, dic)
    >>> dic['m']
    {'n': {'g': {'q': {}}}}
    >>> lst = ['m', 'n', 'g', 'q', (1, 2, 3, 4)]
    >>> _add_lst_to_dic(lst, dic)
    >>> dic['m']['n']['g']['q'][1]
    (2, 3, 4)
    """
    if lst == []:
        pass
    elif isinstance(lst[0], tuple):
        name, author, doi, cite = lst[0]
        dic[name] = author, doi, cite
    elif lst[0] not in dic:
        dic[lst[0]] = {}
        slic = lst[1:]
        _add_lst_to_dic(slic, dic[lst[0]])
    else:
        slic = lst[1:]
        _add_lst_to_dic(slic, dic[lst[0]])


def _build_tree_from_dict(nested_dict: Dict) -> List[PaperTree]:
    """Return a list of trees from the nested dictionary <nested_dict>.
    """
    lst = []
    for item in nested_dict:
        if isinstance(nested_dict[item], tuple):
            author, doi, citations = nested_dict[item]
            a = PaperTree(item, [], author, doi, citations)
            lst.append(a)
        else:
            k = PaperTree(item, _build_tree_from_dict(nested_dict[item]),
                          '', '')
            lst.append(k)
    return lst


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': ['python_ta', 'typing', 'csv', 'tm_trees'],
        'allowed-io': ['_load_papers_to_dict'],
        'max-args': 8
    })
