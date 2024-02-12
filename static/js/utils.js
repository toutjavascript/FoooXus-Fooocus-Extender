function timer(ms) {
    return new Promise(res => setTimeout(res, ms));
}

function secure(text) {
    if (text) {
        text=text.toString();
        return text.replace("'","&#39;").replace('"', "&#34;").replace(/</g, "&lt;").replace(/>/g, "&gt;");    
    }
    return "";
}

function secureFile(name) {
    if (name) {
        name=name.toString();
        name=name.toLowerCase();
        return name.replace(/\W/gi, "-");
    }
}

function now() {
    if (performance)  return performance.now();
    return new Date().getTime();
}

/* Display number with maximum 3 significant digits */
function significant3(val) {
    if (val < 10) {return val.toFixed(2);}
    if (val < 100) { return val.toFixed(1); }
    return val.toFixed(0);
}


function formatBytes(B, toFixed=2) {
    if (toFixed==0) {    
        if (B < 1024) {
            return B + " B";
        }
        else if (B < 1024 * 1024) {
            return (B / 1024).toFixed(toFixed) + " KB";
        }
        else if (B < 1024 * 1024 * 1024) {
            return (B / (1024 * 1024)).toFixed(toFixed) + " MB";
        }
        else if (B < 1024 * 1024 * 1024 * 1024) {
            return (B / (1024 * 1024 * 1024)).toFixed(toFixed) + " GB";
        } else { 
            return (B / (1024 * 1024 * 1024 * 1024)).toFixed(toFixed) + " TB";
        }
    } else {
        if (B < 1024) {
            return B + " B";
        }
        else if (B < 1024 * 1024) {
            return significant3(B / 1024) + " KB";
        }
        else if (B < 1024 * 1024 * 1024) {
            return significant3(B / (1024 * 1024)) + " MB";
        }
        else if (B < 1024 * 1024 * 1024 * 1024) {
            return significant3(B / (1024 * 1024 * 1024)) + " GB";
        } else { 
            return significant3(B / (1024 * 1024 * 1024 * 1024)) + " TB";
        }        
    }
}

function formatHz(Hz, toFixed=2) {
    if (Hz < 1000) {
        return Hz + " Hz";
    }
    else if (Hz < 1000 * 1000) {
        return (Hz / 1000).toFixed(toFixed) + " KHz";
    }
    else if (Hz < 1000 * 1000 * 1000) {
        return (Hz / (1000 * 1000)).toFixed(toFixed) + " MHz";
    }
    else if (Hz < 1000 * 1000 * 1000 * 1000) {
        return (Hz / (1000 * 1000 * 1000)).toFixed(toFixed) + " GHz";
    } else { 
        return (Hz / (1000 * 1000 * 1000 * 1000)).toFixed(toFixed) + " THz";
    }
}


