# -*- coding: utf-8 -*-
from burp import IBurpExtender, ITab
from javax.swing import JPanel, JTextArea, JScrollPane, JButton, JLabel, BoxLayout, JTextField, JTabbedPane
from java.awt import FlowLayout, BorderLayout, Dimension, GridLayout, Font, Color
from java.awt.datatransfer import StringSelection
from java.awt import Toolkit
import java.lang.String

class BurpExtender(IBurpExtender, ITab):
    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Punycode Pro Tool")

        # --- User's Complete Homoglyph Map ---
        self._homoglyphs_map = {
            'a': [u'à',u'á',u'â',u'ã',u'ä',u'å',u'ɑ',u'А',u'Α',u'Ꭺ',u'Ａ',u'𝔄',u'𝕬',u'𝒜',u'𝐀',u'𝐴',u'𝘈',u'𝙰',u'𝖠',u'𝗔',u'𝘼',u'𝚨',u'𝑨',u'ⓐ',u'Ⓐ',u'🅐',u'🅰',u'𝔞',u'𝖆',u'𝒶',u'𝗮',u'𝘢',u'а'],
            'b': [u'Ь',u'Ꮟ',u'Ƅ',u'ᖯ',u'𝐛',u'𝑏',u'𝒃',u'𝓫',u'𝔟',u'𝕓',u'𝖇',u'𝗯',u'𝘣',u'𝙗',u'𝚋'],
            'c': [u'ϲ',u'с',u'ƈ',u'ȼ',u'ḉ',u'ⲥ',u'𝐜',u'𝑐',u'𝒄',u'𝓬',u'𝔠',u'𝕔',u'𝖈',u'𝗰',u'𝘤',u'𝙘',u'𝚌'],
            'd': [u'ԁ',u'ժ',u'Ꮷ',u'𝐝',u'𝑑',u'𝒅',u'𝓭',u'𝔡',u'𝕕',u'𝖉',u'𝗱',u'𝘥',u'�',u'𝚍'],
            'e': [u'е',u'ҽ',u'℮',u'ḛ',u'ḝ',u'ẹ',u'é',u'è',u'ê',u'ë',u'ē',u'ė',u'ę',u'𝐞',u'𝑒',u'𝒆',u'𝓮',u'𝔢',u'𝕖',u'𝖊',u'𝗲',u'𝘦',u'𝙚',u'𝚎'],
            'f': [u'ғ',u'𝐟',u'𝑓',u'𝒇',u'𝓯',u'𝔣',u'𝕗',u'𝖋',u'𝗳',u'𝘧',u'𝙛',u'𝚏'],
            'g': [u'ɡ',u'ց',u'𝐠',u'𝑔',u'𝒈',u'𝓰',u'𝔤',u'𝕘',u'𝖌',u'𝗴',u'𝘨',u'𝙜',u'𝚐'],
            'h': [u'һ',u'հ',u'Ꮒ',u'ℎ',u'𝐡',u'𝒉',u'𝒽',u'𝓱',u'𝔥',u'𝕙',u'𝖍',u'𝗵',u'𝘩',u'𝙝',u'𝚑'],
            'i': [u'і',u'ɩ',u'Ꭵ',u'Ⅰ',u'ı',u'í',u'ì',u'î',u'ï',u'ī',u'į',u'𝐢',u'𝑖',u'𝒊',u'𝓲',u'𝔦',u'𝕚',u'𝖎',u'𝗶',u'𝘪',u'𝙞',u'𝚒'],
            'j': [u'ј',u'ʝ',u'ϳ',u'𝐣',u'𝑗',u'𝒋',u'𝓳',u'𝔧',u'𝕛',u'𝖏',u'𝗷',u'𝘫',u'𝙟',u'𝚓'],
            'k': [u'κ',u'𝐤',u'𝑘',u'𝒌',u'𝓴',u'𝔨',u'𝕜',u'𝖐',u'𝗸',u'ｋ',u'𝙠',u'𝚔'],
            'l': [u'ⅼ',u'ӏ',u'Ɩ',u'ʟ',u'𝐥',u'𝑙',u'𝒍',u'𝓵',u'𝔩',u'𝕝',u'𝖑',u'𝗹',u'𝘭',u'𝙡',u'𝚕'],
            'm': [u'м',u'ṃ',u'ᴍ',u'𝐦',u'𝑚',u'𝒎',u'𝓶',u'𝔪',u'𝕞',u'𝖒',u'𝗺',u'𝘮',u'𝙢',u'𝚖'],
            'n': [u'ո',u'п',u'ռ',u'ṅ',u'ṇ',u'ṋ',u'𝐧',u'𝑛',u'𝒏',u'𝓷',u'𝔫',u'𝕟',u'𝖓',u'𝗻',u'𝘯',u'𝙣',u'𝚗'],
            'o': [u'ο',u'օ',u'ӧ',u'ö',u'ó',u'ò',u'ô',u'õ',u'ō',u'ő',u'ⲟ',u'𝐨',u'𝑜',u'𝓸',u'𝔬',u'𝕠',u'𝖔',u'𝗼',u'𝘰',u'𝙤',u'𝚬'],
            'p': [u'р',u'ρ',u'⍴',u'𝐩',u'𝑝',u'𝒑',u'𝓹',u'𝔭',u'𝕡',u'𝖕',u'𝗽',u'𝘱',u'𝙥',u'𝚭'],
            'q': [u'զ',u'ԛ',u'գ',u'𝐪',u'𝑞',u'𝒒',u'𝓺',u'𝔮',u'𝕢',u'𝖖',u'𝗾',u'𝘲',u'𝙦',u'𝚞'],
            'r': [u'ᴦ',u'г',u'ř',u'ȓ',u'ṛ',u'ⲅ',u'𝐫',u'𝑟',u'𝒓',u'𝓻',u'𝔯',u'𝕣',u'𝖗',u'𝗿',u'𝘳',u'𝙧',u'𝚛'],
            's': [u'ѕ',u'ʂ',u'ṡ',u'ṣ',u'𝐬',u'𝑠',u'𝒔',u'𝓼',u'𝔰',u'𝕤',u'𝖘',u'𝘴',u'𝙨',u'𝚜'],
            't': [u'т',u'τ',u'ṭ',u'ț',u'ⲧ',u'𝐭',u'𝑡',u'𝒕',u'𝓽',u'𝔱',u'𝕥',u'𝖙',u'𝘵',u'𝙩',u'𝚝'],
            'u': [u'υ',u'ս',u'ü',u'ú',u'ù',u'û',u'ū',u'ⲩ',u'𝐮',u'𝑢',u'𝒖',u'𝓾',u'𝔲',u'𝕦',u'𝖚',u'𝘶',u'𝙪',u'𝚞'],
            'v': [u'ν',u'ѵ',u'ⴸ',u'𝐯',u'𝑣',u'𝒗',u'𝓿',u'𝔳',u'𝕧',u'𝖛',u'𝗏',u'𝘷',u'𝙫',u'вів'],
            'w': [u'ԝ',u'ա',u'ѡ',u'ⲱ',u'𝐰',u'𝑤',u'𝒘',u'𝔀',u'𝕨',u'𝖜',u'𝗐',u'𝘸',u'𝙬',u'𝚠'],
            'x': [u'х',u'ҳ',u'ӿ',u'𝐱',u'𝑥',u'𝒙',u'𝔁',u'𝕩',u'𝖝',u'𝗑',u'𝘹',u'𝙭',u'𝚡'],
            'y': [u'у',u'ү',u'ӯ',u'ý',u'ÿ',u'ⲩ',u'𝐲',u'𝑦',u'𝒚',u'𝔂',u'𝕪',u'𝖞',u'𝗒',u'𝘺',u'𝙮',u'𝚢'],
            'z': [u'ᴢ',u'ż',u'ź',u'ž',u'𝐳',u'𝑧',u'𝒛',u'𝔃',u'𝕫',u'𝖟',u'𝗓',u'𝘻',u'𝙯',u'𝚣']
        }

        # --- UI Setup ---
        self._panel = JPanel(BorderLayout())
        self._tabs = JTabbedPane()

        # Tab 1: Variant Generator (Based on your Script)
        genTab = JPanel(BorderLayout())
        topRow = JPanel(FlowLayout(FlowLayout.LEFT))
        topRow.add(JLabel("Enter a single letter (a-z): "))
        self._inputField = JTextField(5)
        self._inputField.setFont(Font("SansSerif", Font.BOLD, 18))
        topRow.add(self._inputField)
        
        genBtn = JButton("Generate & Encode", actionPerformed=self.handleGenerate)
        topRow.add(genBtn)
        
        self._resultsArea = JTextArea()
        self._resultsArea.setFont(Font("Monospaced", Font.PLAIN, 14))
        self._resultsArea.setEditable(False)
        
        genTab.add(topRow, BorderLayout.NORTH)
        genTab.add(JScrollPane(self._resultsArea), BorderLayout.CENTER)
        
        # Tab 2: Quick Copy Gallery (All characters from your map)
        galleryTab = JPanel(BorderLayout())
        galleryContainer = JPanel()
        galleryContainer.setLayout(BoxLayout(galleryContainer, BoxLayout.Y_AXIS))
        
        # We sort by key/letter
        sorted_keys = sorted(self._homoglyphs_map.keys())
        for letter in sorted_keys:
            chars = self._homoglyphs_map[letter]
            letterPanel = JPanel(BorderLayout())
            letterPanel.add(JLabel(" Letter: " + letter.upper()), BorderLayout.NORTH)
            
            grid = JPanel(GridLayout(0, 10, 3, 3))
            for char in chars:
                btn = JButton(char)
                btn.setFont(Font("Serif", Font.PLAIN, 18))
                btn.setPreferredSize(Dimension(45, 45))
                btn.addActionListener(lambda e, c=char: self.toClipboard(c))
                grid.add(btn)
            
            letterPanel.add(grid, BorderLayout.CENTER)
            galleryContainer.add(letterPanel)
            
        galleryTab.add(JScrollPane(galleryContainer), BorderLayout.CENTER)

        # Tab 3: Simple Web Symbols
        webTab = JPanel(BorderLayout())
        webSymbols = [u"．", u"∕", u"ː", u"˗", u"＠", u"¿", u"¡", u"¹", u"²", u"³", u"٠", u"¹", u"²", u"³", u"٤", u"Ƽ", u"Ƅ", u"٧", u"٨", u"٩"]
        webGrid = JPanel(GridLayout(0, 10, 5, 5))
        for sym in webSymbols:
            btn = JButton(sym)
            btn.setFont(Font("Serif", Font.PLAIN, 18))
            btn.addActionListener(lambda e, s=sym: self.toClipboard(s))
            webGrid.add(btn)
        webTab.add(webGrid, BorderLayout.NORTH)

        self._tabs.addTab("Generator", genTab)
        self._tabs.addTab("Quick Copy List", galleryTab)
        # self._tabs.addTab("Web Symbols", webTab)

        self._panel.add(self._tabs, BorderLayout.CENTER)
        
        status = JLabel(" [Punycode Pro] Use the list to copy characters directly, or Generate to see Punycode results.")
        self._panel.add(status, BorderLayout.SOUTH)

        callbacks.addSuiteTab(self)
        print("Punycode Pro Tool loaded successfully.")

    def getTabCaption(self):
        return "Punycode Tool"

    def getUiComponent(self):
        return self._panel

    def encode_punycode(self, char):
        try:
            return char.encode('idna').decode('ascii')
        except:
            try:
                return u'xn--' + char.encode('punycode').decode('ascii')
            except:
                return None

    def handleGenerate(self, event):
        letter = self._inputField.getText().strip()
        if len(letter) != 1 or not letter.isalpha():
            self._resultsArea.setText("❗ Please enter a single letter (a-z).")
            return
            
        letter = letter.lower()
        glyphs = self._homoglyphs_map.get(letter, [])
        
        if not glyphs:
            self._resultsArea.setText("❌ No variants found for this letter.")
            return

        header = u"🔎 Encodings for: '{}'\n".format(letter)
        output = u"{:<10} | {:<20}\n".format("Glyph", "Punycode Result")
        output += u"-" * 40 + u"\n"
        
        for glyph in glyphs:
            punycode = self.encode_punycode(glyph)
            if punycode:
                output += u"{:<10} -> {:<20}\n".format(glyph, punycode)
        
        self._resultsArea.setText(header + output)

    def toClipboard(self, text):
        selection = StringSelection(text)
        clipboard = Toolkit.getDefaultToolkit().getSystemClipboard()
        clipboard.setContents(selection, None)
