// var handsontable = require('handsontable');
// var data = function () {
//   return Handsontable.helper.createSpreadsheetData(100, 10);
// };
//
// var container = document.getElementById('example');
//
// var hot = new Handsontable(container, {
//   data: data(),
//   minSpareCols: 1,
//   minSpareRows: 1,
//   rowHeaders: true,
//   colHeaders: true,
//   contextMenu: true,
//   readOnly: true
// });

var $$ = function(id) {
      return document.getElementById(id);
    },
    container = $$('example'),
    exampleConsole = $$('example1console'),
    autosave = $$('autosave'),
    load = $$('load'),
    save = $$('save'),
    autosaveNotification,
    hot;

  hot = new Handsontable(container, {
    startRows: 700,
    startCols: 6,
    dataSchema: {address: null, classification: null, dateListed: null, pricePerMonth: null, specs: null},
    rowHeaders: true,
    colHeaders: ['address', 'classification', 'dateListed', 'pricePerMonth', 'specs'],
    columns: [
      {data: 'address'},
      {data: 'classification'},
      {data: 'dateListed'},
      {data: 'pricePerMonth'},
      {data: 'specs'}
    ],
    manualColumnResize: true,
    manualRowResize: true,
    afterChange: function (change, source) {
      if (source === 'loadData') {
        return; //don't save this change
      }
      if (!autosave.checked) {
        return;
      }
      clearTimeout(autosaveNotification);
      $.ajax('json/save.json', 'GET', JSON.stringify({data: change}), function (data) {
        exampleConsole.innerText  = 'Autosaved (' + change.length + ' ' + 'cell' + (change.length > 1 ? 's' : '') + ')';
        autosaveNotification = setTimeout(function() {
          exampleConsole.innerText ='Changes will be autosaved';
        }, 1000);
      });
    }
  });

  Handsontable.Dom.addEvent(load, 'click', function() {
    console.log("clicked load")
    // $.ajax('json/load.json', 'GET', '', function(res, err) {
    //   console.log("ajax start")
    //   var data = JSON.parse(res.response);
    //   console.log("1", data)
    //   console.log("2", data.data)
    //   hot.loadData(data);
    //   exampleConsole.innerText = 'Data loaded';
    // });
    $.ajax({
          type: 'GET',
           url: 'json/load.json',
           async: false,
           contentType: "application/json",
           dataType: 'json',
           success: function(res) {
             console.log(res);
             var data = res;
             console.log(data);
             hot.loadData(data);
             exampleConsole.innerText = 'Data loaded';
          },
           error: function(e) {
              console.log(e.message);
              // console.log(JSON.parse(e.responseText)[0]['address'])
              // var data = JSON.parse(e.responseText)[0]
              //console.log(data)
              // hot.loadData(data);
              // exampleConsole.innerText = 'Data loaded';
           }
          })
  });

  Handsontable.Dom.addEvent(save, 'click', function() {
    // save all cell's data
    console.log("clicked save")
    $.ajax('json/save.json', 'GET', JSON.stringify({data: hot.getData()}), function (res) {
      var response = JSON.parse(res.response);

      if (response.result === 'ok') {
        exampleConsole.innerText = 'Data saved';
      }
      else {
        exampleConsole.innerText = 'Save error';
      }
    });
  });

  Handsontable.Dom.addEvent(autosave, 'click', function() {
    if (autosave.checked) {
      exampleConsole.innerText = 'Changes will be autosaved';
    }
    else {
      exampleConsole.innerText ='Changes will not be autosaved';
    }
  });
