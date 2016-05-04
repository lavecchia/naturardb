
def rows_transpose(rows_obj , headers=None): 
    """transposes a rows object 

    input:    a rows object selected from the data base 
              optional headers dictionary
    output:   a html table of the transposed table 

    This can still be improved by using the headers attribute of the 
    SQLTABLE and a CSS alogn attribute   
    add mjl
    """ 

    tbody=[] 
    for col in rows_obj.colnames: 
        fld=col.split('.')[1]
        if headers:
            if col in headers:
                col = headers[col]
        else:
            exec("col = db." + col + ".label")
        r=[TH(col,_scope='row', _style="text-align : left")]
        for row in rows_obj: 
            r.append(TD(row[fld], _style="text-align : right")) 
        tbody.append(TR(r)) 
    res_table=TABLE(tbody) 


    return res_table 


