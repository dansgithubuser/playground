//for logging to separate file (within a source file) when stdout is noisy/broke
const fs = require('fs');
function dlog(msg) { fs.appendFileSync('d.log', `${(new Date()).toISOString()}: ${msg}\n`); }
