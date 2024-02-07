/**
* This sorting plug-in for DataTables will correctly sort data in date time or date
* format typically used in Germany:
* date and time:dd.mm.YYYY HH:mm
* just date:dd.mm.YYYY.
*
* @name Date (dd.mm.YYYY) or date and time (dd.mm.YYYY HH:mm)
* @summary Sort date / time in the format dd.mm.YYYY HH:mm or dd.mm.YYYY.
* @author Ronny Vedrilla
*
* @example
* $('#example').dataTable( {
* columnDefs: [
* { type: 'de_datetime', targets: 0 },
* { type: 'de_date', targets: 1 }
* ]
* } );
*/

jQuery.extend(jQuery.fn.dataTableExt.oSort, {
"de_datetime-asc": function (a, b) {
var x, y;
if ($.trim(a) !== '') {
var deDatea = $.trim(a).split(' ');
var deTimea = deDatea[1].split(':');
var deDatea2 = deDatea[0].split('.');
x = (deDatea2[2] + deDatea2[1] + deDatea2[0] + deTimea[0] + deTimea[1]) * 1;
} else {
x = Infinity; // = l'an 1000 ...
}
    if ($.trim(b) !== '') {
        var deDateb = $.trim(b).split(' ');
        var deTimeb = deDateb[1].split(':');
        deDateb = deDateb[0].split('.');
        y = (deDateb[2] + deDateb[1] + deDateb[0] + deTimeb[0] + deTimeb[1]) * 1;
    } else {
        y = Infinity;
    }
    var z = ((x < y) ? -1 : ((x > y) ? 1 : 0));
    return z;
},

"de_datetime-desc": function (a, b) {
    var x, y;
    if ($.trim(a) !== '') {
        var deDatea = $.trim(a).split(' ');
        var deTimea = deDatea[1].split(':');
        var deDatea2 = deDatea[0].split('.');
        x = (deDatea2[2] + deDatea2[1] + deDatea2[0] + deTimea[0] + deTimea[1]) * 1;
    } else {
        x = Infinity;
    }

    if ($.trim(b) !== '') {
        var deDateb = $.trim(b).split(' ');
        var deTimeb = deDateb[1].split(':');
        deDateb = deDateb[0].split('.');
        y = (deDateb[2] + deDateb[1] + deDateb[0] + deTimeb[0] + deTimeb[1]) * 1;
    } else {
        y = Infinity;
    }
    var z = ((x < y) ? 1 : ((x > y) ? -1 : 0));
    return z;
},

"de_date-asc": function (a, b) {
    //debugger;
    var x, y;
    if ($.trim(a) !== '') {
        if (a.indexOf('年') > 0) {
            a = a.replace("年", ".").replace("月", ".").replace("日", ".");
            var deDatea = $.trim(a).split('.');
            if (deDatea[1].length == 1) {
                deDatea[1] = 0 + deDatea[1];
            }
            if (deDatea[2].length == 1) {
                deDatea[2] = 0 + deDatea[2];
            }
            x = (deDatea[0] + deDatea[1] + deDatea[2]) * 1;
        }
        else if (a.indexOf('-') > 0) {
            var deDatea = $.trim(a).split('-');
            if (deDatea[1].length == 1) {
                deDatea[1] = 0 + deDatea[1];
            }
            if (deDatea[2].length == 1) {
                deDatea[2] = 0 + deDatea[2];
            }
            x = (deDatea[2] + deDatea[1] + deDatea[0]) * 1;

        }
        else {
            var deDatea = $.trim(a).split('.');
            x = (deDatea[2] + deDatea[1] + deDatea[0]) * 1;
        }

    } else {
        x = Infinity; // = l'an 1000 ...
    }

    if ($.trim(b) !== '') {
        if (b.indexOf('年') > 0) {
            b = b.replace("年", ".").replace("月", ".").replace("日", ".");
            var deDateb = $.trim(b).split('.');
            if (deDateb[1].length == 1) {
                deDateb[1] = 0 + deDateb[1];
            }
            if (deDateb[2].length == 1) {
                deDateb[2] = 0 + deDateb[2];
            }
            y = (deDateb[0] + deDateb[1] + deDateb[2]) * 1;
        }
        else if (b.indexOf('-') > 0) {
            var deDateb = $.trim(b).split('-');
            if (deDateb[1].length == 1) {
                deDateb[1] = 0 + deDateb[1];
            }
            if (deDateb[2].length == 1) {
                deDateb[2] = 0 + deDateb[2];
            }
            y = (deDateb[2] + deDateb[1] + deDateb[0]) * 1;
        }
        else {
            var deDateb = $.trim(b).split('.');
            y = (deDateb[2] + deDateb[1] + deDateb[0]) * 1;
        }
    } else {
        y = Infinity;
    }
    var z = ((x < y) ? -1 : ((x > y) ? 1 : 0));
    return z;
},

"de_date-desc": function (a, b) {
    //debugger;
    var x, y;
    if ($.trim(a) !== '') {
        if (a.indexOf('年') > 0) {
            a = a.replace("年", ".").replace("月", ".").replace("日", ".");
            var deDatea = $.trim(a).split('.');
            if (deDatea[1].length == 1) {
                deDatea[1] = 0 + deDatea[1];
            }
            if (deDatea[2].length == 1) {
                deDatea[2] = 0 + deDatea[2];
            }
            x = (deDatea[0] + deDatea[1] + deDatea[2]) * 1;
        }
        else if (a.indexOf('-') > 0) {
            var deDatea = $.trim(a).split('-');
            if (deDatea[1].length == 1) {
                deDatea[1] = 0 + deDatea[1];
            }
            if (deDatea[2].length == 1) {
                deDatea[2] = 0 + deDatea[2];
            }
            x = (deDatea[2] + deDatea[1] + deDatea[0]) * 1;
        }
        else {
            var deDatea = $.trim(a).split('.');
            x = (deDatea[2] + deDatea[1] + deDatea[0]) * 1;
        }
    } else {
        x = Infinity;
    }

    if ($.trim(b) !== '') {
        if (b.indexOf('年') > 0) {
            b = b.replace("年", ".").replace("月", ".").replace("日", ".");
            var deDateb = $.trim(b).split('.');
            if (deDateb[1].length == 1) {
                deDateb[1] = 0 + deDateb[1];
            }
            if (deDateb[2].length == 1) {
                deDateb[2] = 0 + deDateb[2];
            }
            y = (deDateb[0] + deDateb[1] + deDateb[2]) * 1;
        }
        else if (b.indexOf('-') > 0) {
            var deDateb = $.trim(b).split('-');
            if (deDateb[1].length == 1) {
                deDateb[1] = 0 + deDateb[1];
            }
            if (deDateb[2].length == 1) {
                deDateb[2] = 0 + deDateb[2];
            }
            y = (deDateb[2] + deDateb[1] + deDateb[0]) * 1;
        }
        else {
            var deDateb = $.trim(b).split('.');
            y = (deDateb[2] + deDateb[1] + deDateb[0]) * 1;
        }
    } else {
        y = Infinity;
    }
    var z = ((x < y) ? 1 : ((x > y) ? -1 : 0));
    return z;
}
});