"""
ModInfo
=======

The ModInfo combiner gathers all the ModInfoEach parsers into a dictionary
indexed by the module name.

"""

from insights.core.plugins import combiner
from insights.parsers.modinfo import ModInfoEach
from insights.parsers import SkipException


@combiner(ModInfoEach)
class ModInfo(dict):
    """
    Combiner for accessing all the modinfo outputs.

    Examples:
        >>> type(modinfo_obj)
        <class 'insights.combiners.modinfo.ModInfo'>
        >>> type(modinfo_obj['i40e'])
        <class 'insights.parsers.modinfo.ModInfoEach'>
        >>> modinfo_obj['i40e'].module_name
        'i40e'
        >>> modinfo_obj['i40e'].module_name
        'i40e'
        >>> modinfo_obj['i40e']['retpoline']
        'Y'
        >>> modinfo_obj['i40e'].module_version
        '2.3.2-k'
        >>> modinfo_obj['i40e'].module_path
        '/lib/modules/3.10.0-993.el7.x86_64/kernel/drivers/net/ethernet/intel/i40e/i40e.ko.xz'
        >>> "i40e" in modinfo_obj.retpoline_y
        True
        >>> "bnx2x" in modinfo_obj.retpoline_y
        False
        >>> "bnx2x" in modinfo_obj.retpoline_n
        True

    Raises:
        SkipException: When content is empty.

    Attributes:
        retpoline_y (set): A set of names of the modules with the attribute "retpoline: Y".
        retpoline_n (set): A set of names of the modules with the attribute "retpoline: N".
    """
    def __init__(self, modinfo):
        data = {}
        self.retpoline_y = set()
        self.retpoline_n = set()
        for m in modinfo:
            name = m.module_name
            data[name] = m
            if "retpoline" in m:
                r = m["retpoline"]
                if r == "Y":
                    self.retpoline_y.add(name)
                if r == "N":
                    self.retpoline_n.add(name)
        if not data:
            raise SkipException("No parsed contents")
        self.update(data)

    @property
    def data(self):
        """
        (dict): Dict with the module name as the key and the module details as the value.
        """
        return self
