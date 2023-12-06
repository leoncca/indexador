Esto es un sencillo buscador de palabras, o indexador, que hice para una asignatura de procesado de lenguaje natural en la universidad.


Extras implementados:
	-> Varios índices; uno por sección (título,cuerpo,categoría y fecha)
	-> Búsqueda de sintagmas (palabras contiguas en los documentos))
	NOTA: No se pueden usar a la vez (los sintagmas se buscan siempre en el cuerpo)

Uso de los dos programas:

indexador.py:
	Sintaxis llamada: indexador [archivo_destino]
		la ruta del archivo se pondrá como ruta relativa
recuperador.py:
	Sintaxis llamada: recuperador.py [ruta_índice]
		la ruta del archivo se pondrá como ruta relativa
	Sintaxis consultas: ["sintagma"]*[palabra|([headline|text|date|category]:palabra)]*
		donde: sintagma denota una serie de palabras separadas por espacios;
				 | denota la operación "+"("o" u "OR") en álgebra de expresiones regulares;
				 * denota la clausura de Kleene de expr. regulares;
				 () cambian la prioridad de operaciones;
				 el vacío entre clases adyacentes es la concatenación de expr. regulares;
				 palabra denota una cadena de símbolos sin espacios en medio.
	Informalmente: Varios o ningún sintagma primero; luego una serie de palabras o de sección:palabra o ninguna cosa.
