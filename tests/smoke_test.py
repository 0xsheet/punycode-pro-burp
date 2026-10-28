# -*- coding: utf-8 -*-
import sys
import types
import os
burp = types.ModuleType('burp')
burp.IBurpExtender = type('IBurpExtender', (object,), {})
burp.ITab = type('ITab', (object,), {})
sys.modules['burp'] = burp
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from punycode_tool import BurpExtender
from javax.swing import SwingUtilities
from java.lang import Runnable

class Callbacks(object):
    def getHelpers(self): return None
    def setExtensionName(self, value): self.name = value
    def addSuiteTab(self, value): self.tab = value

class Smoke(Runnable):
    def run(self):
        cb = Callbacks()
        ext = BurpExtender()
        ext.registerExtenderCallbacks(cb)
        assert cb.name == 'Punycode Pro Tool'
        assert cb.tab is ext
        assert ext.getTabCaption() == 'Punycode Tool'
        assert ext._tabs.getTabCount() == 2
        assert len(ext._homoglyphs_map) == 26
        assert sum(len(v) for v in ext._homoglyphs_map.values()) == 421
        assert ext.encode_punycode(u'à') == u'xn--0ca'
        assert ext.encode_punycode(u'а') == u'xn--80a'
        assert ext.encode_punycode(u'Ａ') == u'a'
        assert ext.encode_punycode(u'𝔞') == u'a'
        count = 0
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            ext._inputField.setText(letter)
            ext.handleGenerate(None)
            result = unicode(ext._resultsArea.getText())
            assert 'Punycode Result' in result
            count += sum(1 for line in result.splitlines() if u' -> ' in line)
        assert count == 421, count
        ext._inputField.setText('A')
        ext.handleGenerate(None)
        assert "'a'" in ext._resultsArea.getText()
        for value in ['', 'ab', '1']:
            ext._inputField.setText(value)
            ext.handleGenerate(None)
            assert 'Please enter a single letter' in ext._resultsArea.getText()
        ext._inputField.setText(u'é')
        ext.handleGenerate(None)
        assert 'No variants found' in ext._resultsArea.getText()
        print('PASS: UI registration, 26 groups / 421 generated rows, encoding examples, uppercase input, invalid input, unsupported alphabetic input')
SwingUtilities.invokeAndWait(Smoke())
