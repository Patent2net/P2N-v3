.. image:: https://img.shields.io/badge/Python-3.6-green.svg
    :target: https://github.com/Patent2net/P2N-v3/tree/master

|

:: 
     _____      _             _     ___    _   _      _           ____   ___    _   _
    |  __ \    | |           | |   |__ \  | \ | |    | |      /  |  __ \ |__ \  | \ | | \
    | |__) |_ _| |_ ___ _ __ | |_     ) | |  \| | ___| |_    /   | |__) |   ) | |  \| |  \
    |  ___/ _` | __/ _ \ '_ \| __|   / /  | . ` |/ _ \ __|   |   |  ___/   / /  | . ` |   |
    | |  | (_| | ||  __/ | | | |_   / /_  | |\  |  __/ |_     \  | |      / /_  | |\  |  /
    |_|   \__,_|\__\___|_| |_|\__| |____| |_| \_|\___|\__|     \ |_|     |____| |_| \_| /


=====
About
=====
:: 
Patent2Net is a tool suite for patent information processing and statistical analysis for education and science.  
  Patent2Net aims to collect and help study and analyze patent data from the European Patent Office's `Open Patent Services API (OPS) <https://www.epo.org/searching-for-patents/data/web-services/ops.html>`_.

:: 
Patent2Net is free software, dedicated to:
 * provide statistical analysis and representations of a set of patents.
 * promote the use of patent information in academic, nano and small firms, developing countries
 * learn, study and practice how to collect, treat and communicate "textual bibliographic information", and automation process
 * learn several information processing in the Library and Information Science fields.
 * learn skills in data-mining software, Data analysis, Textual data-mining, distance reading, knowledge discovery
 * See extra-feature with `the docker version <https://github.com/Patent2net/P2N-Docker>`_

.. note:: Contributions are always welcome!

==============================
P2N essential features covered
==============================
---------------------------------------------
In short (read the usage manual in progress)
---------------------------------------------

* Patent2Net interface you to the `European Patent Organisation <https://www.epo.org/>`_ worldwide database to gather patent documents set in answer to your requests 
* Patent2Net interfaces also several softwares to build indicators and help analyse: `Datatable <https://datatables.net/>`_, `Pivot table <https://pivottable.js.org/examples/>`_
* Patent2Net provides compatible files with two major open source projects in text analysis `IRaMuTeQ <http://iramuteq.org/>`_ and document clustering `Carrot2 <https://github.com/carrot2/carrot2>`_. But these programs have to be installed by your way. P2N provide data in compatible format for the different distributions.

.. TIP:: the docker version includes now a beta version of the Carrot2 software plugin using the Elastic Search server!

* Patent2Net build as well network files from patent Metadata. Assuming some trivial hypothesis that co-authors of a patent works together... Same for co-applicants: so networks analyses aims to help in exploring who works for who, who works with who... And so on. Same with the  `International Patent Classification <https://www.wipo.int/classifications/ipc/en/>`_ metadata field that provides language independent views on patent sets. This P2N version integrate inline interface to those networks (see the link in page data synthesis) but the interface with network is not friendly enought. We recommend the use of the exported files in gexf format compatible with the wondefull Open Graph Viz Platform `Gephi <https://gephi.org/>`_ that you may install on your machine.
* Patent2Net, aside HTML5, exports also in several format: CSV, Excel, BibTex for `Zotero <https://www.zotero.org/>`_ import.

---------------------------------------------
Undocumented features
---------------------------------------------

Some extra additional features comes also within the makefile... Help us to improve the docs and the projects

==============================================
Project information: Who we are
==============================================
The source code of the »Patent2Net« toolkit is available under an open source license,
see also  ` Patent2Net on GitHub <https://github.com/Patent2net/P2N-v3/tree/master>`_
 
The project is elaborated and maintained by an `international team <http://patent2netv2.vlab4u.info/dokuwiki/doku.php?id=about_p2n:community>`_
of university professors and researchers on a free basis.

=======
License
=======
Aside integrated open-source sofware that leads their own licence, the Patent2Net code is covered by the `CECILL-B licence <https://cecill.info/licences/Licence_CeCILL-B_V1-en.html>`_. 

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


=============
Documentation
=============
************
Doc and wiki
************

.. _Patent2Net-Documentation:
 * `Wiki <http://patent2netv2.vlab4u.info/dokuwiki/>`_
 * `Documentation <https://docs.ip-tools.org/patent2net/>`_


****
Demo
****
Some results of patent analysis can be explored on http://patent2netv2.vlab4u.info/. See for instance some use case processed:

* `Creativity <http://patent2netv2.vlab4u.info/DATA/creativity.html>`_
 
* `3D-printing <http://patent2netv2.vlab4u.info/DATA/3Dprint.html>`_

* `Arabic-gum-emulsifiers <http://patent2netv2.vlab4u.info/DATA/Arabic_Gum.html>`_


