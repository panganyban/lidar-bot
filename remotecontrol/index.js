var keypress = require('keypress');
var net = require('net');
var client = new net.Socket();
var ip = null;

if (process.argv.length <= 2) {
    console.log("No ip specified.\n\n." + process.argv[1] + " 127.0.0.1");
    process.exit(-1)
}
else {
    client.connect(3343, process.argv[2].toString(), function() {
        console.log('client connected');
    });

    client.on('close', function() {
        console.log('connection has closed');
    })

    client.on('error', function() {
        console.log('connection error');
    })

    client.on('timeout', function() {
        console.log('connection has timed out');
    })

    // setup keypress
    keypress(process.stdin);
    process.stdin.on('keypress', function(chunk, key) {
        // console.log('pressed: ', key);
        if(key && key.ctrl && key.name == 'c') {
            client.end();
            process.exit();  // exit
        }
        else if (key && (key.name === 'up' || key.name === 'w')){
            console.log('go forward');
            client.write('GF');
        }
        else if (key && (key.name === 'down' || key.name === 's')) {
            if (key.shift) {
                console.log('reverse');
                client.write('GB');
            }
            else {
                console.log('stop');
                client.write('GS');
            }
        }
        else if (key && (key.name === 'left' || key.name === 'a')) {
            console.log('go left');
            client.write('GL');
        }
        else if (key && (key.name === 'right' || key.name === 'd')) {
            console.log('go right');
            client.write('GR');
        }
        else if (key && (key.name == 'space')) {
            console.log('resume processing');
            client.write('GNULL');
        }
    });

    process.stdin.setRawMode(true);
    process.stdin.resume();
}

