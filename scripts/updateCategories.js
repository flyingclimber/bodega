DOMAIN = "";
ARGS = "get/";
URL = DOMAIN + ARGS;

function onOpen() {
  var ui = SpreadsheetApp.getUi();
  ui.createMenu('AutoCharacterize')
      .addItem('updateSingleCategory', 'updateSingleCategory')
      .addItem('updateAllCategories', 'updateAllCategories')
      .addToUi();
}

function updateSingleCategory() {
  var sheet = SpreadsheetApp.getActive().getActiveSheet();
  var cell = sheet.getActiveCell();

  var range = sheet.getRange('D' + cell.getRow());
  var category = range.getCell(1,1);

  if (category.getValue() == 'Unknown') {
    resp = lookupMerchant(cell.getValue());
    category.setValue(resp);
  }
}

function updateAllCategories() {
  var sheet = SpreadsheetApp.getActive().getActiveSheet();
  var range = sheet.getRange('B2:D200');
  var values = range.getValues();

  for (var i=0; i < values.length; i++) { //
    var row = "";
    if (values[i][0]) {
      row = row + values[i][0];
    }
    if (row == "") {
      continue;
    } else {
      category = range.getCell(i+1, 3);

      if (category.getValue() == 'Unknown') {
        resp = lookupMerchant(row);
        category.setValue(resp);
      }
    }
  }
}

function lookupMerchant(merchant) {
  var response = UrlFetchApp.fetch(URL + merchant);

  return response.getContentText();
}
