const electron = require('electron');
const url = require('url');
const path = require('path');

const{app,BrowserWindow} = electron;
let mainWindow;

//listen for app to be ready 
app.on('ready',function(){
    // new window 
    
    const {width, height} = electron.screen.getPrimaryDisplay().workAreaSize
    mainWindow = new BrowserWindow({width, height});
     // load html
    mainWindow.maximize();
    mainWindow.loadURL(url.format({
        pathname: path.join(__dirname,'Run.html'),
        protocol:'file',
        slashes: true 
    }));
    
});

