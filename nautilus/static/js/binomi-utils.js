/*!
 * Author: Ferran Gurri Mancera
 */

 /*!
 * Fills the value of two controls identified by string id representing the specified year range in format YYYYMM
 * return:
 * p_monthini: id string of the control we want to fill with starting value
 * p_monthfinal: id string of the control we want to fill with ending value
 * p_year: year string
 */
function showYear (p_monthini, p_monthfinal, p_year) {
    document.getElementById(p_monthini).value = p_year+"01";
    document.getElementById(p_monthfinal).value = p_year+"12";
}

/*!
 * Fills the value of two controls identified by string id with the current year in format YYYYMM
 * return:
 * p_monthini: id string of the control we want to fill with starting value
 * p_monthfinal: id string of the control we want to fill with ending value
 */
function currentYear(p_monthini, p_monthfinal) {
    var d = new Date();
    var monthini = new Date(d.getFullYear(), 0, 1);
    var monthfinal = new Date(d.getFullYear(), d.getMonth()-1, 1);
    document.getElementById(p_monthini).value = monthini.getFullYear() + ("0" + (monthini.getMonth()+1)).slice(-2);
    document.getElementById(p_monthfinal).value = monthfinal.getFullYear() + ("0" + (monthfinal.getMonth()+1)).slice(-2);
}


/*!
 * Fills the value of two controls identified by string id with the last 12 months in format YYYYMM.
 * Only considers finished months, so last month is not the current one but the last.
 * return:
 * p_monthini: id string of the control we want to fill with starting value
 * p_monthfinal: id string of the control we want to fill with ending value
 */
function last12months (p_monthini, p_monthfinal) {
    var d = new Date();
    var monthini = new Date(d.getFullYear()-1, d.getMonth(), 1);
    var monthfinal = new Date(d.getFullYear(), d.getMonth()-1, 1);
    document.getElementById(p_monthini).value = monthini.getFullYear() + ("0" + (monthini.getMonth()+1)).slice(-2);
    document.getElementById( p_monthfinal).value = monthfinal.getFullYear() + ("0" + (monthfinal.getMonth()+1)).slice(-2);
}
