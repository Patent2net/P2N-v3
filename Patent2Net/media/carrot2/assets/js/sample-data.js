/*
 * Some sample data for clustering examples.
 */

doIndex = function(progressFn) {
  var i = 0;
  

  function _doIndex() {
    var url = window.ES_URL + "/test/test/" + i;

    if (i < sampleData.length) {
      $.post(url, JSON.stringify(sampleData[i]), function(result) {
        progressFn && progressFn(i, sampleData.length);
        i++;
        _doIndex(progressFn);
      });
    } else {
      $.post(window.ES_URL + "/_flush", function(result) {
        progressFn && progressFn(i, sampleData.length);
      });
    }
  }
  const sampleData = fetch("../DATA/lentille/PatentContents/Carrot2/EN_Abstract_Familieslentille.json")
  .then(response => response.json())
  .then(json => console.log(json));
  // Some sample documents.
  
  _doIndex();
}
