"""
Custom element classes related to the footnotes part
"""


from . import OxmlElement
from .simpletypes import ST_DecimalNumber, ST_String
from ..text.paragraph import Paragraph
from ..text.run import Run
from ..opc.constants import NAMESPACE
from .xmlchemy import (
    BaseOxmlElement, OneAndOnlyOne, RequiredAttribute, ZeroOrMore, ZeroOrOne, OneOrMore
)

# Aqui tenemos las clases de Footnotes, mezcla de br-rkdrnf/python-docx y bayoo-docx
# La base es la de Bayoo, con el método get_by_id de br-rkdrnf
# Se han marcado con ALT TEST las líneas que colisionan con las clases de bayoo-docx

class CT_Footnotes(BaseOxmlElement):
    """
    A ``<w:footnotes>`` element, a container for Footnotes properties 
    """

    footnote = ZeroOrMore ('w:footnote', successors=('w:footnotes',))
    # footnote = ZeroOrMore('w:footnote') # ALT TEST

    @property
    def _next_id(self):
        ids = self.xpath('./w:footnote/@w:id')

        return int(ids[-1]) + 1
    
    def add_footnote(self):
        _next_id = self._next_id
        footnote = CT_Footnote.new(_next_id)
        footnote = self._insert_footnote(footnote)
        return footnote

    def get_footnote_by_id(self, _id):
        namesapce = NAMESPACE().WML_MAIN
        for fn in self.findall('.//w:footnote', {'w':namesapce}):
            if fn._id == _id:
                return fn
        return None
    
    def get_by_id(self, footnoteId):
        """
        Return the ``<w:footnote>`` child element having ``w:id`` attribute
        matching *footnoteId*, or |None| if not found.
        """
        xpath = 'w:footnote[@w:id="%s"]' % footnoteId
        try:
            return self.xpath(xpath)[0]
        except IndexError:
            return None

class CT_Footnote(BaseOxmlElement):
    """
    A ``<w:footnote>`` element, a container for Footnote properties 
    """
    _id = RequiredAttribute('w:id', ST_DecimalNumber)
    p = ZeroOrOne('w:p', successors=('w:footnote',))
    # p = OneOrMore('w:p') # ALT TEST

    @classmethod
    def new(cls, _id):
        footnote = OxmlElement('w:footnote')
        footnote._id = _id
        
        return footnote
    
    def _add_p(self, text):
        _p = OxmlElement('w:p')
        _p.footnote_style()
        
        _r = _p.add_r()
        _r.footnote_style()
        _r = _p.add_r()
        _r.add_footnoteRef()
        
        run = Run(_r, self)
        run.text = text
        
        self._insert_p(_p)
        return _p
    
    @property
    def paragraph(self):
        return Paragraph(self.p, self)
    
class CT_FNR(BaseOxmlElement):
    _id = RequiredAttribute('w:id', ST_DecimalNumber)
    id = RequiredAttribute('w:id', ST_String) # ALT TEST -> dejo los dos para ver si funciona

    @classmethod
    def new (cls, _id):
        footnoteReference = OxmlElement('w:footnoteReference')
        footnoteReference._id = _id
        return footnoteReference

class CT_FootnoteRef (BaseOxmlElement):

    @classmethod
    def new (cls):
        ref = OxmlElement('w:footnoteRef')
        return ref

# Estas clases son para las endnotes y vienen tal cual de https://github.com/br-rkdrnf/python-docx/commit/5562cd4040346f11257ca83e260e9fbd9653ee03

class CT_Endnotes(BaseOxmlElement):
    """
    A ``<w:endnotes>`` element, the root element of a endnotes part, i.e.
    endnotes.xml
    """

    endnote = ZeroOrMore('w:endnote')

    def get_by_id(self, endnoteId):
        """
        Return the ``<w:endnote>`` child element having ``w:id`` attribute
        matching *endnoteId*, or |None| if not found.
        """
        xpath = 'w:endnote[@w:id="%s"]' % endnoteId
        try:
            return self.xpath(xpath)[0]
        except IndexError:
            return None

class CT_Endnote(BaseOxmlElement):
    """
    A ``<w:endnote>`` element, representing a endnote definition
    """

    p = OneOrMore('w:p')


class CT_EndnoteReference(BaseOxmlElement):
    """
    A ``<w:endnoteReference>`` element. provide access to endnote proxy object.
    """

    id = RequiredAttribute('w:id', ST_String)