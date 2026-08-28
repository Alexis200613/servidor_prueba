from wsgiref.simple_server import make_server
import json

lista_tareas = {}
contador_id = 0

def mi_server(environ, start_response):
    global contador_id
    metodo = environ.get('REQUEST_METHOD', 'GET')
    ruta = environ.get('PATH_INFO','/')
    partes = ruta.split('/')
    id = None
    headers = [('Content-Type', 'application/json; charset=utf-8')]
    
    if len(partes) > 2:
        id = int(partes[2])
    
    if metodo == 'GET' and partes[1] == 'tasks':
        status = '200 OK'

        if len(partes) == 2 and len(lista_tareas) == 0:
            status = '404 Not Found'
            start_response(status, headers)
            return [b'no hay datos en la lista aun'] 

        if id != None:
            if lista_tareas.get(id) == None:
                status = '404 Not Found'
                start_response(status, headers)
                print(id)
                return [b'el id no pertenece a la lista']
            
            else:
                start_response(status, headers)
                return [json.dumps(lista_tareas.get(id)).encode('utf-8')]
        
        else:
            start_response(status, headers)
            return [json.dumps(lista_tareas).encode('utf-8')]

    if metodo == 'POST' and partes[1] == 'tasks':  
        status = '200 OK'
        cuerpo_crudo = environ.get('CONTENT_LENGTH','0')
        longitud = int(cuerpo_crudo) if cuerpo_crudo.isdigit() else 0

        if longitud > 0:
            cuerpo_post = environ['wsgi.input'].read(longitud)
            try:
                cuerpo_aguardar = json.loads(cuerpo_post)
                lista_tareas[contador_id] = cuerpo_aguardar
                contador_id += 1
                start_response(status, headers)
                return [b'el objeto se guardo correctamente']
            except json.decoder.JSONDecodeError:
                status = '404 Not Found'
                start_response(status, headers)
                return [b'no se pudo guardar el objeto']

    if metodo == 'PATCH' and partes[1] == 'tasks':
        try:
            tarea_existente = lista_tareas.get(id)
            
            if tarea_existente is None:
                start_response('404 Not Found', [('Content-Type', 'application/json')])
                return [b'{"error": "La tarea no existe"}']
                
            longitud = int(environ.get('CONTENT_LENGTH', 0))
            cuerpo_patch = json.loads(environ['wsgi.input'].read(longitud))
            
            tarea_existente.update(cuerpo_patch)
            
            status = '200 OK'
            headers = [('Content-Type', 'application/json')]
            start_response(status, headers)
            return [json.dumps(tarea_existente).encode('utf-8')]
            
        except ValueError:
            start_response('400 Bad Request', [('Content-Type', 'application/json')])
            return [b'{"error": "ID de tarea invalido"}']

    if metodo == 'DELETE' and partes[1] == 'tasks':
        if id != None and lista_tareas.get(id) != None:
            status = '200 OK'
            del lista_tareas[id] 
            start_response(status, headers)
            return [b'se borro corectamente el objeto']
        else:
            status = '404 Not Found'
            start_response(status, headers)
            return [b'no se pudo borrar el objeto']
    
    else:
        status = '404 error'
        headers = [('content-type','text/html; charset=utf-8')]
        start_response(status, headers)
        return [b'que dijo chat?']

with make_server('localhost', 9292, mi_server) as servidor:
    print("servidor activo en http://localhost:9292")
    servidor.serve_forever()