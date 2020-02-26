// ----------------------------
// import library
// ----------------------------
const express  = require('express');
const router   = express.Router();
const url      = require('url');
const util     = require('util');
const boom     = require('@hapi/boom');
const log4js   = require('log4js');
const childProcess = require('child_process');
const { PythonShell } = require('python-shell');

//const logErrors    = require('../../../error').logErrors;
const errorHandler = require('../../../error');

// ----------------------------
// local variable
// ----------------------------
// GRANTA script working directry
var granta_dir = process.cwd() + '/db/granta'

// python files
// const cmd = '/home/misystem/.pyenv/shims/python';
const cmd = '/usr/bin/python3.6';
// var script = 'searchGRANTA6.py';
var conf = granta_dir + '/searchGRANTA.conf';
var infile = granta_dir + '/granta_schema.csv';
var fout_dir = granta_dir + '/data';
var fout_base = 'granta_mi_pid';

// csv parse option
var csvParseOptions = {
    separator: ','
};
var jsonContent = {};

const mimetypes = {
    'json': {
        header: 'application/json; charset=UTF-8'
    },
    'csv': {
        header: 'text/csv; charset=UTF-8'
    }
};
const tests = {
    'tensile_test': {
        script: 'searchGRANTA12.py',
        script_arg1: 'granta_schema_a.csv'
    }
};

// ----------------------------
// local function
// ----------------------------

// ----------------------------
// main
// ----------------------------

// log setting
log4js.configure(process.cwd() + '/config/log4js.config.json');
const systemLogger = log4js.getLogger('system');
const httpLogger   = log4js.getLogger('http');
const accessLogger = log4js.getLogger('access');

router.use(require("../../../logger.js"));
router.use(log4js.connectLogger(accessLogger));
router.use((req, res, next) => {
    if (typeof req === 'undefined' || req === null || 
        typeof req.method === 'undefined' || req.method === null ||
        typeof req.header === 'undefined' || req.header === null) {
        next();
        return;
    }
    if (req.method === 'GET') {
        httpLogger.info(req.query);
    } else {
        httpLogger.info(req.body);
    }
    next();
});

// get /dbabi/v[n]/get/:table
router.get('/', function(req, res, next) {
    var url_parse = url.parse(req.url, true);
    var query = req.query;

    // check query param
    var mimetype = 'json';
    if (query['mimetype']) {
        mimetype = req.query.mimetype;
    };
    var test = '';
    if (query['test']) {
        test = req.query.test;
    };

    // validation
    var msg = '';
    if (mimetype in mimetypes) {
        msg = '';
    } else {
        msg = 'invalid "mimetypes"';
        return next(boom.badRequest(msg));
    };
    if (test in tests) {
        msg = '';
    } else {
        msg = 'invalid "test"';
        return next(boom.badRequest(msg));
    };

    // parameter set
    var script = tests[test]['script']; 
    infile = granta_dir + '/' + tests[test]['script_arg1'];
    // python-shell options
    var pyoptions = {
        cwd: granta_dir,
        mode: 'text',
        pythonPath: cmd,
        pythonOptions: ['-u'],
        scriptPath: granta_dir + '/',
        args: [conf, infile, mimetype]
    };
    res.setHeader('Content-Type', mimetypes[mimetype]['header']);

    // python shell
    var pyshell = new PythonShell(script, pyoptions);
    var lines = '';
    var fout = fout_dir+'/'+fout_base.replace('pid',pyshell.childProcess.pid)
                           + '.' + mimetype;

    // send unique filename
    //pyshell.send(fout);
    pyshell.on('message', function(message) {
        if (message.match(/^\(python\)/)) {
            console.log(message);
        } else {
            res.write(message + '\n');
        }
    });
    pyshell.on('stderr', function(stderr) {
        console.log('err:' + stderr);
    });
    pyshell.end(function (err, code, signal) {
        if (err) throw err;
        console.log('end code:' + code);
        console.log('end signal:' + signal);

        res.send();
    });
});

// errorHandler
//router.use(logErrors);
router.use(errorHandler);

module.exports = router;
