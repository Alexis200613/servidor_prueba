# servidor_prueba
GET: Se usa exclusivamente para **consultar o leer** información. No modifica absolutamente nada en el servidor.
* POST: Se usa para **crear** un recurso nuevo. El servidor decide qué identificador (ID) asignarle.
* PATCH: Se usa para **modificar parcialmente** un recurso existente. Solo envías los datos que cambian, dejando el resto intacto.
* DELETE: Se usa para **eliminar** un recurso específico.

* POST no es idempotente porque cada petición crea un recurso nuevo.
