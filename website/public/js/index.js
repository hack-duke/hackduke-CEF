var PythonShell = require('python-shell');
var options = {
  mode: 'text',
  pythonPath: '/Library/Frameworks/Python.framework/Versions/3.6/lib/python3.6',
  pythonOptions: ['-u'],
  scriptPath: '/Users/snggeng/dev/hackduke-CEF/housing',
  args: []
};
// var pyShell = new PythonShell('MultiCrawler.py',options);
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
    colHeaders: ['Address', 'Classification', 'Date Listed', 'Price Per Month', 'Specs'],
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

  // Handsontable.Dom.addEvent(save, 'click', function() {
  //   // run python script
  //   console.log("clicked run")
  //   PythonShell.run('MultiCrawler.py', options,  function (err, results) {
  //   console.log('run script')
  //   if (err) throw err;
  //   console.log('results: %j', results);
  //   });
  // });

  Handsontable.Dom.addEvent(autosave, 'click', function() {
    if (autosave.checked) {
      exampleConsole.innerText = 'Changes will be autosaved';
    }
    else {
      exampleConsole.innerText ='Changes will not be autosaved';
    }
  });

  var updateJSON = function() {
      $.ajax({
            type: 'GET',
             url: 'json/load.json',
             async: false,
             contentType: "application/json",
             dataType: 'json',
             success: function(res) {
               //console.log(res);
               var data = res;
               //console.log(data);
               hot.loadData(data);
               exampleConsole.innerText = 'Data loaded';
            },
             error: function(e) {
                console.log(e.message);
             }
            })
  }

  var runPython = function(){
    console.log("clicked run", options.scriptPath)
    PythonShell.run('MultiCrawler.py', options,  function (err, results) {
    console.log('run script')
    if (err) throw err.stack;
    console.log('results: %j', results);
    });
    // var spawn = require('child_process').spawn,
    // py = spawn('python', ['MultiCrawler.py'])
    //
    // py.stdout.on('data', function(data){
    //   dataString += data.toString();
    // });
    // py.stdout.on('end', function(){
    //   console.log('Sum of numbers=',dataString);
    // });
    // py.stdin.write(JSON.stringify(data));
    // py.stdin.end();
  }

  // Shorthand for $( document ).ready()
  $(document).ready(function() {
      updateJSON();
      $( "#save" ).click(function() {
        runPython();
      });
  });
