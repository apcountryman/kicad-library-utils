# -*- coding: utf-8 -*-

from rules.rule import *
import re


class Rule(KLCRule):
    """Graphical symbols follow some special rules/KLC-exceptions"""
    fixTooManyPins = False
    fixNoFootprint = False

    def check(self):
        # no need to check this for an alias
        if self.component.extends != None:
            return False


        fail = False
        if self.component.is_graphic_symbol():
            # no pins in graphical symbol
            if (len(self.component.pins) != 0):
                self.error("Graphical symbols have no pins")
                fail = True
                self.fixTooManyPins = True
            # footprint field must be empty
            fp_prop = self.component.get_property("Footprint")
            if fp_prop and fp_prop.value != '':
                self.error("Graphical symbols have no footprint association (footprint was set to '"+fp_prop.value+"')")
                fail = True
                self.fixNoFootprint = True
            # FPFilters must be empty
            if len(self.component.get_fp_filters()) > 0:
                self.error("Graphical symbols have no footprint filters")
                fail = True
                self.fixNoFootprint = True

        return fail

    def fix(self):
        """
        Proceeds the fixing of the rule, if possible.
        """
        if self.fixTooManyPins:
            self.info("FIX for too many pins in graphical symbol")
            self.component.pins = []
        if self.fixNoFootprint:
            self.info("FIX empty footprint association and FPFilters")
            self.component.get_property("Footprint").value = ""
            self.component.get_property("ki_fp_filters").value = ""
