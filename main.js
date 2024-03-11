const {app, BrowserWindow} = require('electron')

function createWindow () {
    window = new BrowserWindow({width: 800, height: 600})
    window.loadFile('/templates/index.html')


    	var python = require('child_process').spawn('C:/Python312/python.exe', ['./main.py']);
	python.stdout.on('data',function(data){
    		console.log("data: ",data.toString('utf8'));
	});


var pyshell =  require('python-shell');

pyshell.run('main.py',  function  (err, results)  {
 if  (err)  throw err;
 console.log('main.py finished.');
 console.log('results', results);
});   	
    
}



app.on('ready', createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
      app.quit()
    }
})

