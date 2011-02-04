"""
Defines existing HTML elements (including some jank deprecated ones!), along
with a series of base classes for supporting common HTML attributes and
operations.
"""

from core import :x:base, :x:primitive
from xhpy.utils import get_probably_unique_id, htmlspecialchars

class :xhpy:html-element(:x:primitive):
  attribute
    # HTML attributes
    string accesskey, string class, string dir, string id, string lang,
    string style, string tabindex, string title,

    # Javascript events
    string onabort, string onblur, string onchange, string onclick,
    string ondblclick, string onerror, string onfocus, string onkeydown,
    string onkeypress, string onkeyup, string onload, string onmousedown,
    string onmousemove, string onmouseout, string onmouseover, string onmouseup,
    string onreset, string onresize, string onselect, string onsubmit,
    string onunload,

    # IE only
    string onmouseenter, string onmouseleave,

    # misc
    string selected, string otherButtonLabel, string otherButtonHref,
    string otherButtonClass, string type, string replaceCaret,
    string replaceChildren

  def requireUniqueId(self):
    id = self.getAttribute('id')
    if not id:
      id = get_probably_unique_id()
      self.setAttribute('id', id)
    return id

  def renderBaseAttrs(self):
    buf = '<' + self.tagName
    attributes = self.getAttributes()
    for key in attributes:
      val = attributes[key]
      if val is not None and val is not False:
        buf += ' ' + htmlspecialchars(key) + '="' +\
                     htmlspecialchars(val, True) + '"'
    return buf

  def addClass(self, klass):
    klass = klass.trim()
    currentClasses = self.getAttribute('class')
    tmp = ' ' + currentClasses + ' '
    has = tmp.find(' ' + klass + ' ')
    if has != -1:
      return self
    tmp = currentClasses + ' ' + klass
    self.setAttribute('class', tmp.trim())
    return self

  def stringify(self):
    buf = self.renderBaseAttrs() + '>'
    for child in self.getChildren():
      buf += :x:base.renderChild(child)
    buf += '</' + self.tagName + '>'
    return buf

class :xhpy:html-singleton(:xhpy:html-element):
  """
  Subclasses of :xhpy:html-singleton may not contain children. When rendered they
  will be in singleton (<img />, <br />) form.
  """
  children empty

  def stringify(self):
    return self.renderBaseAttrs() + ' />'

class :xhpy:pseudo-singleton(:xhpy:html-element):
  """
  Subclasses of :xhpy:pseudo-singleton may contain exactly zero or one
  children. When rendered they will be in full open/close form, no matter how
  many children there are.
  """
  children (pcdata)*

  def escape(self, txt):
    return htmlspecialchars(txt)

  def stringify(self):
    buf = self.renderBaseAttrs() + '>'
    children = self.getChildren()
    if children:
      buf += :x:base.renderChild(children[0])
    return buf + '</' + self.tagName + '>'

# XHP element definitions

class :a(:xhpy:html-element):
  attribute
    string href, string name, string rel, string target
  category %flow, %phrase, %interactive
  # transparent
  # may not contain %interactive
  children (pcdata | %flow)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'a'


