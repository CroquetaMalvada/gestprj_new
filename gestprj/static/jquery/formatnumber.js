function formatnumber ( d ,thousands, decimal, precision, prefix, postfix ) { //formatea un numero(sirve para cuando el render.number de las datatables no se pouede usar)
            if ( typeof d !== 'number' && typeof d !== 'string' ) {
                return d;
            }
            d=d.toString();
//            alert(d+" - "+thousands+" - "+decimal);
//            if (d==0)//ojo funcion que evita que se formatee el numero 0
//                return d;

            if (d.indexOf(thousands) > -1 && d.indexOf(decimal) > -1){//ojo! funcion añadida que comprueba si el numero a formatear ya tiene el formato que deseamos,en cuyo caso lo devolverá como está y nada mas
                return d;
            }

            var negative = d < 0 ? '-' : '';
            var flo = parseFloat( d );

            // If NaN then there isn't much formatting that we can do - just
            // return immediately, escaping any HTML (this was supposed to
            // be a number after all)
            if ( isNaN( flo ) ) {
                return 0;
            }

            flo = flo.toFixed( precision );
            d = Math.abs( flo );

            var intPart = parseInt( d, 10 );
            var floatPart = precision ?
                decimal+(d - intPart).toFixed( precision ).substring( 2 ):
                '';

            return negative + (prefix||'') +
                intPart.toString().replace(
                    /\B(?=(\d{3})+(?!\d))/g, thousands
                ) +
                floatPart +
                (postfix||'');

}

function formatear_tablas(){//detecta los numeros de las datatables y los formatea con la funcion de arriba
//    $("table").find("tbody").find("td").each(function(){
//
//    });
}