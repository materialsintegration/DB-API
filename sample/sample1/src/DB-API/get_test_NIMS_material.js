// ----------------------------
// import library
// ----------------------------
const express  = require('express');
const app      = express();
const router   = express.Router();
const url      = require('url');
const json2csv = require('json2csv');
const boom     = require('@hapi/boom');
const log4js   = require('log4js');

//const logErrors    = require('../../../error').logErrors;
const errorHandler = require('../../../error');

// ----------------------------
// local variable
// ----------------------------
//const node_root_path = '../../../../..';
const mid_db_path = process.cwd() + '/db';
const dblist = require(mid_db_path + '/dic_dblist.js');

const db = 'NIMS_material';

const mimetypes = ['json', 'csv'];
//const tests = ['tensile test', 'fatigue test', 'creep rupture test'];
const tests = {
    creep_rupture_test: {
        view: 'view_creep_test',
        sql: 'sql_view_test.js',
        key: 'test_piece_id'
    },
    tensile_test: {
        view: 'view_tensile_test',
        sql: 'sql_view_test.js',
        key: 'test_piece_id'
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
    var query = url_parse.query;

    // check query param
    if ('mimetype' in query == false) {
        query['mimetype'] = 'csv';
    }
    if ('test' in query == false) {
        query['test'] = '';
    }

    // validation
    var msg = '';
    if (mimetypes.indexOf(query['mimetype']) == -1) {
        msg = 'invalid mimetype';
        return next(boom.badRequest(msg));
    }
    if (query['test'] in tests == false) {
        msg = 'invalid test';
        return next(boom.badRequest(msg));
    }

    // import sql
    var sql_import = require('./' + tests[query['test']].sql);
    var sql = sql_import.replace('__view__', tests[query['test']].view);

    // get connection
    var dbobj = null;
    dblist.forEach(function( d ) {
        if (db != d.name) return

        switch (d.dbtype) {
            case 'mysql':
                var Mysql = require(mid_db_path + '/' + d.middle)
                dbobj = new Mysql(d.name)

                break
            case 'postgresql':
                var Postgresql = require(mid_db_path + '/' + d.middle)
                dbobj = new Postgresql(d.name)

                break
            default:
                console.log('no database type match')
                return

                break
        }
    }); 
    
    // execute sql
    if (sql != '') {
        try {
            dbobj.getRecordset(sql, function(flds, result, next) {
                // output
                var output = '';
                if (query['mimetype'] == 'json') {
                    output = result;
                    res.setHeader('Content-Type', 'application/json');
                } else if (query['mimetype'] == 'csv') {
                    output = json2csv.parse(result, flds);
                    res.setHeader('Content-Type', 'text/csv; charset=UTF-8');
                }

                res.send(output);
            })

        } catch (error) {
            return next(error);
        }
    } else {
        res.send('');
    }
});

// errorHandler
//router.use(logErrors);
router.use(errorHandler);

module.exports = router;