class :abbr(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'abbr'


class :acronym(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'acronym'


class :address(:xhpy:html-element):
  category %flow
  # may not contain h1-h6
  children (pcdata | %flow)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'address'


class :area(:xhpy:html-singleton):
  attribute string alt, string coords, string href, bool nohref, string target
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'area'


class :b(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'b'


class :base(:xhpy:html-singleton):
  attribute string href, string target
  # also a member of "metadata", but is not listed here. see comments in :head
  # for more information
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'base'


class :big(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'big'


class :blockquote(:xhpy:html-element):
  attribute string cite
  category %flow
  children (pcdata | %flow)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'blockquote'


class :body(:xhpy:html-element):
  children (pcdata | %flow)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'body'


class :br(:xhpy:html-singleton):
  category %flow, %phrase
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'br'


class :button(:xhpy:html-element):
  attribute
    bool disabled, string name, enum { "submit", "button", "reset" } type, string value
  category %flow, %phrase, %interactive
  # may not contain interactive
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'button'


class :caption(:xhpy:html-element):
  # may not contain table
  children (pcdata | %flow)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'caption'


class :cite(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'cite'


class :code(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'code'


class :col(:xhpy:html-singleton):
  attribute
    enum { "left", "right", "center", "justify", "char" } align, string char,
    int charoff, int span,
    enum { "top", "middle", "bottom", "baseline" } valign, string width
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'col'


class :colgroup(:xhpy:html-element):
  attribute
    enum { "left", "right", "center", "justify", "char" } align, string char,
    int charoff, int span,
    enum { "top", "middle", "bottom", "baseline" } valign, string width
  children (:col)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'colgroup'


class :dd(:xhpy:html-element):
  children (pcdata | %flow)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'dd'


class :del(:xhpy:html-element):
  attribute string cite, string datetime
  category %flow, %phrase
  # transparent
  children (pcdata | %flow)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'del'

class :div(:xhpy:html-element):
  category %flow
  children (pcdata | %flow)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'div'


class :dfn(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'dfn'


class :dl(:xhpy:html-element):
  category %flow
  children (:dt+, :dd+)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'dl'


class :dt(:xhpy:html-element):
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'dt'


class :em(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'em'


class :fieldset(:xhpy:html-element):
  category %flow
  children (:legend?, (pcdata | %flow)*)
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'fieldset'


class :form(:xhpy:html-element):
  attribute
    string action, string accept, string accept-charset, string enctype,
    enum { "get", "post" } method, string name, string target, bool ajaxify
  category %flow
  # may not contain form
  children (pcdata | %flow)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'form'


class :frame(:xhpy:html-singleton):
  attribute
    bool frameborder, string longdesc, int marginheight, int marginwidth,
    string name, bool noresize, enum { "yes", "no", "auto" } scrolling,
    string src
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'frame'


class :frameset(:xhpy:html-element):
  children (:frame | :frameset | :noframes)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'frameset'


class :h1(:xhpy:html-element):
  category %flow
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'h1'


class :h2(:xhpy:html-element):
  category %flow
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'h2'


class :h3(:xhpy:html-element):
  category %flow
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'h3'


class :h4(:xhpy:html-element):
  category %flow
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'h4'


class :h5(:xhpy:html-element):
  category %flow
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'h5'


class :h6(:xhpy:html-element):
  category %flow
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'h6'


class :head(:xhpy:html-element):
  attribute string profile
  children (%metadata*, :title, %metadata*, :base?, %metadata*)
  # Note: html/xhtml spec says that there should be exactly 1 <title />, and at
  # most 1 <base />. These elements can occur in any order, and can be
  # surrounded by any number of other elements (in %metadata). The problem
  # here is that XHP's validation does not backtrack, so there's no way to
  # accurately implement the spec. This is the closest we can get. The only
  # difference between this and the spec is that in XHP the <title /> must
  # appear before the <base />.
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'head'


class :hr(:xhpy:html-singleton):
  category %flow
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'hr'


class :html(:xhpy:html-element):
  attribute string xmlns
  children (:head, :body)
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'html'


class :i(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'i'


class :iframe(:xhpy:pseudo-singleton):
  attribute
    enum {"1", "0"} frameborder,
    string height, string longdesc, int marginheight,
    int marginwidth, string name, enum { "yes", "no", "auto" } scrolling,
    string src, string width
  category %flow, %phrase, %interactive
  children empty
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'iframe'


class :img(:xhpy:html-singleton):
  attribute
    # Lite
    string staticsrc,
    # HTML
    string alt, string src, string height, bool ismap, string longdesc,
    string usemap, string width
  category %flow, %phrase
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'img'


class :input(:xhpy:html-singleton):
  attribute
    # Non-standard
    enum { "on", "off" } autocomplete,
    string placeholder,
    # HTML
    string accept, enum { "left", "right", "top", "middle", "bottom" } align,
    string alt, bool checked, bool disabled, int maxlength, string name,
    bool readonly, int size, string src,
    enum {
      "button", "checkbox", "file", "hidden", "image", "password", "radio",
      "reset", "submit", "text"
    } type,
    string value
  category %flow, %phrase, %interactive
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'input'


class :ins(:xhpy:html-element):
  attribute string cite, string datetime
  category %flow, %phrase
  # transparent
  children (pcdata | %flow)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'ins'


class :kbd(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'kbd'


class :label(:xhpy:html-element):
  attribute string for
  category %flow, %phrase, %interactive
  # may not contain label
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'label'


class :legend(:xhpy:html-element):
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'legend'


class :li(:xhpy:html-element):
  children (pcdata | %flow)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'li'


class :link(:xhpy:html-singleton):
  attribute
    string charset, string href, string hreflang, string media, string rel,
    string rev, string target, string type
  category %metadata
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'link'


class :map(:xhpy:html-element):
  attribute string name
  category %flow, %phrase
  # transparent
  children ((pcdata | %flow)+ | :area+)
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'map'


class :meta(:xhpy:html-singleton):
  attribute
    string content @required,
    enum {
      "content-type", "content-style-type", "expires", "refresh", "set-cookie"
    } http-equiv,
    string http-equiv, string name, string scheme
  category %metadata
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'meta'


class :noframes(:xhpy:html-element):
  children (%html-body)
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'noframes'


class :noscript(:xhpy:html-element):
  # transparent
  category %flow, %phrase
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'noscript'


class :object(:xhpy:html-element):
  attribute
    enum { "left", "right", "top", "bottom" } align, string archive, int border,
    string classid, string codebase, string codetype, string data, bool declare,
    int height, int hspace, string name, string standby, string type,
    string usemap, int vspace, int width
  category %flow, %phrase
  # transparent, after the params
  children (:param*, (pcdata | %flow)*)
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'object'


class :ol(:xhpy:html-element):
  category %flow
  children (:li)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'ol'


class :optgroup(:xhpy:html-element):
  attribute string label, bool disabled
  children (:option)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'optgroup'


class :option(:xhpy:pseudo-singleton):
  attribute bool disabled, string label, bool selected, string value
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'option'


class :p(:xhpy:html-element):
  category %flow
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'p'


class :param(:xhpy:pseudo-singleton):
  attribute
    string name, string type, string value,
    enum { "data", "ref", "object" } valuetype
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'param'


class :pre(:xhpy:html-element):
  category %flow
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'pre'


class :q(:xhpy:html-element):
  attribute string cite
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'q'


# deprecated
class :s(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 's'


class :samp(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'samp'


class :script(:xhpy:pseudo-singleton):
  attribute string charset, bool defer, string src, string type
  category %flow, %phrase, %metadata
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'script'


class :select(:xhpy:html-element):
  attribute bool disabled, bool multiple, string name, int size
  category %flow, %phrase, %interactive
  children (:option | :optgroup)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'select'


class :small(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'small'


class :span(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'span'


class :strong(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'strong'


class :style(:xhpy:pseudo-singleton):
  attribute
    enum {
      "screen", "tty", "tv", "projection", "handheld", "print", "braille",
      "aural", "all"
    } media, string type
  category %metadata
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'style'


class :sub(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'sub'


class :sup(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'sup'


class :table(:xhpy:html-element):
  attribute
    int border, int cellpadding, int cellspacing,
    enum {
      "void", "above", "below", "hsides", "lhs", "rhs", "vsides", "box",
      "border"
    } frame,
    enum { "none", "groups", "rows", "cols", "all" } rules,
    string summary, string width
  category %flow
  children (
    :caption?, :colgroup*,
    :thead?,
    (
      (:tfoot, (:tbody+ | :tr*)) |
      ((:tbody+ | :tr*), :tfoot?)
    )
  )
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'table'


class :tbody(:xhpy:html-element):
  attribute
    enum { "right", "left", "center", "justify", "char" } align, string char,
    int charoff, enum { "top", "middle", "bottom", "baseline" } valign
  children (:tr)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'tbody'



class :td(:xhpy:html-element):
  attribute
    string abbr, enum { "left", "right", "center", "justify", "char" } align,
    string axis, string char, int charoff, int colspan, string headers,
    int rowspan, enum { "col", "colgroup", "row", "rowgroup" } scope,
    enum { "top", "middle", "bottom", "baseline" } valign
  children (pcdata | %flow)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'td'


class :textarea(:xhpy:pseudo-singleton):
  attribute int cols, int rows, bool disabled, string name, bool readonly
  category %flow, %phrase, %interactive
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'textarea'


class :tfoot(:xhpy:html-element):
  attribute
    enum { "left", "right", "center", "justify", "char" } align, string char,
    int charoff, enum { "top", "middle", "bottom", "baseline" } valign
  children (:tr)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'tfoot'


class :th(:xhpy:html-element):
  attribute
    string abbr, enum { "left", "right", "center", "justify", "char" } align,
    string axis, string char, int charoff, int colspan, int rowspan,
    enum { "col", "colgroup", "row", "rowgroup" } scope,
    enum { "top", "middle", "bottom", "baseline" } valign
  children (pcdata | %flow)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'th'


class :thead(:xhpy:html-element):
  attribute
    enum { "left", "right", "center", "justify", "char" } align, string char,
    int charoff, enum { "top", "middle", "bottom", "baseline" } valign
  children (:tr)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'thead'


class :title(:xhpy:pseudo-singleton):
  # also a member of "metadata", but is not listed here. see comments in :head
  # for more information.
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'title'


class :tr(:xhpy:html-element):
  attribute
    enum { "left", "right", "center", "justify", "char" } align, string char,
    int charoff, enum { "top", "middle", "bottom", "baseline" } valign
  children (:th | :td)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'tr'


class :tt(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'tt'


# deprecated
class :u(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'u'


class :ul(:xhpy:html-element):
  category %flow
  children (:li)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'ul'


class :var(:xhpy:html-element):
  category %flow, %phrase
  children (pcdata | %phrase)*
  def __init__(self, attributes={}, children=[]):
    super(:xhpy:html-element, self).__init__(attributes, children)
    self.tagName = 'var'


class :x:doctype(:x:primitive):
  """
  Render an <html /> element with a DOCTYPE, great for dumping a page to a
  browser. Choose from a wide variety of flavors like XHTML 1.0 Strict, HTML
  4.01 Transitional, and new and improved HTML 5!
  
  Note: Some flavors may not be available in your area.
  """
  children (:html)

  def stringify(self):
    children = self.getChildren()
    return '<!DOCTYPE html>' + (:x:base.renderChild(children[0]))
