function clearTable(table_id, setDefault, defaultRowHtml) {
    var table = $(table_id)
    if (table != null) {
        while(table[0].rows.length > 1) {
            table[0].deleteRow(table[0].rows.length-1);
        }
        if (setDefault != null && setDefault) {
            $(table_id + ' > tbody:first').append(defaultRowHtml);
        }
    }
}