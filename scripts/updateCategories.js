DOMAIN = "http://api.flyingclimber.net/";
ARGS = "bodega/";
API_KEY = ''

URL = DOMAIN + ARGS;

function onOpen() {
  var ui = SpreadsheetApp.getUi();
  
  ui.createMenu('ToolBox')
  .addItem('Add a month', 'showPrompt_')
  .addSeparator()
  .addItem('Train', 'train')
  .addItem('Update Single Category', 'updateSingleCategory')
  .addItem('Update All Categories', 'updateAllCategories')
  .addToUi()
}

function train() {
  var ss = SpreadsheetApp.getActiveSheet();
  var range = ss.getRange('B2:D53');
  var values = range.getValues();

  for (var i=0; i < values.length; i++) {
    var row = "";
    if (values[i][0] && values[i][2]) {
      var merchant = values[i][0]
      var category = values[i][2]
            
      var payload = {
        "merchant" : merchant,
        "category" : category,
        "api_key" : API_KEY
      };
      
      var options = {
        "method" : "post",
        "payload" : payload,
      };
      Logger.log(options);
      UrlFetchApp.fetch(URL + 'add', options);

    }
  }
}

function updateSingleCategory() {
  var ss = SpreadsheetApp.getActiveSheet();
  var cell = ss.getActiveCell();
  var range = ss.getRange('D' + cell.getRow());
  var category = range.getCell(1,1);
  
  if (category.getValue() == 'Unknown' || category.getValue() == '') {
    resp = lookupMerchant(cell.getValue());
    category.setValue(resp);
  }
}

function updateAllCategories() {
  var ss = SpreadsheetApp.getActiveSheet();
  var range = ss.getRange('B2:D53');
  var values = range.getValues();

  for (var i=0; i < values.length; i++) {
    var row = "";
    if (values[i][0]) {
      row = row + values[i][0];
    }
    if (row == "") {
      continue;
    } else {
      category = range.getCell(i+1, 3);

      if (category.getValue() == 'Unknown' || category.getValue() == '' ) {
        resp = lookupMerchant(row);
        category.setValue(resp);
      }
    }
  }
}

function lookupMerchant(merchant) {
  var response = UrlFetchApp.fetch(URL + 'get/' + merchant);

  return response.getContentText();
}
